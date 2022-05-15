# screenshot-translation-python 截图翻译-python实现
因为看到TextShot和translators两个python的github项目，想着可以做一个截图翻译软件，于是合了一下 [pyqt5 截屏,图片识别文字](https://www.cnblogs.com/g2thend/p/14333468.html) 的代码

## 准备工作
需要先安装 Tesseract OCR，并且加入Path路径  
[Tesseract OCR下载地址](https://digi.bib.uni-mannheim.de/tesseract/)

python需要的库
```txt
Pillow==9.1.0
PyQt5==5.15.6
PyQt5-sip==12.10.1
PyQt5-stubs==5.15.6.0
py-notifier==0.3.2
pyperclip==1.8.2
pytesseract==0.3.9
win10toast==0.9; platform_system == "Windows"
translators==5.1.1
```
最后可以用 pyinstaller 打包一下程序，然后到dist目录中项目文件夹下找到exe执行程序，然后把这个执行程序创建桌面快捷方式就可以了
```base
# -w是无显示终端
pyinstaller xxx.py -w
```

参考资料：  
[translators](https://github.com/UlionTse/translators)  
[TextShot](https://github.com/ianzhao05/textshot)  
[pyqt5 截屏,图片识别文字](https://www.cnblogs.com/g2thend/p/14333468.html)
