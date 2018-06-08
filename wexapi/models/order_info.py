from decimal import Decimal
from wexapi.models import Order


class OrderInfo(Order):
    def __init__(
            self,
            order_id: int,
            pair: str,
            type: str,
            start_amount: float,
            amount: float,
            rate: float,
            timestamp_created: int,
            status: int,
    ):
        super().__init__(
            order_id,
            pair,
            type,
            amount,
            rate,
            timestamp_created,
            status,
        )
        self.start_amount = start_amount

    @property
    def start_amount(self) -> Decimal:
        return self._start_amount

    @start_amount.setter
    def start_amount(self, value: float):
        self._start_amount = Decimal(value)
