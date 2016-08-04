# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : QrMask represent data part mask of QrCode,
#            which changes which modules are dark and which are light
#            according to a particular rule.
#            The purpose of this step is to modify the QR code to make it
#            as easy for a QR code reader to scan as possible.
#            There are only 8 mask pattern can be used.

__all__ = ['QrMask']

_FUNCTION_LIST = [
    lambda y, x: (x + y) % 2 == 0,
    lambda y, x: y % 2 == 0,
    lambda y, x: x % 3 == 0,
    lambda y, x: (x + y) % 3 == 0,
    lambda y, x: (y // 2 + x // 3) % 2 == 0,
    lambda y, x: x * y % 2 + x * y % 3 == 0,
    lambda y, x: (x * y % 2 + x * y % 3) % 2 == 0,
    lambda y, x: ((x + y) % 2 + (x * y) % 3) % 2 == 0,
]
"""
The mask function table.
"""


class QrMask(object):
    def __init__(self, mask_index):
        assert 0 <= mask_index <= 7, "Mask must between 0 and 7"
        self._index = mask_index

    @property
    def index(self):
        """
        :return: Mask index, from 0 to 7, specific the mask pattern.
        :rtype: int
        """
        return self._index

    @property
    def should_invert(self):
        """
        :return: A function accept (y, x) to decide if point should invert.
        :rtype: callable
        """
        return _FUNCTION_LIST[self.index]
