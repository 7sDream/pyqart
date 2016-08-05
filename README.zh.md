# PyQArt - QArt 的  Python 实现

[English version](https://github.com/7sDream/pyqart/blob/master/README.md)

## 简介

QArt 是由 [Russ Cox][russ_cos_google_plus] 在他个人网站的[一篇文章][qart_article]中提出的一种将包含 URL 的二维码与图像结合的方法。

示例图片（来源于 Russ Cox 的文章）：

![QArt Example][qart_example]

这个库是 QArt 的 Python 实现版本。

## 安装

```bash
pip install pyqart
```

## 使用

为便于重用，我将库分成了两部分，一部分是普通二维码生成，另一部分则将 URL 二维码与图像结合。

### Qr 部分

使用 `pyqr` 命令行程序，可以创建普通二维码。

```
 pyqr -p 5 -c 102 204 255 "Hello World!" -o qr.png
```

其中：

- `-p` 参数指定生成的二维码图片中，每个填充点的大小，默认是 3 像素。
- `-c` 参数指定填充点的颜色，默认是黑色。背景色默认为白色，可以用 `-g` 参数设定。

![qr code: hello world][qr_in_image]

如果你想在终端里查看的话，不提供 `-o` 参数即可：

```bash
pyqr "Hello World"
```

输出如下：

![qr in terminal: hello world][qr_in_terminal]

显示效果和你终端的字体有关，我的字体是 Dejavu Sans Mono.

当然，终端中只能用于显示比较小的二维码。

有关二维码生成的更多参数请使用 `pyqr -h` 命令查看。

### Art 部分

使用 `pyqart` 命令行程序创建艺术二维码。（所需时间可能较长，请耐心等待）

使用我的博客网址和 Github 头像来做例子，`-v` 参数指定二维码的大小。

```
pyqart -v 8 "http://0v0.link/" photo.jpg -o qart.png
```

生成如下二维码，扫描一下就会跳转到我的博客啦：

![][my-qart-img]

可能效果不太好，试试使用 `-n` 参数来随机选取像素点（默认情况下会先处理大片相同颜色的区域），下面还同时设定了点的颜色：

```bash
pyqart -n -c 102 204 255 -v 8 "http://0v0.link/" photo.jpg -o qart-n.png
```

![][my-qart-n-img]

可能还是不太好？再试试 `-y` 参数通过放弃边缘区域来加强中间区域的逼近效果，：

```bash
pyqart -y -c 102 204 255 -v 8 "http://0v0.link/" photo.jpg -o qart-y.png
```

![][my-qart-y-img]

`-y` 和 `-n` 参数也可以结合起来使用，不过提升不会很明显。

### Python 内接口

文档正在编写中。

## TODO

- [x] 让 QrPainter 能自己决定参数
- [x] Art 部分
- [x] CLI
- [ ] 打包
- [ ] GUI
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
[qr_in_image]: http://ww3.sinaimg.cn/large/88e401f0gw1f6ir3ifivzj20370370ss.jpg
[qr_in_terminal]: http://ww2.sinaimg.cn/large/88e401f0gw1f6ir4taf7hj209008c3ze.jpg
[my-qart-img]: http://ww3.sinaimg.cn/large/88e401f0gw1f6ir8t0mbej20490490t2.jpg
[my-qart-n-img]: http://ww1.sinaimg.cn/large/88e401f0gw1f6irh15ouuj2049049mxp.jpg
[my-qart-y-img]: http://ww2.sinaimg.cn/large/88e401f0gw1f6irbnfjozj20490490t4.jpg
[qr]: https://code.google.com/p/rsc/source/browse/qr
[dieforfree]: https://github.com/dieforfree
[qart4j]: https://github.com/dieforfree/qart4j
[tutorial]: http://www.thonky.com/qr-code-tutorial/
