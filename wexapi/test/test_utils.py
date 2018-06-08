import decimal
import unittest

import wexapi.utils as utils


class TestParseResponse(unittest.TestCase):
    def test_parse_response(self):
        json = '{"test_bool": true, "test_int": 1, "test_dec": 1.560}'
        result = utils.parse_json_response(json)

        self.assertEqual(result['test_bool'], True)
        self.assertEqual(result['test_int'], decimal.Decimal('1'))
        self.assertEqual(result['test_dec'], decimal.Decimal('1.560'))

    def test_parse_json_response(self):
        json1 = """
                {"asks":[[3.29551,0.5],[3.29584,5]],
                "bids":[[3.29518,15.51461],[3,27.5]]}
                """
        parsed = utils.parse_json_response(json1)

        asks = parsed.get("asks")
        self.assertEqual(asks[0], [decimal.Decimal("3.29551"), decimal.Decimal("0.5")])
        self.assertEqual(asks[1], [decimal.Decimal("3.29584"), decimal.Decimal("5")])

        bids = parsed.get("bids")
        self.assertEqual(bids[0], [decimal.Decimal("3.29518"), decimal.Decimal("15.51461")])
        self.assertEqual(bids[1], [decimal.Decimal("3"), decimal.Decimal("27.5")])

    def test_parse_json_response_fail(self):
        json1 = """ \most /definitely *not ^json"""
        self.assertRaises(Exception, utils.parse_json_response, json1)


decimal.getcontext().rounding = decimal.ROUND_DOWN


class TestFormat(unittest.TestCase):
    def test_format_currency(self):
        self.assertEqual(utils.format_currency_digits(1.123456789, 1), "1.1")
        self.assertEqual(utils.format_currency_digits(1.123456789, 2), "1.12")
        self.assertEqual(utils.format_currency_digits(1.123456789, 3), "1.123")
        self.assertEqual(utils.format_currency_digits(1.123456789, 4), "1.1234")
        self.assertEqual(utils.format_currency_digits(1.123456789, 5), "1.12345")
        self.assertEqual(utils.format_currency_digits(1.123456789, 6), "1.123456")
        self.assertEqual(utils.format_currency_digits(1.123456789, 7), "1.1234567")

        self.assertEqual(utils.format_currency_digits(1.12, 3), "1.120")
        self.assertEqual(utils.format_currency_digits(44, 2), "44.00")

    def test_truncate_amount(self):
        self.assertEqual(utils.truncate_amount_digits(1.12, 1), decimal.Decimal('1.1'))
        self.assertEqual(utils.truncate_amount_digits(44.00, 2), decimal.Decimal('44.00'))
