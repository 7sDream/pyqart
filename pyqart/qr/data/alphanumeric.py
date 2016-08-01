# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : Data mode that used to encode
#            big alpha (A-Z)
#            and numeric (0-9)
#            and some special symbols (space, $, %, *, +, -, ., /, :).

from .exception import QrDataInvalidException
from .base import BaseType
from ...common import Bits

__all__ = ['AlphaNumeric']

_ALPHA_NUMERIC_TABLE = {
    ''.join([chr(c) for c in range(ord('0'), ord('9') + 1)]):
        lambda c: int(c),
    ''.join([chr(c) for c in range(ord('A'), ord('Z') + 1)]):
        lambda c: ord(c) - ord('A') + 10,
    ' $%*+-./:':
        lambda c: ' $%*+-./:'.index(c) + 36
}

_DOMAIN = ''
for key in _ALPHA_NUMERIC_TABLE.keys():
    _DOMAIN += key


class AlphaNumeric(BaseType):
    def __init__(self, data, cci_length):
        super().__init__(data, cci_length)

    @property
    def _mode_indicator(self):
        return 0b0010

    def _validate(self):
        for i, v in enumerate(self.data):
            if v not in _DOMAIN:
                raise QrDataInvalidException(
                    type(self).__name__,
                    self.data,
                    i,
                )

    @property
    def _encoded_data_part(self):
        bits = Bits()
        for i in range(0, len(self.data), 2):
            part = self.data[i:i + 2]
            if len(part) == 2:
                a, b = tuple(part)
                length = 11
            else:
                a, b = part[0], None
                length = 6
            bits.append(self._calc_number(a, b), length)
        return bits

    @staticmethod
    def _calc_number(a, b=None):
        number1 = number2 = -1
        for k, func in _ALPHA_NUMERIC_TABLE.items():
            if a in k:
                number1 = func(a)
            if b is not None and b in k:
                number2 = func(b)
        if b is None:
            return number1
        else:
            return number1 * 45 + number2

    @property
    def _encoded_data_part_length(self):
        return 11 * (len(self.data) // 2) + 6 * (len(self.data) % 2)
