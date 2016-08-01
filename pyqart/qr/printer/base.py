# Added at : 2016.7.31
# Author   : 7sDream
# Usage    : Base printer to visualize QrCode, define the function should be
#            implement by subclasses.

import abc

from ..painter import QrPainter
from ..data import QrData


class QrBasePrinter(object):
    def __init__(self):
        pass

    @classmethod
    def _create_painter(cls, obj):
        assert isinstance(obj, (QrPainter, QrData, str, bytes, bytearray))
        if isinstance(obj, QrData):
            obj = QrPainter(obj)
        elif isinstance(obj, str):
            obj = QrPainter(QrData(obj))
        elif isinstance(obj, (bytes, bytearray)):
            data = QrData()
            obj = data.put_bytes(obj)
            obj = QrPainter(obj)
        return obj

    @classmethod
    @abc.abstractmethod
    def print(cls, painter, *args, **kwargs):
        pass
