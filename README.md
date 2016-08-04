# PyQArt - Python implement of QArt

[中文版 README](https://github.com/7sDream/pyqart/blob/master/README.zh.md)

## introduction

QArt is a method of combining QrCode of an URL with any image, which was submitted in [an article][qart_article] writen by [Russ Cox][russ_cos_google_plus] on his personal website.

An Example(come from the article):

![QArt Example][qart_example]

And this repo is Python implement of it.

## Usage

For code reues, I split the lib to two part. One for generate normal QrCode, another is the Art part - mix QrCode of URL with image.

**BUT! Art part is under construction, now just the Qr part is usable.**

### The Qr Part

```python
from pyqart import QrImagePrinter

QrImagePrinterQr.print(
    "Hello world!",     # data
    "qr.png",           # file name
    2,                  # size of every "Point" of QrCode, by pixel
    5,                  # QrCode board width by pixel
    (102, 204, 255),    # front color
                        # no background color provided, use default(white)
)
```

Just from one line of code like above, you can get a QrCode image :

![qr code: hello world][qr_in_image]

If you want show it in terminal, please use StringPrinter：

```python
from pyqart import QrStringPrinter

QrStringPrinter.print("Hello world!")
```

Then you will see:

![qr in terminal: hello world][qr_in_terminal]

The actual result you will see depends on your font setting, I'm using Dejavu Sans Mono.

Yes, StringPrinter is useful for **only small QrCodes**. 

### The Art Part

Finished, I'm designing appropriate interface parameters.

## TODO

- [x] Make QrPainter decided argument by itself.
- [x] Art part
- [ ] CLI
- [ ] GUI
- [ ] Package
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

[russ_cos_google_plus]: https://plus.google.com/+RussCox-rsc
[qart_article]: http://research.swtch.com/qart
[qart_example]: http://ww4.sinaimg.cn/large/88e401f0gw1f6dl845naoj205g05ga9y.jpg
[qr_in_image]: http://ww4.sinaimg.cn/large/88e401f0gw1f6dmbn4xp6j205u05u0t4.jpg
[qr_in_terminal]: http://ww3.sinaimg.cn/large/88e401f0gw1f6e95v7ebmj20di099dh7.jpg
[qr]: https://code.google.com/p/rsc/source/browse/qr
[dieforfree]: https://github.com/dieforfree
[qart4j]: https://github.com/dieforfree/qart4j
[tutorial]: http://www.thonky.com/qr-code-tutorial/
