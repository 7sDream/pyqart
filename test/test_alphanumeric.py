import unittest

from pyqart.qr.data.alphanumeric import AlphaNumeric


class TestAlphaNumeric(unittest.TestCase):
    def test_alphanumeric_odd(self):
        an = AlphaNumeric('AC-42', 9)
        self.assertEqual(
            an.output.as_string,
            '0010' + '000000101' +
            '00111001110' + '11100111001' + '000010'
        )

    def test_alphanumeric_even(self):
        an = AlphaNumeric('7S DREAM', 9)
        self.assertEqual(
            an.output.as_string,
            '0010' + '000001000' +
            '00101010111' + '11001100001' + '10011001101' + '00111011000'
        )
