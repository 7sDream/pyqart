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

![qr code: hello world][qr-in-image]

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

## TODO

- [x] Make QrPainter decided argument by itself.
- [x] Art part
- [x] CLI
- [x] Package
- [ ] GUI
- [ ] Use Cython to accelerate Reed-Solomon error correction
- [ ] Docs
- [ ] Tests

## Other Implement

- Golang: [qr][qr] by [Russ Cox][russ_cos_google_plus]
- Java: [qart4j][qart4j] by [dieforfree][dieforfree]

## Acknowledgements

- All credit goes to [Russ Cos][russ_cos_google_plus], Thanks for his article and implement.
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
