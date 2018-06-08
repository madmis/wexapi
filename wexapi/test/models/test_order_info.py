import unittest
from decimal import Decimal
from wexapi.models import OrderInfo


class TestOrderInfo(unittest.TestCase):
    def test_create_valid(self):
        data = {
            "order_id": "343152",
            "pair": "btc_usd",
            "type": "sell",
            "start_amount": 13.345,
            "amount": 12.345,
            "rate": 485,
            "timestamp_created": 1342448420,
            "status": 0
        }
        info = OrderInfo(**data)

        self.assertIsInstance(info.start_amount, Decimal)
        self.assertEqual(info.start_amount, Decimal(13.345))


if __name__ == '__main__':
    unittest.main()
