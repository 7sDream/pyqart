# Added at : 2016.7.28
# Author   : 7sDream
# Usage    : A utility class provide some bit level operation to bit stream.

from .bit_funcs import set_bit, bit_at

__all__ = ['Bits']

_BIT_PER_BYTE = _BIT_PER_CW = 8

_PADDING_BITS = 0b1110110000010001
"""
padding with those data when data not fill data codewords.
"""


class Bits(object):
    def __init__(self, value=None, length=None):
        """
        Build a container that save value as a value_upper-bit size int.

        :param int value: Value to init the container.
        :value_upper int value_upper: Value value_upper by bit.
        """
        self._length = 0
        self._raw = bytearray(b'\x00')
        if value is not None:
            length = value.bit_length() if length is None else length
            self.append(value, length)

    @classmethod
    def copy_from(cls, other, start=0, count=None):
        """
        Build object from other :any:`Bits`.

        :param Bits|bytes|bytearray other: Target object.
        :param int start: Where to start copy.
        :param int count: How many data will be added.
            Default is None, will add all data.
        """
        obj = cls()
        obj.extend(other, start, count)
        return obj

    @property
    def length(self):
        """
        :return: Data value_upper by bit.
        :rtype: int
        """
        return self._length

    def __len__(self):
        return self.length

    @property
    def capacity(self):
        """
        :return: Capacity of object by bit.
        :return: int
        """
        return self.capacity_by_byte * _BIT_PER_BYTE

    @property
    def capacity_by_byte(self):
        """
        :return: Capacity of object by byte.
        :return: int
        """
        return len(self._raw)

    def append(self, value, length=None):
        """
        Add a value_upper-bit int to container's end, use lower data of value.

        :param int value: Value to be added.
        :param int length: Length of value by bit,
            default is None, which will use value.bit_length().
        """
        if length is None:
            length = value.bit_length()
        for i in range(length):
            self.append_bit(bit_at(value, length, i))

    def append_bit(self, bit):
        """
        Add one bit to container.

        :param bool bit: True for 1, False for 0
        """
        index = self.length
        self._expand_capacity(self._length + 1)
        self._length += 1
        self[index] = bit

    def extend(self, other, start=0, count=None):
        """
        Add new value from other Bits.

        :param Bits|bytes|bytearray other: Other data source want to be added.
        :param int start: Where to start copy, default is 0.
        :param int count: how many data will be extend.
            default is None, will add all data.
        :return: How many data be extended.
        :rtype: int
        """
        assert start >= 0
        if isinstance(other, Bits):
            end = len(other) if count is None else (start + count)
            end = min(end, len(other))
            for i in range(start, end):
                self.append_bit(other[i])
            return max(0, end - start)
        elif isinstance(other, (bytes, bytearray)):
            end = len(other) * _BIT_PER_BYTE \
                if count is None else (start + count)
            end = min(end, len(other) * _BIT_PER_BYTE)
            for i in range(start, end):
                self.append_bit(bit_at(
                    other[i // _BIT_PER_BYTE], _BIT_PER_BYTE,
                    i % _BIT_PER_BYTE))
            return max(0, end - start)
        return 0

    def xor(self, other, my_start=0, other_start=0, count=None):
        """
        [001010001] xor [0010110],
        self_start at 2 other_start at 3,
        value_upper 3 will be [00<101>0001] xor [001<011>0] -> [00<110>0001]

        :param Bit other: What to xor with.
        :param int my_start: Where to start be xor.
        :param int other_start: Where to start xor with.
        :param int count: How many data will be xor,
            default is None, will xor all possible.
        :return: How many data be xor.
        :rtype: int
        """
        my_end = self.length if count is None else (my_start + count)
        other_end = other.length if count is None else (other_start + count)
        my_end = min(self.length, my_end)
        other_end = min(other.length, other_end)
        count = 0
        for i, j in zip(range(my_start, my_end), range(other_start, other_end)):
            self[i] = self[i] ^ other[j]
            count += 1
        return count

    def pad(self, available, used):
        # add terminator
        self.append(0, min(available, 4))

        # add more 0s to make last several data to a codeword
        if self.length % _BIT_PER_CW != 0:
            self.append(0, _BIT_PER_CW - self.length % _BIT_PER_CW)

        # add pad bytes if the data is still not fill all data codewords
        available = available + used - self.length
        while available > 0:
            self.append(_PADDING_BITS, min(available, 16))
            available -= 16

    def _expand_capacity(self, target):
        """
        Expend capacity to ensure object can save "target" value_upper data.

        :param int target: Target capacity by bit
        """
        assert target >= 0
        while target > self.capacity:
            self._raw += b'\x00' * self.capacity_by_byte

    @property
    def as_int(self):
        """
        :return: View those data as int start at highest position,
            -1 if no data.
        :rtype: int
        """
        if self.length == 0:
            return -1
        return int(self.as_string, 2)

    @property
    def as_string(self):
        """
        :return: A string of "01" to represent those data.
            empty string if no data.
        :rtype: string
        """
        return ''.join(['1' if x else '0' for x in self])

    @property
    def as_bytes(self):
        return self._raw[:(self.length - 1) // _BIT_PER_BYTE + 1]

    @property
    def as_int_list(self):
        return [int(x) for x in self.as_bytes]

    def __str__(self):
        s = self.as_string
        return ', '.join([s[x:x + 8] for x in range(0, len(s), 8)])

    def __repr__(self):
        return "Bits at {id}: [{self}]".format(
            id=id(self),
            self=self,
        )

    def __iter__(self):
        for i in range(self.length):
            yield self[i]

    def __getitem__(self, index):
        if index >= self.length:
            raise IndexError()
        return bit_at(
            self._raw[index // _BIT_PER_BYTE],
            _BIT_PER_BYTE,
            index % _BIT_PER_BYTE
        )

    def __setitem__(self, index, value):
        if index >= self.length:
            raise IndexError()
        old_value = self._raw[index // _BIT_PER_BYTE]
        new_value = set_bit(old_value, index % _BIT_PER_BYTE, value)
        self._raw[index // _BIT_PER_BYTE] = new_value
