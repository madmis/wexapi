import unittest
from decimal import Decimal
from wexapi.models import TransHistory


class TestTransHistory(unittest.TestCase):
    def test_create_valid(self):
        data = {
            "transaction_id": "1081672",
            "type": 1,
            "amount": 1.00000000,
            "currency": "BTC",
            "desc": "BTC Payment",
            "status": 2,
            "timestamp": 1342448420
        }
        info = TransHistory(**data)

        self.assertIsInstance(info.transaction_id, int)
        self.assertEqual(info.transaction_id, 1081672)

        self.assertIsInstance(info.type, int)
        self.assertEqual(info.type, 1)

        self.assertIsInstance(info.status, int)
        self.assertEqual(info.status, 2)

        self.assertIsInstance(info.timestamp, int)
        self.assertEqual(info.timestamp, 1342448420)

        self.assertIsInstance(info.currency, str)
        self.assertEqual(info.currency, "BTC")

        self.assertIsInstance(info.desc, str)
        self.assertEqual(info.desc, "BTC Payment")

        self.assertIsInstance(info.amount, Decimal)
        self.assertEqual(info.amount, Decimal(1.00000000))


if __name__ == '__main__':
    unittest.main()
