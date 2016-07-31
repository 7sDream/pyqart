# Added at : 2016.7.31
# Author   : 7sDream
# Usage    : A printer that print QrCode to a image.

from io import BytesIO

from .base import BasePrinter
from ..painter import QrPainter

import PIL.Image as Image
import PIL.ImageDraw as Draw


class ImagePrinter(BasePrinter):
    @classmethod
    def print(cls, painter, code_width=None, border_width=None,
              fcolor=None, bgcolor=None, format='png',
              path=None):
        """
        Print the QrCode to a image.

        :param QrPainter painter: The painter that want print his/her QrCode.
        :param int code_width: Width and Height of code part.
            None will be 1 pixel per point.
        :param border_width: Border width, None will be code width / 20.
        :param (int, int, int) fcolor: Front color, Default is black.
        :param (int, int, int) bgcolor: Background color, Default is white.
        :param str format: Image suffix, like png, jpeg, bmp, etc.
        :param str path: If provided, will auto save file to the path.
        :return: Bytes data of image **Only when file path is not provided**.
        :rtype: bytes|None
        """
        matrix = painter.as_bool_matrix
        size = len(matrix)
        code_width = int(code_width) if code_width is not None else size
        border_width = size // 20 if border_width is None else border_width
        border_width = max(1, border_width)
        img_size = code_width + 2 * border_width

        fcolor = (0, 0, 0) if fcolor is None else fcolor
        bgcolor = (255, 255, 255) if bgcolor is None else bgcolor

        qrImg = Image.new('RGB', (size, size), bgcolor)
        drawer = Draw.Draw(qrImg)

        fpoints = []
        for y in range(size):
            for x in range(size):
                if matrix[y][x]:
                    fpoints.append((x, y))

        drawer.point(fpoints, fcolor)
        del drawer

        qrImg = qrImg.resize((code_width, code_width))

        img = Image.new('RGB', (img_size, img_size), bgcolor)
        img.paste(qrImg, (border_width, border_width))

        if path is not None:
            img.save(path, format=format)
            return None

        f = BytesIO()
        img.save(f, format=format)
        return f.getvalue()
