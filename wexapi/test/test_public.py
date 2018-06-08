from decimal import Decimal
import unittest

import wexapi.models as models
from wexapi.common import WexConnection
from wexapi.public import PublicApi, InfoApi


class TestPublic(unittest.TestCase):
    pair = "bch_btc"

    def test_get_ticker(self):
        connection = WexConnection()
        api = PublicApi(connection)
        ticker = api.get_ticker(self.pair)

        self.assertIsInstance(ticker, models.Ticker)

        info = InfoApi(connection)
        api.get_ticker(self.pair, info=info)

    def test_get_history(self):
        connection = WexConnection()
        api = PublicApi(connection)
        history = api.get_trade_history(self.pair, limit=1)

        self.assertIsInstance(history, list)
        self.assertIsInstance(history[0], models.Trade)

        info = InfoApi(connection)
        api.get_trade_history(self.pair, info=info, limit=1)

    def test_get_depth(self):
        connection = WexConnection()
        api = PublicApi(connection)
        self.assertIsInstance(api.get_depth(self.pair, limit=1), tuple)

        asks, bids = api.get_depth(self.pair, limit=1)

        self.assertIsInstance(asks, list)
        self.assertIsInstance(asks[0], list)
        self.assertIsInstance(asks[0][0], Decimal)
        self.assertIsInstance(asks[0][1], Decimal)

        self.assertIsInstance(bids, list)
        self.assertIsInstance(bids[0], list)
        self.assertIsInstance(bids[0][0], Decimal)
        self.assertIsInstance(bids[0][1], Decimal)

        info = InfoApi(connection)
        api.get_depth(self.pair, info=info, limit=1)


if __name__ == '__main__':
    unittest.main()
