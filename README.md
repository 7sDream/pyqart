# PyQArt - QArt Python implementation

[中文版 README](https://github.com/7sDream/pyqart/blob/master/README.zh.md)

## introduction

QArt is a method of combining QrCode of an URL with any image, which was submitted in [an article][qart-article] writen by [Russ Cox][russ-cos-google-plus] on his personal website.

An Example(come from the article):

![QArt Example][qart-example]

This repo is Python implementation of it.

## Install

```
pip install pyqart
```

**Note: Support Python3 only, please make sure you are using pip of Python3.**

## Usage

For code reuse, I split the lib to two part. One for generate normal QrCode, another for generate QArt.

### The Qr Part

Use `pyqr` CLI to create normal QrCode.

```
 pyqr -p 5 -c 102 204 255 "Hello World!" -o qr.png
 ```
 
 The options:
 
 - `-p` for point size of QrQCode, by pixel, default is 3 pixel.
 - `-c` for color of point, default is black. Background color can be set with `-g` option, default is white.

![qr code: hello world][my-qr-img]

If you want show it in terminal, just don't provide `-o` option:

```bash
pyqr "Hello World"
```

Then you will see:

![qr in terminal: hello world][my-qr-terminal]

The actual result you will see depends on your font setting, I'm using Dejavu Sans Mono.

Yes, it is only useful for small QrCode. 

Run `pyqr -h` for more options and their effect.

### The Art Part

Use `pyqart` CLI to create QArt. It may take a long time, please be patient :)

This is an example that mix my blog url and my Github avatar: 

```
pyqart -v 8 -c 102 204 255 "http://0v0.link/" photo.jpg -o qart.png
```

My Github avatar:

![][my-github-avatar]

The QArt Code:

![][my-qart-img]

Not meet your expectations? Try `-n` option to pick point at random(default is pick low-contrast region pixels first):

```bash
pyqart -n -c 102 204 255 -v 8 "http://0v0.link/" photo.jpg -o qart-n.png
```

![][my-qart-n-img]

Still not satisfied? Use `-y` option to enhance the accuracy of the central region by giving up the control of the edge pixels:

![][my-qart-y-img]

`-y` and `-n` can be used at the same time, but no obvious improvement.

**Note： because that `-y` option will only use data block, ignore error correction block，it reduce many many many calculate. It has about 30x to 100x speed up compare with no `-y` option case. So I strongly recommend using `-y` option whenever you needn't make a full picture fitting.**

Use `-r` option to set rotation degree, The controllable data region can be changed into a horizontal area, it will make it easier to process very wide picture.

![][my-pyqart-y-r-img]

Run `pyqart -h` for more options and their effect.

### Use it in your codes as a module

Documentation is in preparation.

## Gallery

![][python-qr]

python.org(used -d option, means dithering, see help message for more info.)

![][github-qr]

github.com

![][bilibili-qr]

bilibili.com (An ACG videos website)

## Halftone

Halftone support added in version 0.1.0, and I made another new method which combined Halftone and QArt, so I call it HalfArt temporarily.

The following code shows arguments to get output image of all kind of method:

```python
from pyqart import QArtist, QrHalftonePrinter, QrImagePrinter, QrPainter

QR_VERSION = 10
POINT_PIXEL = 3

artist = QArtist('http://www.nankai.edu.cn/', 'example.jpg', QR_VERSION)
painter = QrPainter('http://www.nankai.edu.cn/', QR_VERSION)
artist_data_only = QArtist('http://www.nankai.edu.cn/', 'example.jpg',
                           QR_VERSION, only_data=True)

# normal
QrImagePrinter.print(painter, path='normal.png', point_width=POINT_PIXEL)
# Halftone
QrHalftonePrinter.print(painter, path='halftone.png', img='example.jpg',
                        point_width=POINT_PIXEL, colorful=False)
# Halftone colorful
QrHalftonePrinter.print(painter, path='halftone-color.png', img='example.jpg',
                        point_width=POINT_PIXEL)
# Halftone pixel
QrHalftonePrinter.print(painter, path='halftone-pixel.png', img='example.jpg',
                        point_width=POINT_PIXEL, colorful=False,
                        pixelization=True)
# QArt
QrImagePrinter.print(artist, path='qart.png', point_width=POINT_PIXEL)
# QArt data only
QrImagePrinter.print(artist_data_only, path='qart-data-only.png',
                     point_width=POINT_PIXEL)
# HalfArt
QrHalftonePrinter.print(artist, path='halfart.png', point_width=POINT_PIXEL)
# HalfArt data only
QrHalftonePrinter.print(artist_data_only, path='halfart-data-only.png',
                        point_width=POINT_PIXEL)
```

Result：

|  |  |  |
| :-: | :-: | :-: |
| ![][halftone.png]| ![][halftone-color.png] | ![][halftone-pixel.png] |
| halftone | halftone colorful | halftone pixel |
| ![][qart.png] | ![][qart-data-only.png] | |
| QArt | QArt data only | |
| ![][halfart.png] | ![][halfart-data-only.png] | |
| HalfArt | HalfArt data only | |

## TODO

- [x] Make QrPainter decided argument by itself.
- [x] Art part
- [x] CLI
- [x] Package
- [ ] GUI
- [ ] Use Cython to accelerate Reed-Solomon error correction
- [ ] Docs
- [ ] Tests

## Other Implementation

- Golang: [qr][qr] by [Russ Cox][russ-cos-google-plus]
- Java: [qart4j][qart4j] by [dieforfree][dieforfree]

## Acknowledgements

- All credit goes to [Russ Cos][russ-cos-google-plus], Thanks for his article and implement.
- Thanks for [qart4j project][qart4j] by [dieforfree][dieforfree]，which helps me so much on how to implement the art part.
- Thanks to a series of articles named [QR Code Tutorial][tutorial] in thonky.com, It's very detailed. Whenever I faced problem about encoding or error correction, I will go to it for help.
- Thanks to the Python programing language。

## LICENSE

MIT.

See LICENSE.

[russ-cos-google-plus]: https://plus.google.com/+RussCox-rsc
[qart-article]: http://research.swtch.com/qart
[qart-example]: http://ww4.sinaimg.cn/large/88e401f0gw1f6dl845naoj205g05ga9y.jpg
[my-qr-img]: http://ww3.sinaimg.cn/large/88e401f0gw1f6ir3ifivzj20370370ss.jpg
[my-qr-terminal]: http://ww2.sinaimg.cn/large/88e401f0gw1f6ir4taf7hj209008c3ze.jpg
[my-github-avatar]: http://ww3.sinaimg.cn/large/88e401f0gw1f6iyj9nuwhj2049049q2v.jpg
[my-qart-img]: http://ww3.sinaimg.cn/large/88e401f0gw1f6ir8t0mbej20490490t2.jpg
[my-qart-n-img]: http://ww1.sinaimg.cn/large/88e401f0gw1f6irh15ouuj2049049mxp.jpg
[my-qart-y-img]: http://ww2.sinaimg.cn/large/88e401f0gw1f6irbnfjozj20490490t4.jpg
[my-pyqart-y-r-img]: http://ww3.sinaimg.cn/large/88e401f0gw1f6jd7w10r7j205l05lt91.jpg
[qr]: https://code.google.com/p/rsc/source/browse/qr
[dieforfree]: https://github.com/dieforfree
[qart4j]: https://github.com/dieforfree/qart4j
[tutorial]: http://www.thonky.com/qr-code-tutorial/

[python-qr]: http://ww1.sinaimg.cn/large/88e401f0gw1f6iz81tkwpj204x04xaaf.jpg
[github-qr]: http://ww4.sinaimg.cn/large/88e401f0gw1f6izdtv2kqj204x04x0sy.jpg
[bilibili-qr]: http://ww3.sinaimg.cn/large/88e401f0gw1f6j0ds93k9j204x04x74m.jpg

[halftone.png]: http://rikka-10066868.image.myqcloud.com/f62cbc2f-1e38-4a94-80aa-0be1a0c32b55.png
[halftone-color.png]: http://rikka-10066868.image.myqcloud.com/d96d057a-42d2-469b-9b65-0eabd2bd915f.png
[halftone-pixel.png]: http://rikka-10066868.image.myqcloud.com/00da6fa8-5035-4ba6-8c33-584b54e73e2d.png
[qart.png]: http://rikka-10066868.image.myqcloud.com/d2f3febb-a535-4154-8ebc-80183701c47d.png
[qart-data-only.png]: http://rikka-10066868.image.myqcloud.com/59834cea-5d44-41c3-b759-780c56c9789b.png
[halfart.png]: http://rikka-10066868.image.myqcloud.com/8b0847b9-c3fc-451d-b554-7bdc3a53f7e9.png
[halfart-data-only.png]: http://rikka-10066868.image.myqcloud.com/9f4fd92e-99ff-4aca-a252-b6c1ab709e65.png
