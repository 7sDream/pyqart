# pyqart - QArt 的  Python 实现

[English version]((https://github.com/7sDream/pyqart/blob/master/README.md))

## 简介

QArt 是由 [Russ Cox][russ_cos_google_plus] 在他个人网站的[一篇文章][qart_article]中提出的一种将包含 URL 的二维码与图像结合的方法。

示例图片（来源于 Russ Cox 的文章）：

![QArt Example](http://ww4.sinaimg.cn/large/88e401f0gw1f6dl845naoj205g05ga9y.jpg)

这个库是 QArt 的 Python 实现版本。

## 使用

为便于重用，我将库分成了两部分，一部分是普通二维码生成，另一部分则将 URL 二维码与图像结合。

**然而！art 部分我还没实现。但是我觉得 qr 部分已经可用了，先放上来。**

### qr 部分

```
from pyqart import QrArgs, QrPainter, ImagePrinter

# set QrCode arguments
args = QrArgs(
    1,  # 二维码版本，决定二维码的大小和能存放的最大字节数
    0,  # 纠错等级，范围 0 - 3
    0,  # 数据部分掩码， 范围 0 - 7
)

# 创建一个把数据画在二维码上的画家
painter = QrPainter(args)

# 给画家一些数据
painter.put_string("Hello world!")

# 打印机将画出的二维码打印（显示）出来
ImagePrinter.print(
    painter,
    bgcolor=(255, 255, 255),
    fcolor=(102, 204, 255),
    code_width=200,
    border_width=5,
    path='qr.png'
)
```

你将的在当前目录得到一张:

- 内部大小 200x200
- 边框宽度 5 像素
- 背景色为白色
- 前景色为天依蓝
- 名为 qr.png

的二维码图片：

![qr code: hello world](http://ww4.sinaimg.cn/large/88e401f0gw1f6dmbn4xp6j205u05u0t4.jpg)

如果你想在终端里查看的话，请使用 StringPrinter：

```
from pyqart import QrArgs, QrPainter, StringPrinter

# just like last example

# ...

print(StringPrinter.print(painter))
```

输出如下：

![qr in terminal: hello world](http://ww4.sinaimg.cn/large/88e401f0gw1f6dmg4d14bj20ja0dowft.jpg)

显示效果和你终端的字体有关，我的字体是 Dejavu Sans Mono.

当然 StringPrinter 只能用于显示比较小的二维码。

### art 部分

还在编写中。

## TODO

- [ ] Art 部分
- [ ] CLI
- [ ] GUI
- [ ] 文档
- [ ] 打包
- [ ] 测试

## 其他实现版本

- Golang: [qr] by [Russ Cox][russ_cos_google_plus]
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
[dieforfree]: https://github.com/dieforfree
[qart4j]: https://github.com/dieforfree/qart4j
[tutorial]: http://www.thonky.com/qr-code-tutorial/
