import unittest
from decimal import Decimal
from wexapi.models import Ticker


class TestTicker(unittest.TestCase):
    def test_create_valid(self):
        data = {
            "high": 109.88,
            "low": 91.14,
            "avg": 100.51,
            "vol": 1632898.2249,
            "vol_cur": 16541.51969,
            "last": 101.773,
            "buy": 101.9,
            "sell": 101.773,
            "updated": 1370816308,
        }
        ticker = Ticker(**data)

        self.assertIsInstance(ticker.avg, Decimal)
        self.assertEqual(ticker.avg, Decimal(100.51))

        self.assertIsInstance(ticker.buy, Decimal)
        self.assertEqual(ticker.buy, Decimal(101.9))

        self.assertIsInstance(ticker.sell, Decimal)
        self.assertEqual(ticker.sell, Decimal(101.773))

        self.assertIsInstance(ticker.high, Decimal)
        self.assertEqual(ticker.high, Decimal(109.88))

        self.assertIsInstance(ticker.low, Decimal)
        self.assertEqual(ticker.low, Decimal(91.14))

        self.assertIsInstance(ticker.last, Decimal)
        self.assertEqual(ticker.last, Decimal(101.773))

        self.assertIsInstance(ticker.vol, Decimal)
        self.assertEqual(ticker.vol, Decimal(1632898.2249))

        self.assertIsInstance(ticker.vol_cur, Decimal)
        self.assertEqual(ticker.vol_cur, Decimal(16541.51969))

        self.assertIsInstance(ticker.updated, int)
        self.assertEqual(ticker.updated, 1370816308)


if __name__ == '__main__':
    unittest.main()
