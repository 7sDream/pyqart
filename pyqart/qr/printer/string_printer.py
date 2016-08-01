# Added at : 2016.8.1
# Author   : 7sDream
# Usage    : A printer that print QrCode to a string, can be show in shell.

from .base import QrBasePrinter

WHITE_ALL = '\u2588'
WHITE_BLACK = '\u2580'
BLACK_WHITE = '\u2584'
BLACK_ALL = ' '

MAP = {
    (True, True): BLACK_ALL,
    (True, False): BLACK_WHITE,
    (False, True): WHITE_BLACK,
    (False, False): WHITE_ALL,
}


class QrStringPrinter(QrBasePrinter):
    @classmethod
    def print(cls, obj, print_out=True, *args, **kwargs):
        """
        :param obj: See :any:`QrImagePrinter`
        :param bool print_out: Whether to print QrCode out.
        :return: The string that can be print out like a QrCode.
        :type: string
        """
        painter = cls._create_painter(obj)
        matrix = painter.as_bool_matrix
        matrix = [[False] + x + [False] for x in matrix]
        size = len(matrix) + 2
        matrix.insert(0, [False] * size)
        matrix.append([False] * size)
        matrix.append([True] * size)
        lines = []
        for row in range(0, size, 2):
            line = []
            for col in range(0, size):
                line.append(MAP[(matrix[row][col], matrix[row + 1][col])])
            lines.append(''.join(line))
        string = '\n'.join(lines)
        if print_out:
            print(string)
        return string
