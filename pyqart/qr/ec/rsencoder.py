from .poly import GF28Poly
from ...common import Bits


class _RSGenPolynomials(object):
    def __init__(self):
        self._table = [None, GF28Poly.from_index_list([0, 0], 1)]

    def __getitem__(self, index):
        while index > len(self._table) - 1:
            c = len(self._table) - 1
            self._table.append(
                self._table[-1] * GF28Poly.from_index_list([0, c], 1))
        return self._table[index]


RSGenPolynomials = _RSGenPolynomials()


class RSEncoder(object):
    @classmethod
    def encode(cls, data, ec_length, need_bits=True):
        assert ec_length >= 0
        if ec_length == 0:
            return Bits()
        if not isinstance(data, list):
            data = data.as_int_list
        data_length = len(data)
        all_length = ec_length + data_length
        m = GF28Poly.from_value_list(
            data + [0] * ec_length,
            all_length - 1
        )
        g = RSGenPolynomials[ec_length]
        r = m % g
        res = r.as_int_list
        if len(res) < ec_length:
            res = [0] * (ec_length - len(res)) + res
        if need_bits:
            return Bits.copy_from(bytearray(res))
        else:
            return res

