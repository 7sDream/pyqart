# Added at  : 2016.07.31
# Author    : 7sDream
# Usage     : Provide math operator with polynomials on GF28.
#               Used in Reed-solomon encoder.

import abc

from .gf import GF28

__all__ = ['GF28Poly']


class _GFPoly(object):
    @classmethod
    @abc.abstractmethod
    def gf(cls):
        pass

    def __init__(self, pcmap):
        self._pcmap = pcmap
        if self._pcmap:
            self._max_index = max(self._pcmap.keys())
        else:
            self._max_index = 0

    @classmethod
    def from_index_list(cls, ilist, maxp):
        pcmap = {}
        for xi, ai in enumerate(ilist):
            if ai is None:
                continue
            pcmap[maxp - xi] = cls.gf()[ai]
        return cls(pcmap)

    @classmethod
    def from_value_list(cls, vlist, maxp):
        pcmap = {}
        for i, v in enumerate(vlist):
            if v == 0:
                continue
            pcmap[maxp - i] = cls.gf()[cls.gf().index(v)]
        return cls(pcmap)

    @property
    def pcmap(self):
        return self._pcmap

    @property
    def max_index(self):
        return self._max_index

    @property
    def as_int_list(self):
        int_list = []
        for p in reversed(range(self.max_index + 1)):
            if p in self.pcmap:
                int_list.append(self.pcmap[p].value)
            else:
                int_list.append(0)
        return int_list

    def __mul__(self, other):
        new_pcmap = {}
        for p1, c1 in self.pcmap.items():
            for p2, c2 in other.pcmap.items():
                if (p1 + p2) in new_pcmap:
                    old_value = new_pcmap[p1 + p2]
                    new_pcmap[p1 + p2] = old_value + c1 * c2
                else:
                    new_pcmap[p1 + p2] = c1 * c2
        return type(self)(new_pcmap)

    def __mod__(self, other):
        r = type(self)(self.pcmap)
        while r.max_index >= other.max_index:
            pad = r.max_index - other.max_index
            pad_item = type(self)({pad: r.pcmap[r.max_index]})
            r += other * pad_item
        return r

    def __add__(self, other):
        pcmap = {}
        for p in range(max(self.max_index, other.max_index) + 1):
            if p in self.pcmap:
                pcmap[p] = self.pcmap[p]
            if p in other.pcmap:
                if p in pcmap:
                    pcmap[p] += other.pcmap[p]
                else:
                    pcmap[p] = other.pcmap[p]
                if pcmap[p] is None:
                    del pcmap[p]
        return type(self)(pcmap)

    def __str__(self):
        pc_list = sorted(self.pcmap.items(), key=lambda x: x[0], reverse=True)
        strings = []
        for p, c in pc_list:
            if p == 0:
                item = str(c)
            elif p == 1:
                item = str(c) + 'x'
            else:
                item = str(c) + 'x^' + str(p)
            strings.append(item)
        return '+'.join(strings)

    def __repr__(self):
        return "Poly at {id}: {string}".format(id=id(self), string=str(self))


class GF28Poly(_GFPoly):
    @classmethod
    def gf(cls):
        return GF28
