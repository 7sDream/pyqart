import argparse
import sys
import time

from pyqart.art import QArtist
from pyqart.qr.printer import QrImagePrinter, QrStringPrinter


def main():
    parser = argparse.ArgumentParser(
        prog="pyqart",
        description="A program of generate QArt Codes.",
        epilog="Writen by 7sDream. (https://github.com/7sDream/pyqart)",
    )
    parser.add_argument(
        'url', type=str,
        help="url will be encode, like http://example.com/",
    )
    parser.add_argument(
        'img', type=str,
        help="target image the QrCode will look like",
    )
    parser.add_argument(
        '-s', '--start-point', type=int, nargs=2,
        help="left top point of the region of target image to use, "
             "default is (0, 0).",
    )
    parser.add_argument(
        '-w', '--region-width', type=int,
        help="target region width and height, "
             "default will make region as bigger as possible",
    )
    parser.add_argument(
        '-d', '--dither', action="store_true",
        help="dithering when generate binary target image",
    )
    parser.add_argument(
        '-y', '--only-data', action="store_true",
        help="only use data bit points to approach the target image",
    )
    parser.add_argument(
        '-n', '--rand', action="store_true",
        help="generate point contrast by random, "
             "if not provide, will use pixel nearby to calculate contrast",
    )
    parser.add_argument(
        '-f', '--higher-first', action='store_true',
        help="pick pixel from higher contrast region first, "
             "default will pick from lower region first"
    )
    parser.add_argument(
        '-x', '--yx', type=int, nargs=2,
        help="yx region when calculate contrast",
    )
    parser.add_argument(
        '-v', '--version', type=int,
        help="version of QrCode, 1 to 40, "
             "will auto calculated from data length if not provide",
    )
    parser.add_argument(
        '-l', '--level', type=int, default=0,
        help="QrCode error correction level, 0 to 3, default is 0",
    )
    parser.add_argument(
        '-m', '--mask', type=int,
        help="mask of QrCode, 0 to 7, default is random value",
    )
    parser.add_argument(
        '-r', '--rotation', type=int, default=0,
        help="rotate the QrCode(clockwise), "
             "0 for no rotation, 1 for 90 degree, 2 for 180, 3 for 270",
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

    if args.yx is None:
        args.yx = [None, None]
    if args.color is not None:
        args.color = tuple(args.color)
    if args.background_color is not None:
        args.background_color = tuple(args.background_color)

    start = time.time()

    artist = QArtist(args.url, args.img, args.version, args.mask, args.level,
                     args.rotation, args.dither, args.only_data, args.rand,
                     args.yx[0], args.yx[1])

    if args.output is not None:
        QrImagePrinter.print(
            artist, args.output, args.point_size, args.board,
            args.color, args.background_color
        )
        print('Done.')
    else:
        QrStringPrinter.print(artist, True)

    end = time.time()
    print("Used time:", end-start, 'second.')

if __name__ == '__main__':
    main()
