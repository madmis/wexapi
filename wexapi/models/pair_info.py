from decimal import Decimal


class PairInfo(object):
    def __init__(
            self,
            decimal_places: int,
            min_price: float,
            max_price: float,
            min_amount: float,
            hidden: int,
            fee: float,
    ):
        self.decimal_places = decimal_places
        self.min_price = min_price
        self.max_price = max_price
        self.min_amount = min_amount
        self.hidden = hidden
        self.fee = fee

    @property
    def decimal_places(self) -> int:
        return self._decimal_places

    @decimal_places.setter
    def decimal_places(self, value: int):
        self._decimal_places = int(value)

    @property
    def min_price(self) -> Decimal:
        return self._min_price

    @min_price.setter
    def min_price(self, value: float):
        self._min_price = Decimal(value)

    @property
    def max_price(self) -> Decimal:
        return self._max_price

    @max_price.setter
    def max_price(self, value: float):
        self._max_price = Decimal(value)

    @property
    def min_amount(self) -> Decimal:
        return self._min_amount

    @min_amount.setter
    def min_amount(self, value: float):
        self._min_amount = Decimal(value)

    @property
    def hidden(self) -> bool:
        return self._hidden

    @hidden.setter
    def hidden(self, value: int):
        self._hidden = bool(value)

    @property
    def fee(self) -> Decimal:
        return self._fee

    @fee.setter
    def fee(self, value: float):
        self._fee = Decimal(value)
