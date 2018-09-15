# -*- coding: utf-8 -*-
import sys, time, re, os, sip
from Danmu.MessageQueueManager import MessageQueueManager
from Danmu.DanmuManager import DanmuManager
from Danmu.RunLabel import RunLabel
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QGraphicsDropShadowEffect, QWidget, QFrame
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEventLoop, QTimer
from Danmu.config import *

myWindow = None

class App(QWidget):
    def __init__(self):
        global myWindow
        super().__init__()
        myWindow = self
        self.left = 0
        self.top = 0
        self.width = screenWidth
        self.height = screenHeight
        if os.name == 'nt':
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowOpacity(WINDOW_OPACITY)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()


def sleep(s):
    loop = QEventLoop()
    QTimer.singleShot(int(s * 1000), loop.quit)
    loop.exec()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screenRect = QDesktopWidget.screenGeometry(QApplication.desktop())
    screenWidth = screenRect.width()
    screenHeight = screenRect.height()
    ex = App()

    mq = MessageQueueManager()
    danmu_manager = DanmuManager(ex, screenWidth, screenHeight)
    danmu_manager.add("Hello, World!")
    rlbl = RunLabel(ex, FOOTER_TEXT, QColor(255, 0, 0), screenWidth, screenHeight)
    while True:
        # loop every 100ms
        ex.raise_()
        danmu_manager.destroyDM()
        rlbl.changeLabel()
        mq.push_all_message_to_danmu_manager(danmu_manager)
        danmu_manager.show()
        sleep(0.1)

