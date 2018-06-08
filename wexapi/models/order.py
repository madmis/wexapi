from decimal import Decimal


class Order(object):
    def __init__(
            self,
            order_id: int,
            pair: str,
            type: str,
            amount: float,
            rate: float,
            timestamp_created: int,
            status: int,
    ):
        self.order_id = order_id
        self.pair = pair
        self.type = type
        self.amount = amount
        self.rate = rate
        self.timestamp_created = timestamp_created
        self.status = status

    @property
    def order_id(self) -> int:
        return self._order_id

    @order_id.setter
    def order_id(self, value: int):
        self._order_id = int(value)

    @property
    def pair(self) -> str:
        return self._pair

    @pair.setter
    def pair(self, value: str):
        self._pair = str(value)

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
    def rate(self) -> Decimal:
        return self._rate

    @rate.setter
    def rate(self, value: float):
        self._rate = Decimal(value)

    @property
    def timestamp_created(self) -> int:
        return self._timestamp_created

    @timestamp_created.setter
    def timestamp_created(self, value: int):
        self._timestamp_created = int(value)

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int):
        self._status = int(value)
