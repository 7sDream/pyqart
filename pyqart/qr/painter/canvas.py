# Added at : 2016.7.29
# Author   : 7sDream
# Usage    : A canvas to draw the QrCode. It implements function to draw
#            a basic QrCode whose data part is empty from QrArgs.

from .exception import QrCanvasException
from .point import QrPoint, QrPointType
from ..args import QrArgs

__all__ = ['QrCanvas']

_TYPE_CHAR_MAP = {
    QrPointType.UNKNOWN: '? ',
    QrPointType.POSITION: 'Q*',
    QrPointType.ALIGNMENT: 'A^',
    QrPointType.TIMING: 'T-',
    QrPointType.FORMAT: 'F<',
    QrPointType.VERSION_PATTERN: 'V+',
    QrPointType.UNUSED: 'Nu',
    QrPointType.DATA: '@.',
    QrPointType.CORRECTION: '#,',
    QrPointType.EXTRA: 'E~',
}
"""
The char table use to convert QrCode to string to print.
"""

_BIT_PER_CW = 8


class QrCanvas(object):
    def __init__(self, args):
        assert isinstance(args, QrArgs), "args argument must be QrArgs object."
        self._args = args
        self._size = self.args.size
        self._points = [
            [QrPoint(False) for _ in range(self.size)]
            for _ in range(self.size)]

        self._add_timing_pattern()
        self._add_position_patterns()
        self._add_align_patterns()
        self._add_version_pattern()
        self._add_unused_point()
        self._add_format_pattern()
        self._data_ec_points = self._add_empty_data_ec()
        self._add_mask()
        self._rotate()

    def _add_timing_pattern(self):
        """
        Add timing line to point array,  like bellow

          0 1 2 3 4 5 6 7 8 9 ... -- x axis
        0             @
        1             .
        2             @
        3             .
        4             @
        5             .
        6 @ . @ . @ . @ . @ . @ . @ . @ . @ . @ . @ . @ ....
        7             .
        8             @
        9             .
        10            @
        11            .
        12            @
        13           ...
        |
        y axis

        The (0-6, 6) and (6, 0-5) part will be override by position box.
        """
        # rol 6 and col 6 is timing version_pattern_value
        timing_position = 6
        for i in range(self.size):
            self._points[i][timing_position].type = QrPointType.TIMING
            self._points[timing_position][i].type = QrPointType.TIMING
            if i % 2 == 0:
                self._points[i][timing_position].fill = True
                self._points[timing_position][i].fill = True

    def _add_position_patterns(self):
        self._add_position_pattern(0, 0)
        self._add_position_pattern(0, self.size - 7)
        self._add_position_pattern(self.size - 7, 0)

    def _add_align_patterns(self):
        first_special_pos = 4
        start = self.args.align_start
        step = self.args.align_step
        size = self.size
        y = first_special_pos
        while y + 5 < size:
            x = first_special_pos
            while x + 5 < size:
                if self._check_align_box_position(y, x):
                    self._add_align_pattern(y, x)
                x = start if x == first_special_pos else (x + step)
            y = start if y == first_special_pos else (y + step)

    def _add_version_pattern(self):
        version_block_pattern = self.args.version_pattern_value
        if version_block_pattern != 0:
            for x in range(6):
                for y in range(3):
                    point_a = self._points[self.size - 11 + y][x]
                    point_b = self._points[x][self.size - 11 + y]
                    point_a.type = point_b.type = QrPointType.VERSION_PATTERN
                    if version_block_pattern & 1 != 0:
                        point_a.fill = point_b.fill = True
                    version_block_pattern >>= 1

    def _add_unused_point(self):
        point = self._points[self.size - 8][8]
        point.type = QrPointType.UNUSED
        point.fill = True

    def _add_format_pattern(self):
        for i, bit in enumerate(reversed(self.args.format_pattern_bits)):
            # top left
            if i < 6:
                point_1 = self._points[i][8]
            elif i < 8:
                point_1 = self._points[i + 1][8]
            elif i < 9:
                point_1 = self._points[i][7]
            else:
                point_1 = self._points[8][14 - i]

            # top right
            if i < 8:
                point_2 = self._points[8][self.size - 1 - i]
            # bottom left
            else:
                point_2 = self._points[self.size - 15 + i][8]

            point_1.type = point_2.type = QrPointType.FORMAT
            point_1.fill = point_2.fill = bit

    def _add_empty_data_ec(self):
        # make data and extra data
        dbc = self.args.dcwc * _BIT_PER_CW
        ecbc = self.args.eccwc * _BIT_PER_CW
        data_points = [QrPoint(False, QrPointType.DATA, offset)
                       for offset in range(dbc)]
        ec_points = [QrPoint(False, QrPointType.CORRECTION, dbc + offset)
                     for offset in range(ecbc)]

        # split into blocks
        data_blocks = []
        ec_blocks = []
        ecbpb = self.args.eccwcpb * _BIT_PER_CW
        di = eci = 0
        for bi in range(self.args.bc):
            dbcpb = self.args.dcwcof(bi) * _BIT_PER_CW
            data_blocks.append(data_points[di:di + dbcpb])
            ec_blocks.append(ec_points[eci:eci + ecbpb])
            di += dbcpb
            eci += ecbpb

        if di != dbc or eci != ecbc:
            raise QrCanvasException(
                "Error when split data and ec points to blocks.")

        # re-sort codewords
        data_ec_points = []
        for cwi in range(self.args.ndcwcpb + 1):  # cwi for CodeWord Index
            for blki in range(self.args.bc):  # bi for BLocK Index
                if cwi * _BIT_PER_CW < len(data_blocks[blki]):
                    bi = cwi * _BIT_PER_CW
                    data_ec_points.extend(
                        data_blocks[blki][bi:bi + _BIT_PER_CW])
        for cwi in range(self.args.eccwcpb):
            for blki in range(self.args.bc):
                bi = cwi * _BIT_PER_CW
                data_ec_points.extend(ec_blocks[blki][bi:bi + _BIT_PER_CW])

        if len(data_ec_points) != dbc + ecbc:
            raise QrCanvasException("Error when resort codewords.")

        # add remain points
        # value_upper remaining data count is value_upper(0, 3, 4, 7) = 7
        for i in range(7):
            data_ec_points.append(QrPoint(False, QrPointType.EXTRA))

        # re place points to canvas
        ai = 0  # for All Index
        x = self.size

        def place_two_column(reverse, now_index):
            y_list = range(self.size)
            for y in (y_list if not reverse else reversed(y_list)):
                if self._points[y][x - 1].type is QrPointType.UNKNOWN:
                    self._points[y][x - 1] = data_ec_points[now_index]
                    now_index += 1
                if self._points[y][x - 2].type is QrPointType.UNKNOWN:
                    self._points[y][x - 2] = data_ec_points[now_index]
                    now_index += 1
            return now_index

        while x > 0:
            ai = place_two_column(True, ai)
            x -= 2
            x = 6 if x == 7 else x
            ai = place_two_column(False, ai)
            x -= 2

        return data_ec_points

    def _add_mask(self):
        for y in range(self.size):
            for x in range(self.size):
                point = self._points[y][x]
                if point.type in {QrPointType.DATA, QrPointType.CORRECTION,
                                  QrPointType.EXTRA}:
                    point.invert = self.args.should_invert(y, x)

    def _add_position_pattern(self, y, x):
        """
        add big position box to pixels array, box pattern like bellow

           -1 0 1 2 3 4 5 6 7 -- x(i) axis offset
        -1  . . . . . . . . .
         0  . # @ @ @ @ @ @ .
         1  . @ . . . . . @ .
         2  . @ . @ @ @ . @ .
         3  . @ . @ @ @ . @ .
         4  . @ . @ @ @ . @ .
         5  . @ . . . . . @ .
         6  . @ @ @ @ @ @ @ .
         7  . . . . . . . . .
         |
        y(j)
        axis
        offset

            . for white pixel
            @ for black pixel
            # start pixel

        :param x: left of start pixel
        :param y: top of start pixel
        """

        # ===== generate inside 7 x 7 box =====
        for i in range(7):
            for j in range(7):
                #  left, right     up, bottom           fill inside rect
                point = self._points[x + i][y + j]
                point.type = QrPointType.POSITION
                if i in {0, 6} or j in {0, 6} or (2 <= i <= 4 and 2 <= j <= 4):
                    point.fill = True

        # ===== generate left and right white border =====

        for j in range(-1, 8):
            if self._check_index(y + j):
                if self._check_index(x - 1):
                    # left
                    self._points[y + j][x - 1].type = QrPointType.POSITION
                if self._check_index(x + 7):
                    # right
                    self._points[y + j][x + 7].type = QrPointType.POSITION

        for i in range(-1, 8):
            if self._check_index(x + i):
                if self._check_index(y - 1):
                    # top
                    self._points[y - 1][x + i].type = QrPointType.POSITION
                if self._check_index(y + 7):
                    # bottom
                    self._points[y + 7][x + i].type = QrPointType.POSITION

    def _add_align_pattern(self, y, x):
        """
        add align box to pixels array, version_pattern_value like bellow

          0 1 2 3 4 -- x(i) axis offset
        0 # @ @ @ @
        1 @ . . . @
        2 @ . @ . @
        3 @ . . . @
        4 @ @ @ @ @
        |
        y(j) axis offset

        :param x: left of start pixel
        :param y: top of start pixel
        """
        for j in range(5):
            for i in range(5):
                point = self._points[y + j][x + i]
                point.type = QrPointType.ALIGNMENT
                if i in {0, 4} or j in {0, 4} or i == j == 2:
                    point.fill = True

    def _check_index(self, x):
        return 0 <= x < self.size

    def _check_align_box_position(self, y, x):
        return QrPointType.POSITION not in {
            self._points[y][x].type,
            self._points[y][x + 5].type,
            self._points[y + 5][x].type,
            self._points[y + 5][x + 5].type
        }

    def _rotate(self):
        if self.args.rotate_func is None:
            return
        new = [[None for _ in range(self.size)] for __ in range(self.size)]
        for y in range(self.size):
            for x in range(self.size):
                new_y, new_x = self.args.rotate_func(y, x, self.size)
                new[new_y][new_x] = self.points[y][x]
        self._points = new

    @property
    def args(self):
        return self._args

    @property
    def size(self):
        return self._size

    @property
    def data_ec_points(self):
        return self._data_ec_points

    def load_data(self, bits):
        data_ec_length = len(self._data_ec_points) - 7
        assert bits.length == data_ec_length
        for _, point in zip(range(data_ec_length), self._data_ec_points):
            point.fill = bits[point.offset]

    @property
    def points(self):
        return self._points

    def __str__(self):
        lines = []
        for row in self._points:
            line = []
            for point in row:
                fill = point.fill if not point.invert else not point.fill
                line.append(_TYPE_CHAR_MAP[point.type][0 if fill else 1])
            lines.append(' '.join(line))
        return '\n'.join(lines)
