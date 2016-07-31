# Added at : 2016.7.30
# Author   : 7sDream
# Usage    : A painter that draw paint data to canvas.

from copy import deepcopy

from .canvas import QrCanvas
from .exception import QrSpaceNotEnoughException
from ..encode import Raw, AlphaNumeric, Numbers, QrDataInvalidException
from ..ec import RSEncoder
from ...common import Bits

__all__ = ['QrPainter']

_BIT_PER_CW = 8

_PADDING_BITS = 0b1110110000010001
"""
padding with those data when data not fill data zone
"""


class QrPainter(object):
    def __init__(self, args):
        self._canvas = QrCanvas(args)
        self._encoding_list = []

    @property
    def _used_bit(self):
        return sum([data.needed_space for data in self._encoding_list])

    @property
    def _available_bit(self):
        return self._canvas.args.dcwc * _BIT_PER_CW - self._used_bit

    def _common_put(self, data, cls):
        try:
            encode = cls(data, self._canvas.args.cci_length_of(cls))
            if encode.needed_space > self._available_bit:
                return False, QrSpaceNotEnoughException(
                    self._available_bit, encode.needed_space
                )
            self._encoding_list.append(encode)
            return True, None
        except QrDataInvalidException as e:
            return False, e

    def put_string(self, string):
        """
        Add string(utf-8) data to QrCode.

        :param str string: The string will be added.
        :return: A tuple: (if_success, exception).
        :rtype: (bool, QrException)
        :raise: QrDataInvalidException
        """
        return self._common_put(string.encode('latin-1'), Raw)

    def put_bytes(self, data):
        """
        Add raw bytes data to QrCode.

        :see-also:: :any:`put_string` for return and exception info.
        """
        return self._common_put(data, Raw)

    def put_numbers(self, numbers):
        """
        Add numbers data to QrCode.

        :see-also:: :any:`put_string` for return and exception info.

        :param int|str numbers: The number will be added,
            0 start at string type numbers will be preserved.
        """
        return self._common_put(numbers, Numbers)

    def put_alpha_numeric(self, string):
        """
        Add numbers, big letters, and some special symbol data to QrCode.

        :see-also:: :any:`put_string` for return and exception info.

        :param str string: The data will be added.
        """
        return self._common_put(string, AlphaNumeric)

    @property
    def data_bits(self):
        bits = Bits()

        # add encoded data
        for encoding in self._encoding_list:
            bits.extend(encoding.output)

        # add terminator
        bits.append(0, min(self._available_bit, 4))

        # add more 0s to make last several data to a codeword
        if bits.length % _BIT_PER_CW != 0:
            bits.append(0, _BIT_PER_CW - bits.length % _BIT_PER_CW)

        # add pad bytes if the data is still too few
        available = self._canvas.args.dcwc * _BIT_PER_CW - bits.length
        while available > 0:
            bits.append(_PADDING_BITS, min(available, 16))
            available -= 16

        # ensure fill all data zone
        assert bits.length == self._canvas.args.dcwc * _BIT_PER_CW

        return bits

    @property
    def bits(self):
        """
        :rtype: Bits
        :raise: QrEncodingException: When encoding process error.
        """
        bits = self.data_bits
        ec_bits = Bits()
        ec_length = self._canvas.args.eccwcpb
        di = 0
        for bi in range(self._canvas.args.bc):
            dcwc = self._canvas.args.dcwcof(bi)
            dbcob = dcwc * _BIT_PER_CW
            block_data_bits = Bits.copy_from(bits, di, dbcob)
            ec_bits.extend(RSEncoder.encode(block_data_bits, ec_length))
            di += dbcob
        bits.extend(ec_bits)
        return bits

    @property
    def as_canvas(self):
        buff_canvas = QrCanvas(self._canvas.args)
        buff_canvas.load_data(self.bits)
        return buff_canvas

    @property
    def as_bool_matrix(self):
        res = []
        buff_canvas = self.as_canvas
        for row in buff_canvas.points:
            line = []
            for point in row:
                line.append(point.fill if not point.invert else not point.fill)
            res.append(line)
        return res
