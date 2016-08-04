# Added at : 2016.7.30
# Author   : 7sDream
# Usage    : A painter that draw paint data to canvas.

from random import randint

from .canvas import QrCanvas
from .exception import QrPainterException
from ..args import QrArgs
from ..data import QrData
from ..ec import RSEncoder
from ...common import Bits, BIT_PER_CW

__all__ = ['QrPainter']


class QrPainter(object):
    def __init__(self, data, version=None, mask=None, rotation=0):
        """
        :param QrData|str data: Data will be paint to QrCode.
        :param int version: Version of QrCode, 1 to 40,
            None means use the minimum version can encode the data you provided.
        :param int mask: The mask used in data and ec parts, from 0 to 7,
            None for random pick.
        :param int rotation: QrCode rotation direction, 0 for no rotation,
            1 for 90 degree clockwise, 2 for 180, 3 for 270.
        """
        assert isinstance(data, (QrData, str)), "Data must be str or QrData."
        if isinstance(data, str):
            data = QrData(data)
        if mask is None:
            mask = randint(0, 7)
        self._data = data
        self._version = version
        self._mask = mask
        self._rotation = rotation
        self._get_and_test_params()

    def _get_and_test_params(self):
        min_version, available, used = self._data.version_used_available
        if self._version is not None and self._version < min_version:
            raise QrPainterException(
                "The {} version QrCode does not have enough space to encode "
                "the data your provided, minimum version is {}.".format(
                    self._version, min_version,
                ))
        return min_version, available, used

    def get_params(self):
        min_version, available, used = self._get_and_test_params()
        if self._version is None:
            version = min_version
        else:
            version = self._version
            args = QrArgs(version, self._data.ec_level)
            encode_list = [cls(data, args.cci_length_of(cls))
                           for cls, data in self._data.data_set]
            used = sum([x.needed_space for x in encode_list])
            available = args.dcwc * BIT_PER_CW - used
        return QrArgs(version, self._data.ec_level, self._mask,
                      self._rotation), available, used

    @property
    def data_bits(self):
        if self._data.size == 0:
            raise QrPainterException("Unable to paint EMPTY DATA to canvas.")

        args, available, used = self.get_params()

        bits = Bits()

        # add encoded data
        for cls, data in self._data.data_set:
            encoding = cls(data, args.cci_length_of(cls))
            bits.extend(encoding.output)

        # ensure encoding process as expect
        assert bits.length == used

        bits.pad(available, used)

        # ensure fill all data zone
        assert bits.length == args.dcwc * BIT_PER_CW

        return bits

    @property
    def bits(self):
        """
        :rtype: Bits
        :raise: QrEncodingException: When encoding process error.
        """
        bits = self.data_bits
        args, _, _ = self.get_params()
        ec_bits = Bits()
        ec_length = args.eccwcpb
        di = 0
        for bi in range(args.bc):
            dcwc = args.dcwcof(bi)
            dbcob = dcwc * BIT_PER_CW
            block_data_bits = Bits.copy_from(bits, di, dbcob)
            ec_bits.extend(RSEncoder.encode(block_data_bits, ec_length))
            di += dbcob
        bits.extend(ec_bits)
        return bits

    @property
    def canvas(self):
        args, _, _ = self.get_params()
        canvas = QrCanvas(args)
        return canvas

    @property
    def as_bool_matrix(self):
        res = []
        canvas = self.canvas
        canvas.load_data(self.bits)
        for row in canvas.points:
            line = []
            for point in row:
                line.append(point.fill if not point.invert else not point.fill)
            res.append(line)
        return res
