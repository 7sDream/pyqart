# PyQArt - Python implement of QArt

[中文版 README](https://github.com/7sDream/pyqart/blob/master/README.zh.md)

## introduction

QArt is a method of combining QrCode of an URL with any image, which was submitted in [an article][qart_article] writen by [Russ Cox][russ_cos_google_plus] on his personal website.

An Example(come from the article):

![QArt Example](http://ww4.sinaimg.cn/large/88e401f0gw1f6dl845naoj205g05ga9y.jpg)

And this repo is python implement of it.

## Usage

For code reues, I split the lib to two part. One for generate normal QrCode, another is the Art part - mix it with image.

**BUT! Art part is under construction, now just the Qr part is usable.**

### The Qr Part

```python
from pyqart import QrArgs, QrPainter, ImagePrinter

# set QrCode arguments
args = QrArgs(
    1,  # version, which decide the size, max data bis, etc of the QrCode
    0,  # error correction level, 0 to 3,
    0,  # data mask, from 0 to 7
)

# create a painter to draw QrCode from data
painter = QrPainter(args)

# give painter some data
painter.put_string("Hello world!")

# printer print QrCode to image
ImagePrinter.print(
    painter,
    bgcolor=(255, 255, 255),
    fcolor=(102, 204, 255),
    code_width=200,
    border_width=5,
    path='qr.png'
)
```

Then you will get a QrCode image on current directory whose:

- Size of code part is 200x200. 
- Board width 5 pixels.
- Background is white(255, 255, 255).
- Front color is Tianyi Blue(name of color (102, 204, 255)).
- Filename is qr.png.

Like bellow:

![qr code: hello world](http://ww4.sinaimg.cn/large/88e401f0gw1f6dmbn4xp6j205u05u0t4.jpg)

If you want show it in terminal, please use StringPrinter：

```python
from pyqart import QrArgs, QrPainter, StringPrinter

# just like last example

# ...

print(StringPrinter.print(painter))
```

Then you will see:

![qr in terminal: hello world](http://ww4.sinaimg.cn/large/88e401f0gw1f6dmg4d14bj20ja0dowft.jpg)

What you will see depends on your font setting, I'm using Dejavu Sans Mono.

Yes, StringPrinter is useful for only those small QrCode. 

### Art Part

I'm working on it.

## TODO

- [ ] Art part
- [ ] CLI
- [ ] GUI
- [ ] doc
- [ ] package
- [ ] test

## Other Implement

- Golang: [qr][qr] by [Russ Cox][russ_cos_google_plus]
- Java: [qart4j][qart4j] by [dieforfree][dieforfree]

## Acknowledgements

- All credit goes to [Russ Cos][russ_cos_google_plus], Thanks for him。
- Thanks for [qart4j project][qart4j] by [dieforfree][dieforfree]，which helps me so much on how to implement the art part.
- Thanks to a series of articles named [QR Code Tutorial][tutorial] of thonky.com, Is very detailed. Whenever I faced problem about encoding or error correction, I will go to it for help.
- Thanks to the Python programing language。

## LICENSE

MIT.

See LICENSE.

[russ_cos_google_plus]: https://plus.google.com/+RussCox-rsc
[qart_article]: http://research.swtch.com/qart
[qr]: https://code.google.com/p/rsc/source/browse/qr
[dieforfree]: https://github.com/dieforfree
[qart4j]: https://github.com/dieforfree/qart4j
[tutorial]: http://www.thonky.com/qr-code-tutorial/
