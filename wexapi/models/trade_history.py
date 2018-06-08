from decimal import Decimal


class TradeHistory(object):
    def __init__(
            self,
            transaction_id: int,
            type: str,
            amount: float,
            pair: str,
            rate: float,
            order_id: int,
            is_your_order: int,
            timestamp: int,
    ):
        self.transaction_id = transaction_id
        self.type = type
        self.amount = amount
        self.pair = pair
        self.rate = rate
        self.order_id = order_id
        self.is_your_order = is_your_order
        self.timestamp = timestamp

    @property
    def transaction_id(self) -> int:
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value: int):
        self._transaction_id = int(value)

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = str(value)

    @property
    def amount(self) -> Decimal:
        return self._amount

    @amount.setter
    def amount(self, value: float):
        self._amount = Decimal(value)

    @property
    def pair(self) -> str:
        return self._pair

    @pair.setter
    def pair(self, value: str):
        self._pair = str(value)

    @property
    def rate(self) -> Decimal:
        return self._rate

    @rate.setter
    def rate(self, value: float):
        self._rate = Decimal(value)

    @property
    def order_id(self) -> int:
        return self._order_id

    @order_id.setter
    def order_id(self, value: int):
        self._order_id = int(value)

    @property
    def is_your_order(self) -> bool:
        return self._is_your_order

    @is_your_order.setter
    def is_your_order(self, value: int):
        self._is_your_order = bool(value)

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: int):
        self._timestamp = int(value)
