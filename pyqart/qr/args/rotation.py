# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : QrRotation represent the rotate of QrCode:
#               0 for rotate 0 degrees clockwise, 1 for 90, 2 to 180, 3 for 270.

__all__ = ['QrRotation']

_ROTATE_FUNC_LIST = [
    None,
    lambda y, x, s: (x, s-y-1),
    lambda y, x, s: (s-y-1, s-x-1),
    lambda y, x, s: (s-x-1, y)
]


class QrRotation(object):
    def __init__(self, rotate_index):
        assert 0 <= rotate_index <= 3, "Rotation must between 0 and 3."
        self._index = rotate_index

    @property
    def index(self):
        return self._index

    @property
    def rotate_func(self):
        return _ROTATE_FUNC_LIST[self.index]
