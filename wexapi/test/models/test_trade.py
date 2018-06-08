import unittest
from decimal import Decimal
from wexapi.models import Trade


class TestTrade(unittest.TestCase):
    def test_create_valid(self):
        data = {
            "pair": "bch_btc",
            "type": "ask",
            "price": 103.6,
            "amount": 0.101,
            "tid": 4861261,
            "timestamp": 1370818007
        }
        info = Trade(**data)

        self.assertIsInstance(info.pair, str)
        self.assertEqual(info.pair, "bch_btc")

        self.assertIsInstance(info.type, str)
        self.assertEqual(info.type, "ask")

        self.assertIsInstance(info.price, Decimal)
        self.assertEqual(info.price, Decimal(103.6))

        self.assertIsInstance(info.amount, Decimal)
        self.assertEqual(info.amount, Decimal(0.101))

        self.assertIsInstance(info.tid, int)
        self.assertEqual(info.tid, 4861261)

        self.assertIsInstance(info.timestamp, int)
        self.assertEqual(info.timestamp, 1370818007)


if __name__ == '__main__':
    unittest.main()
