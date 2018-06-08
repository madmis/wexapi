import os
import unittest

import wexapi.keyhandler as keyhandler
from wexapi.common import WexConnection
from wexapi.trade import TradeApi

# TODO: Add tests that run against a local server.

TEST_KEY_FILE = os.path.join(os.path.dirname(__file__), "test-keys.txt")

if os.path.isfile(TEST_KEY_FILE):
    class TestTrade(unittest.TestCase):
        def setUp(self):
            self.key_handler = keyhandler.KeyHandler(TEST_KEY_FILE)
            self.connection = WexConnection()

        def tearDown(self):
            self.connection.close()
            self.connection = None
            self.key_handler.close()

        def test_construction(self):
            keys = list(self.key_handler.keys)
            t = TradeApi(keys[0], self.key_handler, self.connection)

        def test_key_info(self):
            for key in self.key_handler.keys:
                t = TradeApi(key, self.key_handler, self.connection)
                r = t.get_info()

if __name__ == '__main__':
    unittest.main()
