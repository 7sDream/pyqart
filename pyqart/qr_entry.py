import argparse
import sys

from pyqart.qr.data import QrData
from pyqart.qr.painter import QrPainter
from pyqart.qr.printer import QrImagePrinter, QrStringPrinter


def main():
    parser = argparse.ArgumentParser(
        prog="pyqr",
        description="A program of generate QrCode.",
        epilog="Writen by 7sDream. (https://github.com/7sDream/pyqart)",
    )
    parser.add_argument(
        'string', type=str,
        help="string will be encode"
    )
    parser.add_argument(
        '-v', '--version', type=int,
        help="version of QrCode, 1 to 40, "
             "will auto calculated from data length if not provide"
    )
    parser.add_argument(
        '-l', '--level', type=int, default=0,
        help="QrCode error correction level, 0 to 3, default is 0"
    )
    parser.add_argument(
        '-m', '--mask', type=int,
        help="mask of QrCode, 0 to 7, default is random value"
    )
    parser.add_argument(
        '-r', '--rotation', type=int, default=0,
        help="rotate the QrCode(clockwise), "
             "0 for no rotation, 1 for 90 degree, 2 for 180, 3 for 270"
    )
    parser.add_argument(
        '-p', '--point-size', type=int, default=3,
        help="the point width and height of one QrCode point,"
             " by pixel, default is 3"
    )
    parser.add_argument(
        '-b', '--board', type=int,
        help="board wide by pixel, will auto calculated "
             "from code size if not provide",
    )
    parser.add_argument(
        '-c', '--color', type=int, nargs=3, metavar=('R', 'G', 'B'),
        help="front color of QrCode, 3 number as rgb color",
    )
    parser.add_argument(
        '-g', '--background-color', type=int, nargs=3, metavar=('R', 'G', 'B'),
        help="background color of QrCode, 3 number as rgb color",
    )
    parser.add_argument(
        '-o', '--output', type=str,
        help="output file path, code will print to terminal if not provide, "
             "and other arguments will be ignored"
    )

    argv = sys.argv[1:]

    args = parser.parse_args(argv)

    data = QrData(args.string, args.level)
    painter = QrPainter(data, args.version, args.mask, args.rotation)

    if args.color is not None:
        args.color = tuple(args.color)
    if args.background_color is not None:
        args.background_color = tuple(args.background_color)

    if args.output is not None:
        QrImagePrinter.print(
            painter, args.output, args.point_size, args.board,
            args.color, args.background_color
        )
    else:
        QrStringPrinter.print(painter, True)

if __name__ == '__main__':
    main()
