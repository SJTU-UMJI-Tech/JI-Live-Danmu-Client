import sys
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEventLoop, QTimer
import os
import time
from urllib.request import urlopen
import threading
from queue import Queue


FONT_SIZE = 24
DISPLAY_AREA = 0.8
DISPLAY_TIME = 8000
INVL_TIME = 2000
WINDOW_ALPHA = 0.8
screenRect = None
screenWidth = None
screenHeight = None


class Danmu(QLabel):
    def __init__(self, text, color, y, parent=None):
        super(Danmu, self).__init__(parent)
        self.setText(text)
        self.setFont(QFont("SimHei", FONT_SIZE, 100))
        pa = QPalette()
        pa.setColor(QPalette.Foreground, color)
        self.setPalette(pa)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowOpacity(WINDOW_ALPHA)
        if os.name == 'nt':
            self.setWindowFlags(Qt.FramelessWindowHint |
                                Qt.Tool | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint |
                                Qt.SubWindow | Qt.WindowStaysOnTopHint)

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(DISPLAY_TIME)
        self.anim.setStartValue(
            QRect(screenWidth-1, y, self.width(), FONT_SIZE + 20))
        self.anim.setEndValue(
            QRect(-self.width(), y, self.width(), FONT_SIZE + 20))
        self.showNormal()
        self.anim.start()


class DanmuManager:
    def __init__(self, display_area=0.8):
        self.dandaos = []
        for _ in range(int(screenHeight * display_area / (FONT_SIZE + 20))):
            self.dandaos.append([])

    def add(self, text, color=QColor(127, 9, 9)):
        # print(self.dandaos)
        flag = True
        while flag:
            for idx, dandao in enumerate(self.dandaos):
                while dandao:
                    if time.time() - dandao[0][1] > DISPLAY_TIME / 1000 + 2:
                        dandao[0][0].destroy()
                        dandao.pop(0)
                    else:
                        break
                if flag and (not dandao or time.time() - dandao[-1][1] > INVL_TIME / 1000):
                    dandao.append(
                        (Danmu(text, color, (FONT_SIZE + 20)*idx), time.time())
                    )
                    flag = False
            loop = QEventLoop()
            QTimer.singleShot(100, loop.quit)
            loop.exec()


def refresh(app):
    while True:
        time.sleep(1/10)
        app.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screenRect = QDesktopWidget.screenGeometry(QApplication.desktop())
    screenWidth = screenRect.width()
    screenHeight = screenRect.height()

    danmu_manager = DanmuManager(DISPLAY_AREA)

    danmu_manager.add('Hello, world!')

    # Test
    for i in range(1000):
        loop = QEventLoop()
        QTimer.singleShot(100, loop.quit)
        loop.exec()
        message = urlopen('http://127.0.0.1:5000/get').read().decode('utf-8')
        if message != 'Error:Empty':
            danmu_manager.add(message)

    sys.exit(app.exec_())
