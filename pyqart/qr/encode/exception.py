# Added at : 2016.7.28
# Author   : 7sDream
# Usage    : Exception when encode data is not invalid.

from ..exception import QrException

__all__ = ['QrDataInvalidException']


class QrDataInvalidException(QrException):
    def __init__(self, typename, invalid_data, index=None):
        self.typename = typename
        self.invalid_data = invalid_data
        self.index = index

    def __str__(self):
        string = "Invalid data \"{data}\" when build a {typename} data mode."
        if self.index is not None:
            string += " first invalid position is {number}."
        return string.format(
            data=self.invalid_data,
            typename=self.typename,
            index=self.index,
        )

    __repr__ = __str__


class QrEncodingException(QrException):
    def __init__(self, cls, data, **kwargs):
        self._cls = cls
        self._data = data
        self._kwargs = kwargs

    def __str__(self):
        string = "Error when encoding {cls}] type data [{data}]."
        if len(self._kwargs) > 0:
            string += 'Additional information: ' + str(self._kwargs)
