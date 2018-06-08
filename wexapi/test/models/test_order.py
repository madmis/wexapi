import unittest
from decimal import Decimal
from wexapi.models import Order


class TestOrder(unittest.TestCase):
    def test_create_valid(self):
        data = {
            "order_id": "343152",
            "pair": "btc_usd",
            "type": "sell",
            "amount": 12.345,
            "rate": 485,
            "timestamp_created": 1342448420,
            "status": 0
        }
        info = Order(**data)

        self.assertIsInstance(info.order_id, int)
        self.assertEqual(info.order_id, 343152)

        self.assertIsInstance(info.pair, str)
        self.assertEqual(info.pair, "btc_usd")

        self.assertIsInstance(info.type, str)
        self.assertEqual(info.type, "sell")

        self.assertIsInstance(info.amount, Decimal)
        self.assertEqual(info.amount, Decimal(12.345))

        self.assertIsInstance(info.rate, Decimal)
        self.assertEqual(info.rate, Decimal(485))

        self.assertIsInstance(info.timestamp_created, int)
        self.assertEqual(info.timestamp_created, 1342448420)

        self.assertIsInstance(info.status, int)
        self.assertEqual(info.status, 0)


if __name__ == '__main__':
    unittest.main()
