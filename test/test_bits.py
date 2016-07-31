import unittest

from pyqart.common.bits import Bits


class TestBits(unittest.TestCase):
    def test_bits_as_string_when_no_data(self):
        b = Bits()
        self.assertEqual(b.as_string, '')

    def test_bits_as_string_when_has_data(self):
        b = Bits()
        b.append(0b11010011, 8)
        self.assertEqual(b.as_string, '11010011')
        b.append(0b1000, 4)
        self.assertEqual(b.as_string, '110100111000')

    def test_bits_as_int_when_no_data(self):
        b = Bits()
        self.assertEqual(b.as_int, -1)

    def test_bits_as_int_when_less_than_a_byte(self):
        b = Bits()
        b.append(1, 1)
        self.assertEqual(b.as_int, 1)

    def test_bits_as_int_when_between_one_and_two_byte(self):
        b = Bits()
        b.append(0b111100111, 9)
        self.assertEqual(b.as_int, 0b111100111)

    def test_bits_append_bit(self):
        b = Bits()
        b.append_bit(True)
        b.append_bit(True)
        b.append_bit(False)
        b.append_bit(False)
        self.assertEqual(b.as_int, 0b1100)
        b.append_bit(True)
        b.append_bit(False)
        b.append_bit(False)
        b.append_bit(False)
        self.assertEqual(b.as_int, 0b11001000)

    def test_bits_append(self):
        b = Bits()
        b.append(0xAC, 8)
        self.assertEqual(b.as_int, 0xAC)
        b.append(0xF, 4)
        self.assertEqual(b.as_int, 0x0ACF)

    def test_bits_extend_all(self):
        b = Bits()
        b.extend(b'\xAC')
        self.assertEqual(b.as_int, 0xAC)
        b.extend(bytearray(b'\x1F'))
        self.assertEqual(b.as_int, 0x0AC1F)

    def test_bits_extend_other_bits_all(self):
        b = Bits()
        b.extend(b'\xAC')
        other_bits = Bits.copy_from(b)
        b.extend(other_bits)
        self.assertEqual(b.as_int, 0xACAC)

    def test_bits_extend_other_bytes_0_to_not_end(self):
        b = Bits()
        b.extend(b'\x0F', count=6)
        self.assertEqual(b.as_int, 3)

    def test_bits_extend_other_bytes_not_start_to_end(self):
        b = Bits()
        b.extend(b'\x0F', 4)
        self.assertEqual(b.as_int, 15)

    def test_bits_extend_other_bytes_not_start_to_not_end(self):
        b = Bits()
        b.extend(b'\x0F', 4, 2)
        self.assertEqual(b.as_int, 3)

    def test_bits_xor(self):
        b = Bits(0b001010001, 9)
        o = Bits(0b0010110, 7)
        b.xor(o, 2, 3, 3)
        self.assertEqual(b.as_string, '001100001')

        b = Bits(0b001010001, 9)
        o = Bits(0b0010110, 7)
        b.xor(o, 2, 3)
        self.assertEqual(b.as_string, '001100001')
