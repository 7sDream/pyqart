# PyQArt - Python implement of QArt

[中文版 README](https://github.com/7sDream/pyqart/blob/master/README.zh.md)

## introduction

QArt is a method of combining QrCode of an URL with any image, which was submitted in [an article][qart_article] writen by [Russ Cox][russ_cos_google_plus] on his personal website.

An Example(come from the article):

![QArt Example][qart_example]

And this repo is Python implement of it.

## Usage

For code reues, I split the lib to two part. One for generate normal QrCode, another is the Art part - mix Qr it with image.

**BUT! Art part is under construction, now just the Qr part is usable.**

### The Qr Part

```python
from pyqart import QrData, QrPainter, ImagePrinter

# create data set
data = QrData()

# you can call this several times to add data
data.put_string("Hello world!")

# give data to a painter to draw them to QrCode
# version=None means let painter decide size of QrCode by data size
# mask argument is stand for data mask flag, from 0 to 7
painter = QrPainter(data, version=None, mask=0)

# printer print painter's painting to a image.
ImagePrinter.print(painter, "qr.png", 200, 5, (102, 204, 255))
```

Then you will get a QrCode image on current directory whose:

- Filename is qr.png.
- Size of code part is 200x200. 
- Board width 5 pixels.
- Background is white(which is the default value).
- Front color is Tianyi Blue(name of color (102, 204, 255)).

Like bellow:

![qr code: hello world][qr_in_image]

If you want show it in terminal, please use StringPrinter：

```python
from pyqart import QrArgs, QrPainter, StringPrinter

# just like last example

# ...

print(StringPrinter.print(painter))
```

Then you will see:

![qr in terminal: hello world][qr_in_terminal]

The actual result you will see depends on your font setting, I'm using Dejavu Sans Mono.

Yes, StringPrinter is useful for **only small QrCodes**. 

### The Art Part

I'm working on it.

## TODO

- [x] Make QrPainter decided argument by itself.
- [ ] Art part
- [ ] CLI
- [ ] GUI
- [ ] doc
- [ ] Package
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

[russ_cos_google_plus]: https://plus.google.com/+RussCox-rsc
[qart_article]: http://research.swtch.com/qart
[qart_example]: http://ww4.sinaimg.cn/large/88e401f0gw1f6dl845naoj205g05ga9y.jpg
[qr_in_image]: http://ww4.sinaimg.cn/large/88e401f0gw1f6dmbn4xp6j205u05u0t4.jpg
[qr_in_terminal]: http://ww3.sinaimg.cn/large/88e401f0gw1f6e95v7ebmj20di099dh7.jpg
[qr]: https://code.google.com/p/rsc/source/browse/qr
[dieforfree]: https://github.com/dieforfree
[qart4j]: https://github.com/dieforfree/qart4j
[tutorial]: http://www.thonky.com/qr-code-tutorial/
