import unittest
from decimal import Decimal
from wexapi.models import TradeResult


class TestTradeResult(unittest.TestCase):
    def test_create_valid(self):
        data = {
            "received": 0.1,
            "remains": 0,
            "order_id": 0,
            "funds": {
                "usd": 325,
                "btc": 2.498,
                "ltc": 0,
            }
        }
        info = TradeResult(**data)

        self.assertIsInstance(info.received, Decimal)
        self.assertEqual(info.received, Decimal(0.1))

        self.assertIsInstance(info.remains, Decimal)
        self.assertEqual(info.remains, Decimal(0))

        self.assertIsInstance(info.order_id, int)
        self.assertEqual(info.order_id, 0)

        self.assertIsInstance(info.funds, dict)
        self.assertEqual(info.funds, {"usd": 325, "btc": 2.498, "ltc": 0})


if __name__ == '__main__':
    unittest.main()
