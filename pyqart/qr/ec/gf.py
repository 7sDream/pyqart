# Added at : 2016.7.31
# Author   : 7sDream
# Usage    : Calculate GF(2^m) and all it's item a^n

from ...common import bit_at

__all__ = ['GF28']

_MUL_CACHE = {}
_ADD_CACHE = {}


class _GF2M(object):
    def __init__(self, m, px):
        self._m = m
        self._px = px % self.value_upper
        self._table, self._rev_table = self.calc()

    @property
    def value_upper(self):
        return 2 ** self._m

    @property
    def index_upper(self):
        return self.value_upper

    def calc(self):
        table = []
        rev_table = [None] * self.value_upper
        for x in range(self.index_upper):
            if x < self._m:
                value = 1 << x
            elif x == self._m:
                value = self._px
            elif not bit_at(table[-1], self._m, 0):
                value = (table[-1] << 1) % self.value_upper
            else:
                value = (table[-1] << 1 ^ self._px) % self.value_upper
            table.append(value)
            try:
                rev_table[value] = x
            except Exception as e:
                print(value)
                raise e
        table.append(1)
        return table, rev_table

    def index(self, value):
        return self._rev_table[value]

    def __getitem__(self, index):
        return _GFItem(self, index, self._table[index])


class _GFItem(object):
    def __init__(self, gf, index, value):
        self._gf = gf
        self._index = index
        self._value = value

    @property
    def gf(self):
        return self._gf

    @property
    def index(self):
        return self._index

    @property
    def value(self):
        return self._value

    def __add__(self, other):
        cache_index = (self.gf, self.index, other.index)
        if cache_index not in _ADD_CACHE:
            value = self._value ^ other.value
            if value == 0:
                return None
            item = _GFItem(self.gf, self.gf.index(value), value)
            _ADD_CACHE[cache_index] = item
        else:
            item = _ADD_CACHE[cache_index]
        return item

    def __mul__(self, other):
        cache_index = (self.gf, self.index, other.index)
        if cache_index not in _MUL_CACHE:
            index = self.index + other.index
            index = index % self.gf.value_upper + int(index // self.gf.value_upper)
            item = self.gf[index]
            _MUL_CACHE[cache_index] = item
        else:
            item = _MUL_CACHE[cache_index]
        return item

    def __str__(self):
        return "a" + str(self.index)


GF28 = _GF2M(8, 0b100011101)
