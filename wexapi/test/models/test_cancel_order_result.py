import unittest
from wexapi.models import CancelOrderResult


class TestCancelOrderResult(unittest.TestCase):
    def test_create_valid(self):
        data = {
            "order_id": 5784,
            "funds": {
                "usd": 325,
                "btc": 2.498,
                "ltc": 0,
            }
        }
        info = CancelOrderResult(**data)

        self.assertIsInstance(info.order_id, int)
        self.assertEqual(info.order_id, 5784)

        self.assertIsInstance(info.funds, dict)
        self.assertEqual(info.funds, {"usd": 325, "btc": 2.498, "ltc": 0})


if __name__ == '__main__':
    unittest.main()
