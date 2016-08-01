import unittest

from pyqart.qr.data.numbers import Numbers


class TestNumbers(unittest.TestCase):
    def test_numbers_length_mod_3_is_0(self):
        numbers = Numbers('923576', 10)
        self.assertEqual(
            numbers.output.as_string,
            '0001' + '0000000110' +
            '1110011011' + '1001000000',
        )

    def test_numbers_length_mod_3_is_1(self):
        numbers = Numbers('0123456789012345', 10)
        self.assertEqual(
            numbers.output.as_string,
            '0001' + '0000010000' +
            '0000001100' + '0101011001' + '1010100110' +
            '1110000101' + '0011101010' + '0101',
        )

    def test_numbers_length_mod_3_is_2(self):
        numbers = Numbers('01234567', 10)
        self.assertEqual(
            numbers.output.as_string,
            '0001' + '0000001000' + '000000110001010110011000011',
        )