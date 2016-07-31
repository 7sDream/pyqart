# Added at : 2016.7.31
# Author   : 7sDream
# Usage    : Base printer to visualize QrCode, define the function should be
#            implement by subclasses.

import abc


class BasePrinter(object):
    def __init__(self):
        pass

    @classmethod
    @abc.abstractmethod
    def print(cls, painter, *args, **kwargs):
        pass
