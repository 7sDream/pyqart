import unittest

from pyqart.common.bit_funcs import one_at, zero_at, set_bit, bit_at


class TestBitUtils(unittest.TestCase):
    def test_one_at_normal(self):
        self.assertEqual(one_at(0), 0b10000000)
        self.assertEqual(one_at(3), 0b00010000)
        self.assertEqual(one_at(4), 0b00001000)
        self.assertEqual(one_at(7), 0b00000001)
        self.assertEqual(one_at(0, 12), 0b100000000000)
        self.assertEqual(one_at(5, 10), 0b0000010000)
        self.assertEqual(one_at(8, 10), 0b0000000010)

    def test_one_at_fail(self):
        with self.assertRaises(AssertionError):
            one_at(-1)
        with self.assertRaises(AssertionError):
            one_at(-2)
        with self.assertRaises(AssertionError):
            one_at(8)
        with self.assertRaises(AssertionError):
            one_at(10, 8)
        with self.assertRaises(AssertionError):
            one_at(10, 9)

    def test_zero_at_normal(self):
        self.assertEqual(zero_at(0), 0b01111111)
        self.assertEqual(zero_at(3), 0b11101111)
        self.assertEqual(zero_at(4), 0b11110111)
        self.assertEqual(zero_at(7), 0b11111110)
        self.assertEqual(zero_at(10, 12), 0b111111111101)
        self.assertEqual(zero_at(0, 12), 0b011111111111)
        self.assertEqual(zero_at(7, 8), 0b11111110)

    def test_zero_at_fail(self):
        with self.assertRaises(AssertionError):
            zero_at(-1)
        with self.assertRaises(AssertionError):
            zero_at(-2)
        with self.assertRaises(AssertionError):
            zero_at(8)
        with self.assertRaises(AssertionError):
            zero_at(10)
        with self.assertRaises(AssertionError):
            zero_at(10, 9)
        with self.assertRaises(AssertionError):
            zero_at(10, 10)

    def test_set_bit_normal(self):
        self.assertEqual(set_bit(0b01001010, 2, True), 0b01101010)
        self.assertEqual(set_bit(0b01001010, 6, False), 0b01001000)

    def test_set_bit_fail(self):
        with self.assertRaises(AssertionError):
            set_bit(0, -1, True)
        with self.assertRaises(AssertionError):
            set_bit(0, -2, True)
        with self.assertRaises(AssertionError):
            set_bit(0, 8, False)
        with self.assertRaises(AssertionError):
            set_bit(0, 9, False)

    def test_bit_at_normal(self):
        self.assertEqual(bit_at(0b01100, 5, 0), False)
        self.assertEqual(bit_at(0b01100, 5, 1), True)
        self.assertEqual(bit_at(0b101101, 6, 1), False)
        self.assertEqual(bit_at(0b101101, 6, 5), True)
        self.assertEqual(bit_at(0b11110111, 8, 4), False)
        self.assertEqual(bit_at(0b11110111, 8, 7), True)

    def test_bit_at_fail(self):
        # value_upper = 0
        with self.assertRaises(AssertionError):
            self.assertEqual(bit_at(0, 0, 0), False)
        # value_upper < 0
        with self.assertRaises(AssertionError):
            self.assertEqual(bit_at(0, -1, 0), False)
        with self.assertRaises(AssertionError):
            self.assertEqual(bit_at(0, -5, 0), False)
