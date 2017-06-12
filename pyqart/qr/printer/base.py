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
        assert isinstance(
            obj,
            (QrPainter, QrData, str, bytes, bytearray)
        ), "Argument must be QrPainter, QrData, str, bytes or bytearray"
        if isinstance(obj, QrData):
            obj = QrPainter(obj)
        elif isinstance(obj, str):
            obj = QrPainter(QrData(obj))
        elif isinstance(obj, (bytes, bytearray)):
            data = QrData()
            obj = data.put_bytes(obj)
            obj = QrPainter(obj)
        return obj

    @abc.abstractmethod
    def print(self, *args, **kwargs):
        pass
