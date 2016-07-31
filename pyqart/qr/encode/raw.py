# Added at : 2016.7.28
# Author   : 7sDream
# Usage    : Raw data model, 8 bit for a byte.

from .base import BaseType
from .exception import QrDataInvalidException
from ...common import Bits

__all__ = ['Raw']


class Raw(BaseType):
    def __init__(self, data, cci_length):
        super().__init__(data, cci_length)

    @property
    def _encoded_data_part(self):
        bits = Bits()
        bits.extend(self.data)
        return bits

    @property
    def _mode_indicator(self):
        return 0b0100

    def _validate(self):
        for i, value in enumerate(self.data):
            if value < 0 or value > 255:
                raise QrDataInvalidException(
                    type(self).__name__,
                    self.data,
                    i,
                )

    @property
    def _encoded_data_part_length(self):
        return 8 * len(self.data)
