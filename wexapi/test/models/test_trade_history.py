import unittest
from decimal import Decimal
from wexapi.models import TradeHistory


class TestTradeHistory(unittest.TestCase):
    def test_create_valid(self):
        data = {
            "transaction_id": "1081672",
            "pair": "btc_usd",
            "type": "sell",
            "amount": 1,
            "rate": 450,
            "order_id": 343148,
            "is_your_order": 1,
            "timestamp": 1342445793,
        }
        info = TradeHistory(**data)

        self.assertIsInstance(info.transaction_id, int)
        self.assertEqual(info.transaction_id, 1081672)

        self.assertIsInstance(info.pair, str)
        self.assertEqual(info.pair, "btc_usd")

        self.assertIsInstance(info.type, str)
        self.assertEqual(info.type, "sell")

        self.assertIsInstance(info.amount, Decimal)
        self.assertEqual(info.amount, Decimal(1))

        self.assertIsInstance(info.rate, Decimal)
        self.assertEqual(info.rate, Decimal(450))

        self.assertIsInstance(info.order_id, int)
        self.assertEqual(info.order_id, 343148)

        self.assertIsInstance(info.is_your_order, bool)
        self.assertTrue(info.is_your_order)

        self.assertIsInstance(info.timestamp, int)
        self.assertEqual(info.timestamp, 1342445793)


if __name__ == '__main__':
    unittest.main()
