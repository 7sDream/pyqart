# Added at : 2016.7.30
# Author   : 7sDream
# Usage    : A painter that draw paint data to canvas.


from .canvas import QrCanvas
from .exception import QrPainterException
from ..args import QrArgs
from ..ec import RSEncoder
from ..data import QrData
from ...common import Bits

__all__ = ['QrPainter']

_BIT_PER_CW = 8

_PADDING_BITS = 0b1110110000010001
"""
padding with those data when data not fill data zone
"""


class QrPainter(object):
    def __init__(self, data, version=None, mask=0):
        """
        :param QrData data: Data will be paint to QrCode.
        :param int version: Version of QrCode, 1 to 40,
            None means use the minimum version can encode the data you provided.
        :param int mask: The mask used in data and ec parts, from 0 to 7.
        """
        assert isinstance(data, QrData)
        if version is not None:
            assert 0 < version <= 40
        assert 0 <= mask <= 7
        self._data = data
        self._version = version
        self._mask = mask
        self._test_version()

    def _test_version(self):
        min_version, _, _ = self._data.version_used_available
        if self._version is not None and self._version < min_version:
            raise QrPainterException(
                "The {} version QrCode does not have enough space to encode "
                "the data your provided, minimum version is {}.".format(
                    self._version, min_version,
                ))

    @property
    def data_bits(self):
        args, available, used = self._get_params()

        bits = Bits()

        # add encoded data
        encoding_set = []
        for encode_cls, data in self._data.data_set:
            encoding = encode_cls(data, args.cci_length_of(encode_cls))
            bits.extend(encoding.output)
            encoding_set.append(encoding)

        # ensure encoding process as expect
        assert bits.length == used

        # add terminator
        bits.append(0, min(available, 4))

        # add more 0s to make last several data to a codeword
        if bits.length % _BIT_PER_CW != 0:
            bits.append(0, _BIT_PER_CW - bits.length % _BIT_PER_CW)

        # add pad bytes if the data is still too few
        available = args.dcwc * _BIT_PER_CW - bits.length
        while available > 0:
            bits.append(_PADDING_BITS, min(available, 16))
            available -= 16

        # ensure fill all data zone
        assert bits.length == args.dcwc * _BIT_PER_CW

        return bits

    def _get_params(self):
        # test version
        min_version, used, available = self._data.version_used_available
        self._test_version()
        if self._version is None:
            version = min_version
        else:
            version = self._version
        args = QrArgs(version, self._data.ec_level, self._mask)
        return args, available, used

    @property
    def bits(self):
        """
        :rtype: Bits
        :raise: QrEncodingException: When encoding process error.
        """
        bits = self.data_bits
        args, _, _ = self._get_params()
        ec_bits = Bits()
        ec_length = args.eccwcpb
        di = 0
        for bi in range(args.bc):
            dcwc = args.dcwcof(bi)
            dbcob = dcwc * _BIT_PER_CW
            block_data_bits = Bits.copy_from(bits, di, dbcob)
            ec_bits.extend(RSEncoder.encode(block_data_bits, ec_length))
            di += dbcob
        bits.extend(ec_bits)
        return bits

    @property
    def as_canvas(self):
        args, _, _ = self._get_params()
        buff_canvas = QrCanvas(args)
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
