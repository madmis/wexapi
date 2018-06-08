from decimal import Decimal


class Ticker(object):
    def __init__(
            self,
            high: float,
            low: float,
            avg: float,
            vol: float,
            vol_cur: int,
            last: float,
            buy: float,
            sell: float,
            updated: int,
    ):
        self.high = high
        self.low = low
        self.avg = avg
        self.vol = vol
        self.vol_cur = vol_cur
        self.last = last
        self.buy = buy
        self.sell = sell
        self.updated = updated

    @property
    def high(self) -> Decimal:
        return self._high

    @high.setter
    def high(self, value: float):
        self._high = Decimal(value)

    @property
    def low(self) -> Decimal:
        return self._low

    @low.setter
    def low(self, value: float):
        self._low = Decimal(value)

    @property
    def avg(self) -> Decimal:
        return self._avg

    @avg.setter
    def avg(self, value: float):
        self._avg = Decimal(value)

    @property
    def vol(self) -> Decimal:
        return self._vol

    @vol.setter
    def vol(self, value: float):
        self._vol = Decimal(value)

    @property
    def vol_cur(self) -> Decimal:
        return self._vol_cur

    @vol_cur.setter
    def vol_cur(self, value: float):
        self._vol_cur = Decimal(value)

    @property
    def last(self) -> Decimal:
        return self._last

    @last.setter
    def last(self, value: float):
        self._last = Decimal(value)

    @property
    def buy(self) -> Decimal:
        return self._buy

    @buy.setter
    def buy(self, value: float):
        self._buy = Decimal(value)

    @property
    def sell(self) -> Decimal:
        return self._sell

    @sell.setter
    def sell(self, value: float):
        self._sell = Decimal(value)

    @property
    def updated(self) -> int:
        return self._updated

    @updated.setter
    def updated(self, value: int):
        self._updated = int(value)
