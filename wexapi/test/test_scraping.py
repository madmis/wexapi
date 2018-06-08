from datetime import datetime
import unittest

import wexapi.common as common
import wexapi.public as api


class TestScraping(unittest.TestCase):

    def test_scrape_main_page(self):
        with common.WexConnection() as connection:
            info = api.InfoApi(connection)
            main_page = info.scrape_main_page()

            for message in main_page.messages:
                msg_id, user, time, text = message
                assert type(time) is datetime

                self.assertIs(type(msg_id), str)
                self.assertIs(type(user), str)
                self.assertIs(type(text), str)


if __name__ == '__main__':
    unittest.main()
