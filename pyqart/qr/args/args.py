# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : All needed args to create a empty qr code.

from .mask import QrMask
from .version import QrVersion
from .rotation import QrRotation
from ..data import Raw, AlphaNumeric, Numbers
from ...common import Bits

__all__ = ['QrArgs']

_FORMAT_POLY = Bits(0x537, 11)
"""
  x^10 + x^8 + x^5 + x^4 + x^2 + x + 1
= 1    0  1 00 1     1   0 1    1   1
= 0101 0011 0111
= 0x573

Used when calculate format pattern data.
"""

_FORMAT_MASK_PATTERN = Bits(0x5412, 15)
"""
After all, format data should be xor with this mask pattern.
"""

_BC_ECCWCPB_TABLE = [
    [(1, 7), (1, 10), (1, 13), (1, 17)],
    [(1, 10), (1, 16), (1, 22), (1, 28)],
    [(1, 15), (1, 26), (2, 18), (2, 22)],
    [(1, 20), (2, 18), (2, 26), (4, 16)],
    [(1, 26), (2, 24), (4, 18), (4, 22)],
    [(2, 18), (4, 16), (4, 24), (4, 28)],
    [(2, 20), (4, 18), (6, 18), (5, 26)],
    [(2, 24), (4, 22), (6, 22), (6, 26)],
    [(2, 30), (5, 22), (8, 20), (8, 24)],
    [(4, 18), (5, 26), (8, 24), (8, 28)],
    [(4, 20), (5, 30), (8, 28), (11, 24)],
    [(4, 24), (8, 22), (10, 26), (11, 28)],
    [(4, 26), (9, 22), (12, 24), (16, 22)],
    [(4, 30), (9, 24), (16, 20), (16, 24)],
    [(6, 22), (10, 24), (12, 30), (18, 24)],
    [(6, 24), (10, 28), (17, 24), (16, 30)],
    [(6, 28), (11, 28), (16, 28), (19, 28)],
    [(6, 30), (13, 26), (18, 28), (21, 28)],
    [(7, 28), (14, 26), (21, 26), (25, 26)],
    [(8, 28), (16, 26), (20, 30), (25, 28)],
    [(8, 28), (17, 26), (23, 28), (25, 30)],
    [(9, 28), (17, 28), (23, 30), (34, 24)],
    [(9, 30), (18, 28), (25, 30), (30, 30)],
    [(10, 30), (20, 28), (27, 30), (32, 30)],
    [(12, 26), (21, 28), (29, 30), (35, 30)],
    [(12, 28), (23, 28), (34, 28), (37, 30)],
    [(12, 30), (25, 28), (34, 30), (40, 30)],
    [(13, 30), (26, 28), (35, 30), (42, 30)],
    [(14, 30), (28, 28), (38, 30), (45, 30)],
    [(15, 30), (29, 28), (40, 30), (48, 30)],
    [(16, 30), (31, 28), (43, 30), (51, 30)],
    [(17, 30), (33, 28), (45, 30), (54, 30)],
    [(18, 30), (35, 28), (48, 30), (57, 30)],
    [(19, 30), (37, 28), (51, 30), (60, 30)],
    [(19, 30), (38, 28), (53, 30), (63, 30)],
    [(20, 30), (40, 28), (56, 30), (66, 30)],
    [(21, 30), (43, 28), (59, 30), (70, 30)],
    [(22, 30), (45, 28), (62, 30), (74, 30)],
    [(24, 30), (47, 28), (65, 30), (77, 30)],
    [(25, 30), (49, 28), (68, 30), (81, 30)],
]
"""
Table of (block count, error correction codeword count per block).
Row by version, column by level.
"""


CCI_LENGTH_TABLE = {
    Raw: [(9, 8), (40, 16)],
    AlphaNumeric: [(9, 9), (26, 11), (40, 13)],
    Numbers: [(9, 10), (26, 12), (40, 14)]
}
"""
When data encoding, the Char Count Indicator value_upper table.

if version <= first_item, cci_length is second_item.
"""


class QrArgs(object):
    def __init__(self, version, level=0, mask=0, rotation=0):
        assert 0 <= level <= 3, "Level must between 0 and 3."
        self._version = QrVersion(version)
        self._mask = QrMask(mask)
        self._level = level
        self._rotation = QrRotation(rotation)

    @property
    def size(self):
        """
        :return: Width and height of QrCode.
        :rtype: int
        """
        return self._version.size

    @property
    def rotate_func(self):
        return self._rotation.rotate_func

    @property
    def align_start(self):
        """
        :return: See :any:`QrVersion.align_start`.
        :rtype: int
        """
        return self._version.align_start

    @property
    def align_step(self):
        """
        :return: See :any:`QrVersion.align_step`.
        :rtype: int
        """
        return self._version.align_step

    @property
    def version_pattern_value(self):
        """
        :return: See :any:`QrVersion.version_pattern_value`.
        :rtype: int
        """
        return self._version.version_pattern_value

    @property
    def version_number(self):
        """
        :return: See :any:`QrVersion.number`.
        :rtype: int
        """
        return self._version.number

    @property
    def level(self):
        """
        :return: See :any:`QrLevel.index`.
        :rtype: int
        """
        return self._level

    @property
    def mask_index(self):
        """
        :return: See :any:`QrMask.index`.
        :rtype: int
        """
        return self._mask.index

    @property
    def format_pattern_bits(self):
        """
        Format pattern has 15 bit,
        split to 3 parts: level, mask, error correction.

        It's structure like bellow:

        14 13 12 11 10 9 8 7 6 5 4 3 2 1 0

        Lv Lv M  M  M  C C C C C C C C C C

        Level part value table：

        ---- ----------- ---------
        name index value bit value
        ---- ----------- ---------
         L        00         01
         M        01         00
         H        10         11
         Q        11         10
        ---- ----------- ---------

        We can see: bit value = index value xor 01, 2 bit

        QrMask from 0(000) to 7(111), 3 bit

        Correction data is calculated by bch(15, 5), 10 bit

        :return: The format pattern value in a :any:`Bits` object.
        :rtype: Bits
        """
        # level
        bits = Bits(self.level ^ 0b01, 2)
        # mask
        bits.append(self.mask_index, 3)
        # ec
        bits.append(0, 10)
        ec = Bits.copy_from(bits)
        for i in range(5):
            if ec[i]:
                ec.xor(_FORMAT_POLY, i, 0)
        for i in range(5, 15):
            bits[i] = ec[i]
        # masking
        bits.xor(_FORMAT_MASK_PATTERN)
        return bits

    @property
    def bc(self):
        """
        :return: Block count.
        :rtype: int
        """
        return _BC_ECCWCPB_TABLE[self.version_number - 1][self.level][0]

    @property
    def eccwcpb(self):
        """
        :return: Error Correction CodeWord Count Per Block.
        :return: int
        """
        return _BC_ECCWCPB_TABLE[self.version_number - 1][self.level][1]

    @property
    def cwc(self):
        """
        :return: See :any:`QrVersion.cwc`.
        :rtype: int
        """
        return self._version.cwc

    @property
    def eccwc(self):
        """
        :return: Error Correction CodeWord Count
        :rtype: int
        """
        return self.eccwcpb * self.bc

    @property
    def dcwc(self):
        """
        :return: Data CodeWord Count.
        :rtype: int
        """
        return self.cwc - self.eccwc

    @property
    def ndcwcpb(self):
        """
        :return: Normal Data CodeWord Count Per Block.
        :rtype: int
        """
        return self.dcwc // self.bc

    @property
    def edcwc(self):
        """
        :return: Extra Data CodeWord Count.
        :rtype: int
        """
        return self.dcwc - self.ndcwcpb * self.bc

    def dcwcof(self, index):
        """
        :param int index: Block index.
        :return: Data CodeWord Count OF No.index block.
        :rtype: int
        """
        assert index < self.bc
        return self.ndcwcpb + (0 if index < (self.bc - self.edcwc) else 1)

    @property
    def should_invert(self):
        """
        :return: See :any:`QrMask.should_invert`.
        :rtype: callable
        """
        return self._mask.should_invert

    def cci_length_of(self, cls):
        for sep, value in CCI_LENGTH_TABLE[cls]:
            if self.version_number <= sep:
                return value
