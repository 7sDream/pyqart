# Added at : 2016.7.30
# Author   : 7sDream
# Usage    : As a data set of (maybe) different data mode thad will be encoded.

from .raw import Raw
from .alphanumeric import AlphaNumeric
from .numbers import Numbers
from .exception import QrSpaceNotEnoughException
from ...common import BIT_PER_CW


class QrData(object):
    def __init__(self, string=None, ec_level=0):
        from ..args import QrArgs
        assert isinstance(string, str)
        assert 0 <= ec_level <= 3
        self._data_set = []
        self._ec_level = ec_level
        self._changed = False
        self._last = (1, QrArgs(1).dcwc * BIT_PER_CW, 0)

        if string is not None:
            self.put_string(string)

    @property
    def size(self):
        """
        :return: How many data item in object.
        :rtype: int
        """
        return len(self._data_set)

    @property
    def version_used_available(self):
        from ..args import QrArgs
        if self._changed is True:
            args = None
            used = 0
            for i in range(1, 41):
                args = QrArgs(i, self._ec_level)
                encode_list = [cls(data, args.cci_length_of(cls))
                               for cls, data in self._data_set]
                used = sum([x.needed_space for x in encode_list])
                available = args.dcwc * BIT_PER_CW - used
                if available >= 0:
                    self._last = (i, available, used)
                    self._changed = False
                    break
            else:
                raise QrSpaceNotEnoughException(
                    args.dcwc * BIT_PER_CW, used
                )
        return self._last

    @property
    def ec_level(self):
        return self._ec_level

    def set_level(self, level):
        assert 0 <= level <= 3
        if self._ec_level != level:
            self._ec_level = level
            self._changed = True

    def _common_put(self, data, cls):
        if len(self._data_set) > 0 and self._data_set[-1][0] is cls:
            old_data = self._data_set[-1][1]
            self._data_set[-1] = (cls, old_data + data)
        else:
            self._data_set.append((cls, data))
        self._changed = True

    def put_string(self, string):
        """
        Add string(utf-8) data to QrCode.

        :param str string: The string will be added.
        :return: A tuple: (if_success, exception).
        :rtype: (bool, QrException)
        :raise: QrDataInvalidException
        """
        return self._common_put(string.encode('utf-8'), Raw)

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
    def data_set(self):
        return tuple(self._data_set)
