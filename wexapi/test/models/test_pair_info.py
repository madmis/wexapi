import unittest
from decimal import Decimal
from wexapi.models import PairInfo


class TestPairInfo(unittest.TestCase):
    def test_create_valid(self):
        data = {
            "decimal_places": 3,
            "min_price": 0.1,
            "max_price": 400,
            "min_amount": 0.01,
            "hidden": 0,
            "fee": 0.2,
        }
        info = PairInfo(**data)

        self.assertIsInstance(info.decimal_places, int)
        self.assertEqual(info.decimal_places, 3)

        self.assertIsInstance(info.min_price, Decimal)
        self.assertEqual(info.min_price, Decimal(0.1))

        self.assertIsInstance(info.max_price, Decimal)
        self.assertEqual(info.max_price, Decimal(400))

        self.assertIsInstance(info.min_amount, Decimal)
        self.assertEqual(info.min_amount, Decimal(0.01))

        self.assertIsInstance(info.hidden, bool)
        self.assertEqual(info.hidden, False)

        self.assertIsInstance(info.fee, Decimal)
        self.assertEqual(info.fee, Decimal(0.2))


if __name__ == '__main__':
    unittest.main()
