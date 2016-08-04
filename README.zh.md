# PyQArt - QArt 的  Python 实现

[English version](https://github.com/7sDream/pyqart/blob/master/README.md)

## 简介

QArt 是由 [Russ Cox][russ_cos_google_plus] 在他个人网站的[一篇文章][qart_article]中提出的一种将包含 URL 的二维码与图像结合的方法。

示例图片（来源于 Russ Cox 的文章）：

![QArt Example][qart_example]

这个库是 QArt 的 Python 实现版本。

## 使用

为便于重用，我将库分成了两部分，一部分是普通二维码生成，另一部分则将 URL 二维码与图像结合。

**然而！art 部分我还没实现。但是我觉得 qr 部分已经可用了，先放上来。**

### Qr 部分

```python
from pyqart import QrImagePrinter

QrImagePrinterQr.print(
    "Hello world!",     # 要编码的数据
    "qr.png",           # 输出文件名
    2,                  # 二维码图片中「点」的大小（以像素为单位）
    5,                  # 边框大小（以像素为单位）
    (102, 204, 255),    # 前景色
                        # 背景色没有设置，将会使用默认的白色
)
```

一行代码，你就可以生成出一张二维码图片：

![qr code: hello world][qr_in_image]

如果你想在终端里查看的话，请使用 StringPrinter：

```python
from pyqart import QrStringPrinter

QrStringPrinter.print(painter)
```

输出如下：

![qr in terminal: hello world][qr_in_terminal]

显示效果和你终端的字体有关，我的字体是 Dejavu Sans Mono.

当然 StringPrinter 只能用于显示比较小的二维码。

### Art 部分

已完成，正在设计合适的接口。

## TODO

- [x] 让 QrPainter 能自己决定参数
- [x] Art 部分
- [ ] CLI
- [ ] GUI
- [ ] 打包
- [ ] 使用 Cython 加快里德所罗门码编码速度
- [ ] 文档
- [ ] 测试

## 其他实现版本

- Golang: [qr][qr] by [Russ Cox][russ_cos_google_plus]
- Java: [qart4j][qart4j] by [dieforfree][dieforfree]

## 致谢

- 所有一切都源自 [Russ Cos][russ_cos_google_plus] 的文章，感谢他。
- 感谢 [dieforfree][dieforfree] 的 [qart4j 项目][qart4j]，它给我提供了很多如何实现 art 部分参考。
- 感谢 thonky.com 的 [二维码原理指导][tutorial] 系列文章，非常详细，关于编码和纠错中不懂的地方多亏了它。
- 感谢 Python。

## 协议

MIT。

参见 LICENSE 文件。

[russ_cos_google_plus]: https://plus.google.com/+RussCox-rsc
[qart_article]: http://research.swtch.com/qart
[qart_example]: http://ww4.sinaimg.cn/large/88e401f0gw1f6dl845naoj205g05ga9y.jpg
[qr_in_image]: http://ww4.sinaimg.cn/large/88e401f0gw1f6dmbn4xp6j205u05u0t4.jpg
[qr_in_terminal]: http://ww3.sinaimg.cn/large/88e401f0gw1f6e95v7ebmj20di099dh7.jpg
[qr]: https://code.google.com/p/rsc/source/browse/qr
[dieforfree]: https://github.com/dieforfree
[qart4j]: https://github.com/dieforfree/qart4j
[tutorial]: http://www.thonky.com/qr-code-tutorial/
