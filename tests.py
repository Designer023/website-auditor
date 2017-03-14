import unittest

from tools.validation import Validator


class ValidatorTestCase(unittest.TestCase):
    """Tests for `primes.py`."""

    def test_html_validates(self):
        """Test that HTML tests return an array of errors"""

        validator = Validator({})
        html = '<!doctype html><html lang="en"><head><body></body></html>'
        html_results = validator.validate_html(html)
        self.assertTrue(type(html_results) is list)


if __name__ == '__main__':
    unittest.main()
