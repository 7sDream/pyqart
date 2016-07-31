# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : QrLevel represent Error Correction Code Level of QrCode,
#            which has 4 level: L(1) M(2) H(3) Q(4).


class QrLevel(object):
    def __init__(self, level_index):
        assert 0 <= level_index <= 3
        self._index = level_index

    @property
    def index(self):
        return self._index
