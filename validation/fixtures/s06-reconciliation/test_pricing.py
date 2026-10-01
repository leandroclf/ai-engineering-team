import unittest

import pricing
import rates


class PricingTest(unittest.TestCase):
    def setUp(self):
        rates.CALLS.clear()

    def test_total(self):
        self.assertEqual(pricing.quote_order([(10, "USD"), (10, "EUR")]), 21.0)

    def test_rate_change_between_quotes_is_seen(self):
        pricing.quote_order([(1, "EUR")])
        rates.RATES["EUR"] = 2.0
        try:
            self.assertEqual(pricing.quote_order([(1, "EUR")]), 2.0)
        finally:
            rates.RATES["EUR"] = 1.1


if __name__ == "__main__":
    unittest.main()
