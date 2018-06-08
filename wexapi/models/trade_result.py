from decimal import Decimal


class TradeResult(object):
    def __init__(
            self,
            received: float,
            remains: float,
            order_id: int,
            funds: {},
    ):
        self.received = received
        self.remains = remains
        self.order_id = order_id
        self.funds = funds

    @property
    def received(self) -> Decimal:
        return self._received

    @received.setter
    def received(self, value: float):
        self._received = Decimal(value)

    @property
    def remains(self) -> Decimal:
        return self._remains

    @remains.setter
    def remains(self, value: float):
        self._remains = Decimal(value)

    @property
    def order_id(self) -> int:
        return self._order_id

    @order_id.setter
    def order_id(self, value: int):
        self._order_id = int(value)

    @property
    def funds(self) -> {}:
        return self._funds

    @funds.setter
    def funds(self, value: {}):
        self._funds = value
