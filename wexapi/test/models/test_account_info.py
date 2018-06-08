import unittest
from wexapi.models import AccountInfo


class TestAccountInfo(unittest.TestCase):
    def test_create_valid(self):
        data = {
            "funds": {
                "usd": 325,
                "btc": 23.998,
                "ltc": 0,
            },
            "open_orders": 2,
            "transaction_count": 34,
            "server_time": 1370818007,
            "rights": {
                "info": 1,
                "trade": 0,
                "withdraw": 0
            },
        }
        info = AccountInfo(**data)

        self.assertIsInstance(info.funds, dict)
        self.assertEqual(info.funds, {"usd": 325, "btc": 23.998, "ltc": 0})

        self.assertIsInstance(info.open_orders, int)
        self.assertEqual(info.open_orders, 2)

        self.assertIsInstance(info.transaction_count, int)
        self.assertEqual(info.transaction_count, 34)

        self.assertIsInstance(info.server_time, int)
        self.assertEqual(info.server_time, 1370818007)

        self.assertIsInstance(info.info_rights, bool)
        self.assertTrue(info.info_rights)

        self.assertIsInstance(info.withdraw_rights, bool)
        self.assertFalse(info.withdraw_rights)

        self.assertIsInstance(info.trade_rights, bool)
        self.assertFalse(info.trade_rights)


if __name__ == '__main__':
    unittest.main()
