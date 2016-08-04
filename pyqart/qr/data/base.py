# Added at : 2016.7.28
# Author   : 7sDream
# Usage    : A base data mode class for encoding data to bytes.
#            All specific data model inherit from this class.

import abc

from ...common import Bits
from .exception import QrEncodingException

__all__ = ['BaseType']


class BaseType(object):
    def __init__(self, data, cci_length):
        """
        :param data: Data to be encoded
        :param int cci_length: value_upper of Char Count Indicator in bit
        """
        assert len(data) > 0, 'Unable to encode empty data.'
        self._data = data
        self._cci_length = cci_length
        self._validate()

    @property
    def data(self):
        """
        :return: provided, raw original data
        """
        return self._data

    @property
    @abc.abstractmethod
    def _encoded_data_part_length(self):
        return 0

    @property
    def needed_space(self):
        return 4 + self._cci_length + self._encoded_data_part_length

    @property
    @abc.abstractmethod
    def _mode_indicator(self):
        """
        :return: A 4-bit data to indicate what model is using,
            Use the lower 4 data.
        :rtype: int
        """
        pass

    @property
    def _char_count_indicator(self):
        """
        :return: Placed before encoded data to indicate data value_upper,
            it's own value_upper is decided by :any:`cci_length`.
        :rtype: Bits
        """
        bits = Bits()
        bits.append(0, self._cci_length - len(self.data).bit_length())
        bits.append(len(self.data), len(self.data).bit_length())
        return bits

    @abc.abstractmethod
    def _validate(self):
        """
        validate data, raise :any:`QrDataInvalidException`
        if data is invalid, implemented by subclasses.

        :raise: QrDataInvalidException
        """
        pass

    @property
    @abc.abstractmethod
    def _encoded_data_part(self):
        """
        encode data to bytes use specific model, implemented by subclasses.

        :return: encoded data
        :rtype: Bits
        """
        pass

    @property
    def output(self):
        """
        :return: Output encoded data.
        :rtype: Bits
        """
        bits = Bits()
        bits.append(self._mode_indicator, 4)
        bits.extend(self._char_count_indicator)
        bits.extend(self._encoded_data_part)
        if bits.length != self.needed_space:
            raise QrEncodingException(
                type(self), self.data,
                info="Encoded data value_upper does not match expectations.",
                exception=self.needed_space,
                actual=bits.length,
            )
        return bits

    def __str__(self):
        mi = Bits()
        mi.append(self._mode_indicator, 4)
        cci = Bits()
        cci.extend(self._char_count_indicator)
        encoded_data = Bits()
        encoded_data.extend(self._encoded_data_part)

        string = "{type} at {id:x}: " \
                 "{{data: {data}, mi: {mi}, cci: {cci}, encode: {code}}}"
        return string.format(
            type=type(self).__name__, id=id(self),
            data=self.data, mi=mi, cci=cci, code=encoded_data,
        )
