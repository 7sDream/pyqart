from __future__ import division

import PIL.ImageDraw as Draw
import PIL.Image as Image

from .image_printer import QrImagePrinter
from ..painter.point import QrPointType
from ...art.qart import QArtist


class QrHalftonePrinter(QrImagePrinter):

    @classmethod
    def print(cls, obj, path=None, point_width=None, border_width=None,
              f_color=None, bg_color=None, file_format=None,
              img=None, colorful=True, pixelization=False):

        super_class = super(QrHalftonePrinter, cls)

        point_width, border_width = super_class._calc_point_border_width(
            point_width, border_width)

        if not colorful:
            bg_color = (255, 255, 255)
            f_color = (0, 0, 0)

        point_width = int(((point_width - 1) // 3 + 1) * 3)
        mask_block_width = point_width // 3
        painter = cls._create_painter(obj)
        canvas = painter.canvas

        if isinstance(painter, QArtist) and img is None:
            img = painter.source.to_image(
                canvas.args, painter.dither, painter.dy, painter.dx
            )

        pass_path = path if img is None else None

        qr = super_class.print(
            painter, pass_path, point_width, border_width,
            f_color, bg_color, file_format,
        )

        qr_size = qr.size[0] - 2 * border_width

        if img is not None:
            if not isinstance(painter, QArtist):
                if not isinstance(img, Image.Image):
                    img = Image.open(str(img))
                if not colorful:
                    if pixelization:
                        img = img.convert('L')
                    else:
                        img = img.convert('1')
                if pixelization:
                    img = img.resize((canvas.size, canvas.size))
        else:
            return qr

        img = img.resize((qr_size, qr_size))

        x = y = 0
        mask = Image.new('1', (qr_size, qr_size), 0)
        drawer = Draw.Draw(mask, '1')
        for line in canvas.points:
            for point in line:
                if point.type in {QrPointType.DATA, QrPointType.CORRECTION}:
                    drawer.rectangle(
                        [x, y, x + point_width - 1, y + point_width - 1],
                        fill=1, outline=1,
                    )
                    drawer.rectangle(
                        [
                            x + mask_block_width,
                            y + mask_block_width,
                            x + 2 * mask_block_width - 1,
                            y + 2 * mask_block_width - 1,
                        ],
                        fill=0, outline=0
                    )
                x += point_width
            x, y = 0, y + point_width

        # uncomment the following code to see mask image
        # mask.save(path + '.mask.bmp', format='bmp')

        qr.paste(img, (border_width, border_width), mask)

        if path is not None:
            qr.save(path, format=file_format)
            return None

        return qr
