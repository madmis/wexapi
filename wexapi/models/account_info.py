class AccountInfo(object):
    def __init__(
            self,
            funds: dict,
            open_orders: int,
            transaction_count: int,
            server_time: int,
            rights: dict,
    ):
        self.funds = funds
        self.open_orders = open_orders
        self.transaction_count = transaction_count
        self.server_time = server_time
        self.info_rights = rights.get('info')
        self.withdraw_rights = rights.get('withdraw')
        self.trade_rights = rights.get('trade')

    @property
    def funds(self) -> dict:
        return self._funds

    @funds.setter
    def funds(self, value: dict):
        self._funds = value

    @property
    def open_orders(self) -> int:
        return self._open_orders

    @open_orders.setter
    def open_orders(self, value: int):
        self._open_orders = int(value)

    @property
    def transaction_count(self) -> int:
        return self._transaction_count

    @transaction_count.setter
    def transaction_count(self, value: int):
        self._transaction_count = int(value)

    @property
    def server_time(self) -> int:
        return self._server_time

    @server_time.setter
    def server_time(self, value: int):
        self._server_time = int(value)

    @property
    def info_rights(self) -> bool:
        return self._info_rights

    @info_rights.setter
    def info_rights(self, value: bool):
        self._info_rights = bool(value)

    @property
    def withdraw_rights(self) -> bool:
        return self._withdraw_rights

    @withdraw_rights.setter
    def withdraw_rights(self, value: bool):
        self._withdraw_rights = bool(value)

    @property
    def trade_rights(self) -> bool:
        return self._trade_rights

    @trade_rights.setter
    def trade_rights(self, value: bool):
        self._trade_rights = bool(value)
