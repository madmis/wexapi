from decimal import Decimal


class Trade(object):
    def __init__(
            self,
            pair: str,
            type: str,
            price: float,
            amount: float,
            tid: int,
            timestamp: int,
    ):
        self.pair = pair
        self.type = type
        self.price = price
        self.amount = amount
        self.tid = tid
        self.timestamp = timestamp

    @property
    def pair(self) -> str:
        return self._pair

    @pair.setter
    def pair(self, value: str):
        self._pair = value

    @property
    def type(self) -> str:
        return self._type

    @type.setter
    def type(self, value: str):
        self._type = value

    @property
    def price(self) -> Decimal:
        return self._price

    @price.setter
    def price(self, value: float):
        self._price = Decimal(value)

    @property
    def amount(self) -> Decimal:
        return self._amount

    @amount.setter
    def amount(self, value: float):
        self._amount = Decimal(value)

    @property
    def tid(self) -> int:
        return self._tid

    @tid.setter
    def tid(self, value: int):
        self._tid = int(value)

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: int):
        self._timestamp = int(value)
