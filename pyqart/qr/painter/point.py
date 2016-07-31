# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : QrPoint represent a point of QrCode, can be 9 type(except UNKNOWN).
#            Enum class QrPointType used to stand for those type.
#            The UNKNOWN type only be used to init the point which means
#            the type of point is temporarily unknown.

from enum import Enum, unique

__all__ = ['QrPointType', 'QrPoint']


@unique
class QrPointType(Enum):
    UNKNOWN = 0
    POSITION = 1
    ALIGNMENT = 2
    TIMING = 3
    FORMAT = 4
    VERSION_PATTERN = 5
    UNUSED = 6
    DATA = 7
    CORRECTION = 8
    EXTRA = 9


class QrPoint(object):
    def __init__(self, fill, type_=QrPointType.UNKNOWN, offset=-1,
                 invert=False):
        self.fill = fill
        self.type = type_
        self.offset = offset
        self.invert = invert
