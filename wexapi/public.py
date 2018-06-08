# Public API v3 description: https://wex.nz/api/3/docs
from decimal import Decimal
from html import unescape
from typing import Union, List, Tuple

import wexapi.common as common
import wexapi.models as models
import wexapi.scraping as scraping
from wexapi.utils import format_currency_digits


class InfoApi(object):
    def __init__(self, connection):
        self.connection = connection
        self.currencies = None
        self.pair_names = None
        self.pairs = None
        self.server_time = None

        self._scrape_pair_index = 0

        self.update()

    def update(self):
        info = self.connection.make_json_request("/api/3/info")
        if type(info) is not dict:
            raise TypeError("The response is not a dict.")

        self.server_time = info.get("server_time")

        pairs = info.get("pairs")
        if type(pairs) is not dict:
            raise TypeError("The pairs item is not a dict.")

        self.pairs = {}
        currencies = set()
        for name, data in pairs.items():
            self.pairs[name] = models.PairInfo(**data)
            a, b = name.split("_")
            currencies.add(a)
            currencies.add(b)

        self.currencies = list(currencies)
        self.currencies.sort()

        self.pair_names = list(self.pairs.keys())
        self.pair_names.sort()

    def validate_pair(self, pair: str):
        if pair not in self.pair_names:
            if "_" in pair:
                a, b = pair.split("_", 1)
                swapped_pair = "{}_{}".format(b, a)
                if swapped_pair in self.pair_names:
                    msg = "Unrecognized pair: {} (did you mean {}?)".format(pair, swapped_pair)
                    raise common.InvalidTradePairException(msg)
            raise common.InvalidTradePairException("Unrecognized pair: {}".format(pair))

    def get_pair_info(self, pair: str) -> models.PairInfo:
        self.validate_pair(pair)
        return self.pairs[pair]

    def validate_order(self, pair: str, trade_type: str, rate: Decimal, amount: Decimal):
        self.validate_pair(pair)

        pair_info = self.pairs[pair]

        if trade_type not in ("buy", "sell"):
            raise common.InvalidTradeTypeException("Unrecognized trade type: {}".format(trade_type))

        formatted_min_amount = format_currency_digits(pair_info.min_amount, pair_info.decimal_places)
        formatted_amount = format_currency_digits(amount, pair_info.decimal_places)
        if amount < pair_info.min_amount:
            msg = "Trade amount {} too small; should be >= {}".format(formatted_amount, formatted_min_amount)
            raise common.InvalidTradeAmountException(msg)

    def scrape_main_page(self) -> scraping.ScraperResults:
        parser = scraping.WexScraper()

        # Rotate through the currency pairs between chat requests so that the
        # chat pane contents will update more often than every few minutes.
        self._scrape_pair_index = (self._scrape_pair_index + 1) % len(self.pair_names)
        current_pair = self.pair_names[self._scrape_pair_index]

        response = self.connection.make_request('/exchange/%s' % current_pair, with_cookie=True)

        parser.feed(unescape(response.read().decode('utf-8')))
        parser.close()

        r = scraping.ScraperResults()
        r.messages = parser.messages
        r.dev_online = parser.dev_online
        r.support_online = parser.support_online
        r.admin_online = parser.admin_online

        return r

    def format_currency(self, pair: str, amount: Union[float, int, str, Decimal]) -> str:
        self.validate_pair(pair)

        pair_info = self.pairs[pair]

        return format_currency_digits(amount, pair_info.decimal_places)


class PublicApi(object):
    def __init__(self, connection):
        self.connection = connection
        self.base_path = "/api/3"

    def _request(self, url: str, extra_headers=None, params: str = "") -> dict:
        return self.connection.make_json_request(
            url="{}{}".format(self.base_path, url),
            extra_headers=extra_headers,
            params=params
        )

    def get_ticker(self, pair: str, info: InfoApi = None) -> Union[models.Ticker, None]:
        """
        Retrieve the ticker for the given pair.  Returns a Ticker instance.
        """

        if info is not None:
            info.validate_pair(pair)

        response = self._request("/ticker/{}".format(pair))

        if type(response) is not dict:
            raise TypeError("The response is a %r, not a dict." % type(response))
        elif 'error' in response:
            print("There is a error \"{}\" while obtaining ticker {}".format(response['error'], pair))
            ticker = None
        else:
            ticker = models.Ticker(**response[pair])

        return ticker

    def get_depth(self, pair: str, info: InfoApi = None, limit: int = 150) -> Tuple[List[Decimal], List[Decimal]]:
        """
        Retrieve the depth for the given pair.
        Returns a tuple (asks, bids);
        each of these is a list of (price, volume) tuples.
        """

        if info is not None:
            info.validate_pair(pair)

        response = self._request("/depth/{}?limit={}".format(pair, limit))
        if type(response) is not dict:
            raise TypeError("The response is not a dict.")

        depth = response.get(pair)
        if type(depth) is not dict:
            raise TypeError("The pair depth is not a dict.")

        asks = depth.get('asks')
        if type(asks) is not list:
            raise TypeError("The response does not contain an asks list.")

        bids = depth.get('bids')
        if type(bids) is not list:
            raise TypeError("The response does not contain a bids list.")

        return asks, bids

    def get_trade_history(self, pair: str, info: InfoApi = None, limit: int = 150) -> List[models.Trade]:
        """
        Retrieve the trade history for the given pair.
        Returns a list of Trade instances.
        """

        if info is not None:
            info.validate_pair(pair)

        response = self._request("/trades/{}?limit={}".format(pair, limit))
        if type(response) is not dict:
            raise TypeError("The response is not a dict.")

        history = response.get(pair)
        if type(history) is not list:
            raise TypeError("The response is a %r, not a list." % type(history))

        result = []
        for h in history:
            h["pair"] = pair
            t = models.Trade(**h)
            result.append(t)

        return result
