# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : Exception raised when drawing or add data to QrCode.

from ..exception import QrException

__all__ = ['QrCanvasException', 'QrPainterException']


class QrCanvasException(QrException):
    pass


class QrPainterException(QrException):
    pass
