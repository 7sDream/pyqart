# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : Exception raised when drawing or add data to QrCode.

from ..exception import QrException

__all__ = ['QrCanvasException', 'QrSpaceNotEnoughException']


class QrCanvasException(QrException):
    pass


class QrSpaceNotEnoughException(QrException):
    def __init__(self, available, need):
        self._available = available
        self._needed = need

    def __str__(self):
        string = "There is not enough space to store the data provided, "
        string += "{available} data space available, data need {need} bit."
        return string.format(
            available=self._available,
            need=self._needed
        )

    __repr__ = __str__
