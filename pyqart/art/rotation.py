# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : QrRotation represent the rotate of QrCode:
#               0 for rotate 0 degrees clockwise, 1 for 90, 2 to 180, 3 for 270.

__all__ = ['QrRotation']


class QrRotation(object):
    def __init__(self, rotate_number):
        assert 0 <= rotate_number <= 3
        self._num = rotate_number
