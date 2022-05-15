import  sys

import pyperclip
import pytesseract
from PIL import Image
import translators as ts
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

try:
    from pynotifier import Notification
except ImportError:
    pass

class QTextEditDemo(QWidget):
    def __init__(self):
        super(QTextEditDemo,self).__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("截图翻译")
        self.resize(300,320)
        self.move(0,200)
        self.textEdit = QTextEdit()
        self.textEdit1 = QTextEdit()
        self.buttonText = QPushButton("截图")
 
        layout = QVBoxLayout()
        layout.addWidget(self.textEdit)
        layout.addWidget(self.textEdit1)
        layout.addWidget(self.buttonText)
     
        self.setLayout(layout)
 
        self.buttonText.clicked.connect(self.onClick_ButtonText)
        # self.textEdit.setPlainText("Hello World")
        # 最小化
        # self.buttonText1.clicked.connect(self.showMinimized)
        
    def onClick_ButtonText(self):
        self.hide()
        win.show()

class WScreenShot(QWidget):
    def __init__(self, parent=None):
        super(WScreenShot, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet('''background-color:black; ''')
        self.setWindowOpacity(0.4)
        # 1 透明度的有效范围从1.0 完全不透明到0.0 完全透明
        # 2 默认情况下是不透明状态，属性值为1.0

        desktopRect = QDesktopWidget().screenGeometry()
        # 获取屏幕的信息
        # screenGeometry（）函数提供有关可用屏幕几何的信息
        self.setGeometry(desktopRect)
        # setGeometry (9,9, 50, 25)
        # 从屏幕上（9，9）位置开始（即为最左上角的点），显示一个50*25的界面（宽50，高25）
        # setGeometry之后一定要调用show函数，否则可能看不到控件存在
        self.setCursor(Qt.ArrowCursor)  # 设置鼠标形状

        self.blackMask = QBitmap(desktopRect.size())
        self.blackMask.fill(Qt.black)
        self.mask = self.blackMask.copy()


        self.isDrawing = False
        self.startPoint = QPoint()
        self.endPoint = QPoint()
        self.setMouseTracking(False)
        self.startX, self.startY = 0, 0  # the point where you start
        self.endX, self.endY = 0, 0  # the point where you end

    def paintEvent(self, event):
        if self.isDrawing:
            self.mask = self.blackMask.copy()
            pp = QPainter(self.mask)
            pen = QPen()
            pen.setStyle(Qt.NoPen)
            pp.setPen(pen)
            brush = QBrush(Qt.white)
            pp.setBrush(brush)
            pp.drawRect(QRect(self.startPoint, self.endPoint))  # 画图
            self.setMask(QBitmap(self.mask))

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.startPoint = event.pos()
            self.startX, self.startY = event.x(), event.y()
            # print("mousepress: ", self.startPoint)
            self.endPoint = self.startPoint
            self.isDrawing = True

    def mouseMoveEvent(self, event):
        if self.isDrawing:
            self.endPoint = event.pos()
            self.endX, self.endY = event.x(), event.y()
            self.update()

    def mouseReleaseEvent(self, event):
        result_str = ""
        fy_str = ""
        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos()
            # print("mouse release: ", self.endPoint)
            # PySide2
            # screenshot = QPixmap.grabWindow(QApplication.desktop().winId())
            # PyQt5
            # screenshot = QApplication.primaryScreen().grabWindow(0)
            # 通用
            screenshot = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
            # rect = QRect(self.startPoint, self.endPoint)
            # rect = QRect(self.startX, self.startY + 28, self.endX-self.startX, self.endY-self.startY)
            rect = QRect(
                min(self.startX, self.endX),
                min(self.startY, self.endY),
                abs(self.startX - self.endX),
                abs(self.startY - self.endY)
            )
            # print("last rect:", rect)
            outputRegion = screenshot.copy(rect)
            try:
                outputRegion.save('111.jpg', format='JPG', quality=100)
            except Exception as e:
                print("保存截图失败！！！")
                notify("保存截图失败！！！")
            # print("ok")
            self.close()
            try:
                pil_img = Image.open('111.jpg')
            except Exception as e:
                print("读取截图失败！！！")
                notify("读取截图失败！！！")
            try:
                result = pytesseract.image_to_string(
                    pil_img, timeout=5, lang=(sys.argv[1] if len(sys.argv) > 1 else None)
                ).strip()
            except RuntimeError as error:
                print(f"ERROR: An error occurred when trying to process the image: {error}")
                notify(f"识别失败！！！")
                return

            if result:
                result_str = result
                # 内容复制到剪贴板
                pyperclip.copy(result)
                print(f'INFO: Copied "{result}" to the clipboard')
                # notify(f'Copied "{result}" to the clipboard')
            else:
                print(f"INFO: Unable to read text from image, did not copy")
                notify(f"Unable to read text from image, did not copy")
            
            main_demo.textEdit.setPlainText(result_str)
            try:
                fy_str = ts.google(result_str,to_language='zh')
            except Exception as e:
                print("翻译出错！！！")
                notify("翻译出错！！！")
            main_demo.textEdit1.setPlainText(fy_str)
            main_demo.show()
    
def notify(msg):
    try:
        Notification(title="TextShot", description=msg).send()
    except (SystemError, NameError):
        trayicon = QSystemTrayIcon(
            QIcon(
                QPixmap.fromImage(QImage(1, 1, QImage.Format_Mono))
            )
        )
        trayicon.show()
        trayicon.showMessage("TextShot", msg, QSystemTrayIcon.NoIcon)
        trayicon.hide()

if __name__ == "__main__":
    
    app = QApplication(sys.argv)
   
    main_demo = QTextEditDemo()
    main_demo.show()
    
    try:
        pytesseract.get_tesseract_version()
    except EnvironmentError:
        print(
            "ERROR: Tesseract is either not installed or cannot be reached.\n"
            "Have you installed it and added the install directory to your system path?"
        )
        sys.exit()
    win = WScreenShot()

    sys.exit(app.exec_())