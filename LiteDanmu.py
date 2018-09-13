import sys
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEventLoop, QTimer
import os
import time
import re
from urllib.request import urlopen
import threading
from queue import Queue


FONT_SIZE = 24
DISPLAY_AREA = 0.8
DISPLAY_TIME = 8000
INVL_TIME = 2000
WINDOW_ALPHA = 0.8
MAX_STR_LEN = 30
screenRect = None
screenWidth = None
screenHeight = None


class Danmu(QLabel):
    def __init__(self, text, color, y, parent=None):
        super(Danmu, self).__init__(parent)
        text = text[0:MAX_STR_LEN]
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

        self.eff = QGraphicsDropShadowEffect()
        self.eff.setBlurRadius(0)
        self.eff.setColor(QColor("#000000"))
        self.eff.setOffset(2, 2)
        self.setGraphicsEffect(self.eff)

        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(DISPLAY_TIME)
        self.setFixedSize((FONT_SIZE + 20) * len(text),FONT_SIZE + 20)
        self.anim.setStartValue(
            QRect(screenWidth-1, y, self.width(), FONT_SIZE + 20))
        self.anim.setEndValue(
            QRect(-self.width(), y, self.width(), FONT_SIZE + 20))
        
        self.show()
        self.anim.start()


class DanmuManager:
    def __init__(self, display_area=0.8):
        self.dandaos = []
        for _ in range(int(screenHeight * display_area / (FONT_SIZE + 20))):
            self.dandaos.append([])

    def add(self, text):
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
                    text, color = self.parse(text)
                    text = text.strip().replace('\n',' ')
                    if text:
                        dandao.append(
                            (Danmu(text, color, (FONT_SIZE + 20)*idx), time.time())
                        )
                    flag = False
            loop = QEventLoop()
            QTimer.singleShot(100, loop.quit)
            loop.exec()

    def parse(self, text):
        if re.search("^\#[0-9a-fA-F]{6} +", text):
            r = int(text[1:3], 16)
            g = int(text[3:5], 16)
            b = int(text[5:7], 16)
            return re.sub("^\#[0-9a-fA-F]{6} +","",text), QColor(r, g, b)
        else:
            return text, QColor(240, 240, 240)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screenRect = QDesktopWidget.screenGeometry(QApplication.desktop())
    screenWidth = screenRect.width()
    screenHeight = screenRect.height()

    danmu_manager = DanmuManager(DISPLAY_AREA)

    danmu_manager.add('Hello, world!')

    # Test
    while True:
        loop = QEventLoop()
        QTimer.singleShot(50, loop.quit)
        loop.exec()
        message = urlopen('http://127.0.0.1:5000/get').read().decode('utf-8')
        if message != 'Error:Empty':
            danmu_manager.add(message)
        else:
            loop = QEventLoop()
            QTimer.singleShot(200, loop.quit)
            loop.exec()
