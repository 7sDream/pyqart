# Added at : 2016.7.28
# Author   : 7sDream
# Usage    : Numbers data model, 10 bit for 3 numbers.

from .base import BaseType
from ...common import Bits
from .exception import QrDataInvalidException


class Numbers(BaseType):
    def __init__(self, data, cci_length):
        super().__init__(data, cci_length)

    def _validate(self):
        for i, value in enumerate(self.data):
            if not ord('0') <= ord(value) <= ord('9'):
                raise QrDataInvalidException(
                    type(self).__name__, self.data, i)

    @property
    def _encoded_data_part(self):
        bits = Bits()
        split = (self.data[x:x + 3] for x in range(0, len(self.data), 3))
        for i, string in enumerate(split):
            bits.append(int(string), 1 + 3 * len(string))
        return bits

    @property
    def _mode_indicator(self):
        return 0b0001

    @property
    def _encoded_data_part_length(self):
        return 10 * (len(self.data) // 3) + [0, 4, 7][len(self.data) % 3]
