# Added at : 2016.7.31
# Author   : 7sDream
# Usage    : A printer that print QrCode to a image.

from .base import QrBasePrinter
from ..data import QrData

import PIL.Image as Image
import PIL.ImageDraw as Draw


class QrImagePrinter(QrBasePrinter):

    @classmethod
    def _calc_point_border_width(cls, point_width, border_width):
        point_width = int(point_width) if point_width is not None else 1
        border_width = point_width if border_width is None else border_width
        border_width = max(1, border_width)
        return point_width, border_width

    @classmethod
    def print(cls, obj, path=None, point_width=None, border_width=None,
              f_color=None, bg_color=None, file_format=None):
        """
        Print the QrCode to a image.

        :param QrPainter|QrData|str|bytes|bytearray obj:
            The painter that want print his/her QrCode,
            or a raw QrData object which contains data,
            or just a string or bytes(bytearray) which will used as data.
        :param str path: If provided, will auto save file to the path.
        :param int point_width: Width and Height of code part.
            None will be 1 pixel per point.
        :param border_width: Border width, None will be code width / 20.
        :param (int, int, int) f_color: Front color, Default is black.
        :param (int, int, int) bg_color: Background color, Default is white.
        :param str file_format: Image suffix, like png, jpeg, bmp, etc.
        :return: Bytes data of image **Only when file path is not provided**.
        :rtype: PIL.Image
        """

        point_width, border_width = cls._calc_point_border_width(
            point_width, border_width)

        obj = cls._create_painter(obj)

        matrix = obj.as_bool_matrix
        size = len(matrix)
        code_width = size * point_width
        img_size = code_width + 2 * border_width

        f_color = (0, 0, 0) if f_color is None else f_color
        bg_color = (255, 255, 255) if bg_color is None else bg_color

        qr_img = Image.new('RGB', (size, size), bg_color)
        drawer = Draw.Draw(qr_img)

        fill_points = []
        for y in range(size):
            for x in range(size):
                if matrix[y][x]:
                    fill_points.append((x, y))

        drawer.point(fill_points, f_color)
        del drawer

        qr_img = qr_img.resize((code_width, code_width))

        img = Image.new('RGB', (img_size, img_size), bg_color)
        img.paste(qr_img, (border_width, border_width))

        if path is not None:
            img.save(path, format=file_format)
            return None

        return img
