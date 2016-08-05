# Added at : 2016.8.3
# Author   : 7sDream
# Usage    : A block of bits. In this class, we let each point (including EC)
#               as much as possible to meet the color of image in it's position.

from ..common import Bits, one_at, bit_at, BIT_PER_CW
from ..qr.ec import RSEncoder

__all__ = ['BitBlock']

_VS_CACHE = {}


def _copy(i):
    vs = []
    for line in _VS_CACHE[i]:
        vs.append([x for x in line])
    return vs


def _create_vs(dbc, ecbc):
    if dbc not in _VS_CACHE:
        print('can\'t find in cache, calculating...', end='', flush=True)
        vs = []
        for i in range(dbc):
            b = [0] * (i // 8) + [one_at(i % 8)] + [0] * (dbc // 8 - i // 8 - 1)
            b += RSEncoder.encode(b, ecbc // BIT_PER_CW, False)
            vs.append(b)
        print('Done')
        _VS_CACHE[dbc] = vs
    else:
        print('found in cache.')
    return _copy(dbc)


class BitBlock(object):
    def __init__(self, bits, di, dbc, eci, ecbc):
        self._dbc = dbc
        self._bits = Bits.copy_from(bits, di, dbc)
        self._bits.extend(bits, eci, ecbc)
        self._bits = self._bits.as_int_list

        # vector space
        self._vs = _create_vs(dbc, ecbc)

        self._locked_index = len(self._vs)
        self._already_set = set()
        self._max_index = len(self._bits) * 8

    def set(self, index, value):
        assert isinstance(index, int)
        assert isinstance(value, bool)
        assert 0 <= index < self._max_index

        if index in self._already_set:
            return False
        if len(self._already_set) >= self._dbc:
            return False

        found = False

        for i in range(self._locked_index):
            if bit_at(self._vs[i][index // 8], 8, index % 8) is False:
                continue
            if not found:
                found = True
                if i != 0:
                    self._exchange_row(0, i)
                continue
            self._vs_xor_line(i, 0)

        if not found:
            return False

        for i in range(self._locked_index, len(self._vs)):
            if bit_at(self._vs[i][index // 8], 8, index % 8) is True:
                self._vs_xor_line(i, 0)

        if bit_at(self._bits[index // 8], 8, index % 8) is not value:
            self._bits_xor_with_vs(0)

        self._exchange_row(0, self._locked_index - 1)
        self._locked_index -= 1
        self._already_set.add(index)

        return True

    def bits(self):
        return Bits.copy_from(bytearray(self._bits))

    def _vs_xor_line(self, i, j):
        self._vs[i] = [a ^ b for a, b in zip(self._vs[i], self._vs[j])]

    def _bits_xor_with_vs(self, i):
        self._bits = [a ^ b for a, b in zip(self._bits, self._vs[i])]

    def _exchange_row(self, i, j):
        self._vs[i], self._vs[j] = self._vs[j], self._vs[i]
