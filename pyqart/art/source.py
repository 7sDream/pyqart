# Added at : 2016.8.2
# Author   : 7sDream
# Usage    : Source image to make QArt.

from random import randint

import PIL.Image as Image

from .target import Target
from ..qr.painter.point import QrPointType

__all__ = ['QArtSourceImage']


class QArtSourceImage(object):
    def __init__(self, path, left=None, top=None, size=None, board=None):
        """
        :param str|file path: Image file path or file-like object.
        :param int left: X of start point.
        :param int top: Y of start point.
        :param int size: Size of target image region.
        :param int board: Board region width.
        """
        self._img = Image.open(path)
        left = left or 0
        top = top or 0
        if size is None:
            size = min(self._img.width - left, self._img.height - top)
        self._set(left or 0, top or 0, size or 0, board or 0)
        self.path = path

    def _set(self, left, top, size, border):
        assert left >= 0, "left arg must > 0"
        assert top >= 0, "top arg must > 0"
        assert size >= 0, "size arg must >= 0"
        assert left + size <= self._img.width, "region over image"
        assert top + size <= self._img.height, "region over image"
        assert border >= 0, "border width must >= 0"
        self._left = int(left)
        self._top = int(top)
        self._size = int(size)
        self._border = int(border)

    def set_by_center(self, x, y, size, board):
        offset = (size - 1) // 2
        self._set(x - offset, y - offset, size, board)

    @staticmethod
    def _calc_divider(img):
        res = 0
        for row in range(img.height):
            for col in range(img.width):
                res += img.getpixel((row, col))
        n = img.width * img.height

        if n == 0:
            return 128

        return res // n

    @staticmethod
    def _calc_target_range(img, y, x, dy, dx):
        assert dy is None or dy > 0
        assert dx is None or dx > 0
        dx = dx or 3
        dy = dy or 3
        left = x - dx if x - dx >= 0 else 0
        right = x + dx + 1 if x + dx < img.width else img.width
        top = y - dy if y - dy >= 0 else 0
        bottom = y + dy + 1 if y + dy < img.height else img.height
        width = right - left
        height = bottom - top
        return left, right, top, bottom, width, height

    def _calc_contrast(self, img, y, x, dy, dx, rand):
        assert 0 <= y < img.height and 0 <= x < img.width, "Point out of image."
        assert isinstance(rand, bool)

        if rand:
            return randint(0, 128) + 64 * ((x + y) % 2) + 64 * ((x + y) % 3 % 2)

        l, r, t, b, w, h = self._calc_target_range(img, y, x, dy, dx)
        n = w * h
        sum_1 = sum_2 = 0
        for y in range(t, b):
            for x in range(l, r):
                v = img.getpixel((x, y))
                sum_1 += v
                sum_2 += v * v
        average = sum_1 / n

        return sum_2 / n - average * average

    def to_image(self, args, dither, dy, dx):
        assert dx is None or dx > 0, 'dx must >= 0.'
        assert dy is None or dy > 0, 'dy must >= 0.'

        code_part_size = self._size - 2 * self._border

        box_x, box_y = self._left + self._border, self._top + self._border
        box = (box_x, box_y, box_x + code_part_size, box_y + code_part_size)
        img = self._img.crop(box).resize((args.size, args.size))

        if dither:
            img = img.convert("1")
        else:
            img = img.convert('L')
            divider = self._calc_divider(img)
            img = img.point(lambda v: 0 if v <= divider else 255, '1')

        return img

    def to_targets(self, canvas, args, dither, rand, dy, dx):
        """
        :param QrCanvas canvas: canvas used to draw the QrCode.
        :param QrArgs args: The args of QrCode.
        :param bool dither: Make binary image with dithering or not.
        :param bool rand: Make contrast of target random number.
        :param int dy: Y offset when calc target.
        :param int dx: X offset when calc target.
        """
        temp = self.to_image(args, dither, dy, dx)

        targets = [None] * args.cwc * 8
        for y in range(temp.height):
            for x in range(temp.width):
                point = canvas.points[y][x]
                if point.type in {QrPointType.DATA, QrPointType.CORRECTION}:
                    fill = temp.getpixel((x, y)) == 0
                    contrast = self._calc_contrast(temp, y, x, dy, dx, rand)
                    targets[point.offset] = Target(y, x, fill, contrast, point)
        return targets
