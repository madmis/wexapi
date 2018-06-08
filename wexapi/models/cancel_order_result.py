class CancelOrderResult(object):
    def __init__(
            self,
            order_id: int,
            funds: {},
    ):
        self.order_id = order_id
        self.funds = funds

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
