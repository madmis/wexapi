from decimal import Decimal


class TransHistory(object):
    def __init__(
            self,
            transaction_id: int,
            type: int,
            amount: float,
            currency: str,
            desc: str,
            status: int,
            timestamp: int,
    ):
        self.transaction_id = transaction_id
        self.type = type
        self.amount = amount
        self.currency = currency
        self.desc = desc
        self.status = status
        self.timestamp = timestamp

    @property
    def transaction_id(self) -> int:
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, value: int):
        self._transaction_id = int(value)

    @property
    def type(self) -> int:
        return self._type

    @type.setter
    def type(self, value: int):
        self._type = int(value)

    @property
    def amount(self) -> Decimal:
        return self._amount

    @amount.setter
    def amount(self, value: float):
        self._amount = Decimal(value)

    @property
    def currency(self) -> str:
        return self._currency

    @currency.setter
    def currency(self, value: str):
        self._currency = str(value)

    @property
    def desc(self) -> str:
        return self._desc

    @desc.setter
    def desc(self, value: str):
        self._desc = str(value)

    @property
    def status(self) -> int:
        return self._status

    @status.setter
    def status(self, value: int):
        self._status = int(value)

    @property
    def timestamp(self) -> int:
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value: int):
        self._timestamp = int(value)
