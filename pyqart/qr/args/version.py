# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : QrVersion represent version of QrCode, which decide:
#               code's size,
#               value_upper codeword count,
#               align pattern position,
#               version pattern value.

__all__ = ['QrVersion']

_ALIGN_START_TABLE = [
    100, 16, 20, 24, 28, 32, 20, 22, 24, 26,
    28, 30, 32, 24, 24, 24, 28, 28, 28, 32,
    26, 24, 28, 26, 30, 28, 32, 24, 28, 24,
    28, 32, 28, 32, 28, 22, 26, 30, 24, 28,
]

_ALIGN_STEP_TABLE = [
    100, 100, 100, 100, 100, 100, 16, 18, 20, 22,
    24, 26, 28, 20, 22, 24, 24, 26, 28, 28,
    22, 24, 24, 26, 26, 28, 28, 24, 24, 26,
    26, 26, 28, 28, 24, 26, 26, 26, 28, 28,
]

_VERSION_PATTERN_VALUE_TABLE = [
    0x0, 0x0, 0x0, 0x0, 0x0,
    0x0, 0x7c94, 0x85bc, 0x9a99, 0xa4d3,
    0xbbf6, 0xc762, 0xd847, 0xe60d, 0xf928,
    0x10b78, 0x1145d, 0x12a17, 0x13532, 0x149a6,
    0x15683, 0x168c9, 0x177ec, 0x18ec4, 0x191e1,
    0x1afab, 0x1b08e, 0x1cc1a, 0x1d33f, 0x1ed75,
    0x1f250, 0x209d5, 0x216f0, 0x228ba, 0x2379f,
    0x24b0b, 0x2542e, 0x26a64, 0x27541, 0x28c69,
]

_CODEWORD_COUNT_TABLE = [
    26, 44, 70, 100, 134, 172, 196, 242, 292, 346,
    404, 466, 532, 581, 655, 733, 815, 901, 991, 1085,
    1156, 1258, 1364, 1474, 1588, 1706, 1828, 1921, 2051, 2185,
    2323, 2465, 2611, 2761, 2876, 3034, 3196, 3362, 3532, 3706,
]


class QrVersion(object):
    def __init__(self, version_number):
        assert 1 <= version_number <= 40, "Version must between 1 and 40."
        self._num = version_number

    @property
    def number(self):
        """
        :return: The number represent of the version, from 1 to 40.
        :rtype: int
        """
        return self._num

    @property
    def size(self):
        return 17 + 4 * self._num

    @property
    def align_start(self):
        return _ALIGN_START_TABLE[self.number - 1]

    @property
    def align_step(self):
        return _ALIGN_STEP_TABLE[self.number - 1]

    @property
    def version_pattern_value(self):
        return _VERSION_PATTERN_VALUE_TABLE[self.number - 1]

    @property
    def cwc(self):
        """
        CodeWord Count
        """
        return _CODEWORD_COUNT_TABLE[self.number - 1]
