from decimal import Decimal
import hashlib
import hmac
import warnings
from typing import List
from urllib.parse import urlencode

from wexapi.common import WexConnection
from wexapi.keyhandler import AbstractKeyHandler
from wexapi.models import (
    AccountInfo, TransHistory,
    TradeHistory, Order, TradeResult, CancelOrderResult,
    OrderInfo,
)
from wexapi.public import InfoApi
from wexapi.utils import format_currency_digits


class InvalidNonceException(Exception):
    def __init__(self, method: str, expected_nonce: int, actual_nonce: int):
        Exception.__init__(self)
        self.method = method
        self.expected_nonce = expected_nonce
        self.actual_nonce = actual_nonce

    def __str__(self):
        return "Expected a nonce greater than {}".format(self.expected_nonce)


class InvalidSortOrderException(Exception):
    """ Exception thrown when an invalid sort order is passed """
    pass


class TradeApi(object):
    def __init__(self, key: str, handler: AbstractKeyHandler, connection: WexConnection):
        self.key = key
        self.handler = handler
        self.connection = connection
        self.apiInfo = InfoApi(self.connection)
        self.raise_if_invalid_nonce = True

        if not isinstance(self.handler, AbstractKeyHandler):
            raise TypeError(
                "The handler argument must be a keyhandler.AbstractKeyHandler, such as keyhandler.KeyHandler"
            )

        # We depend on the key handler for the secret
        self.secret = handler.get_secret(key)

    def _post(self, params: dict, allow_nonce_retry: bool = False) -> dict:
        params["nonce"] = self.handler.get_next_nonce(self.key)
        encoded_params = urlencode(params)

        # Hash the params string to produce the Sign header value
        h = hmac.new(self.secret.encode('utf-8'), digestmod=hashlib.sha512)
        h.update(encoded_params.encode('utf-8'))
        sign = h.hexdigest()

        headers = {"Key": self.key, "Sign": sign}
        result = self.connection.make_json_request("/tapi", headers, encoded_params)

        success = result.get('success')
        if not success:
            err_message = result.get('error')
            method = params.get("method", "[unknown method]")

            if "invalid nonce" in err_message:
                # If the nonce is out of sync, make one attempt to update to
                # the correct nonce.  This sometimes happens if a bot crashes
                # and the nonce file doesn't get saved, so it's reasonable to
                # attempt a correction.  If multiple threads/processes are
                # attempting to use the same key, this mechanism will
                # eventually fail and the InvalidNonce will be emitted so that
                # you'll end up here reading this comment. :)

                # The assumption is that the invalid nonce message looks like
                # "invalid nonce parameter; on key:4, you sent:3"
                s = err_message.split(",")
                expected = int(s[-2].split(":")[1].strip("'"))
                actual = int(s[-1].split(":")[1].strip("'"))
                if self.raise_if_invalid_nonce and not allow_nonce_retry:
                    raise InvalidNonceException(method, expected, actual)

                warnings.warn("The nonce in the key file is out of date; attempting to correct.")
                self.handler.set_next_nonce(self.key, expected + 1000)
                return self._post(params, True)
            elif "no orders" in err_message and method == "ActiveOrders":
                # ActiveOrders returns failure if there are no orders;
                # intercept this and return an empty dict.
                return {}
            elif "no trades" in err_message and method == "TradeHistory":
                # TradeHistory returns failure if there are no trades;
                # intercept this and return an empty dict.
                return {}

            raise Exception("{} call failed with error: {}".format(method, err_message))

        if 'return' not in result:
            raise Exception("Response does not contain a 'return' item.")

        return result.get('return')

    def get_info(self) -> AccountInfo:
        params = {"method": "getInfo"}
        return AccountInfo(**self._post(params))

    def trans_history(
            self,
            from_number: int = None,
            count_number: int = None,
            from_id: int = None,
            end_id: int = None,
            order: str = "DESC",
            since: int = None,
            end: int = None,
    ) -> List[TransHistory]:

        params = self._format_history_params(from_number, count_number, from_id, end_id, order, since, end)
        params["method"] = "TransHistory"

        orders = self._post(params)
        result = []
        for k, v in orders.items():
            v['transaction_id'] = int(k)
            result.append(TransHistory(**v))

        # We have to sort items here because the API returns a dict
        if "ASC" == order:
            result.sort(key=lambda a: a.transaction_id, reverse=False)
        elif "DESC" == order:
            result.sort(key=lambda a: a.transaction_id, reverse=True)

        return result

    def trade_history(
            self,
            from_number: int = None,
            count_number: int = None,
            from_id: int = None,
            end_id: int = None,
            order: str = "DESC",
            since: int = None,
            end: int = None,
            pair: str = None,
    ) -> List[TradeHistory]:
        params = self._format_history_params(from_number, count_number, from_id, end_id, order, since, end)
        params["method"] = "TradeHistory"

        if pair is not None:
            self.apiInfo.validate_pair(pair)
            params["pair"] = pair

        orders = list(self._post(params).items())
        orders.sort(reverse=order != "ASC")
        result = []
        for k, v in orders:
            result.append(TradeHistory(int(k), **v))

        return result

    def active_orders(self, pair: str = None) -> List[Order]:

        params = {"method": "ActiveOrders"}

        if pair is not None:
            self.apiInfo.validate_pair(pair)
            params["pair"] = pair

        orders = self._post(params)
        result = []
        for k, v in orders.items():
            v['order_id'] = int(k)
            result.append(Order(**v))

        return result

    def trade(self, pair: str, trade_type: str, rate: Decimal, amount: Decimal) -> TradeResult:
        pair_info = self.apiInfo.get_pair_info(pair)
        self.apiInfo.validate_order(pair, trade_type, rate, amount)

        params = {
            "method": "Trade",
            "pair": pair,
            "type": trade_type,
            "rate": format_currency_digits(rate, pair_info.decimal_places),
            "amount": format_currency_digits(amount, pair_info.decimal_places)
        }

        return TradeResult(**self._post(params))

    def cancel_order(self, order_id: int) -> CancelOrderResult:
        params = {
            "method": "CancelOrder",
            "order_id": order_id
        }
        return CancelOrderResult(**self._post(params))

    def order_info(self, order_id: int) -> OrderInfo:
        params = {"method": "OrderInfo", "order_id": order_id}
        orders = self._post(params)

        order = orders[order_id]
        order['order_id'] = order_id

        return OrderInfo(**order)

    def _format_history_params(
            self,
            from_number: int = None,
            count_number: int = None,
            from_id: int = None,
            end_id: int = None,
            order: str = "DESC",
            since: int = None,
            end: int = None,
    ):
        params = {}
        if from_number is not None:
            params["from"] = "{}".format(from_number)
        if count_number is not None:
            params["count"] = "{}".format(count_number)
        if from_id is not None:
            params["from_id"] = "{}".format(from_id)
        if end_id is not None:
            params["end_id"] = "{}".format(end_id)
        if order is not None:
            if order not in ("ASC", "DESC"):
                raise InvalidSortOrderException("Unexpected order parameter: %r" % order)
            params["order"] = order
        if since is not None:
            params["since"] = "{}".format(since)
        if end is not None:
            params["end"] = "{}".format(end)

        return params
