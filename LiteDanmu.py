# -*- coding: utf-8 -*-
import sys
import argparse
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from Danmu.MessageQueueManager import MessageQueueManager
from Danmu.DanmuManager import DanmuManager
from Danmu.Marquee import Marquee
from Danmu.App import App
from Danmu.config import *
from Danmu.utils import *


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-serverurl', type=str, default='http://127.0.0.1:5000/', help='server url')
    parser.add_argument('-sk', type=str, default='YourSecretKey', help='secret key')
    args = parser.parse_args()

    app = QApplication(sys.argv)
    screenRect = QDesktopWidget.screenGeometry(QApplication.desktop())
    screenWidth = screenRect.width()
    screenHeight = screenRect.height()
    ex = App(screenWidth, screenHeight)

    MyMessageQueueManager = MessageQueueManager(args.serverurl, args.sk)
    MyDanmuManager = DanmuManager(ex, screenWidth, screenHeight)
    MyDanmuManager.addDanmu("Hello, World!")
    MyMarquee = Marquee(ex, FOOTER_TEXT, QColor(255, 0, 0), screenWidth, screenHeight)

    tictoc = True
    while True:
        # loop every 100ms
        if tictoc:
            # refresh Ui
            # ex.raise_()
            MyDanmuManager.cleanDanmu()
            MyMarquee.changeColor()
        else:
            # get new message
            MyMessageQueueManager.add2DanmuManager(MyDanmuManager)
            MyDanmuManager.showDanmu()
        tictoc = not tictoc
        sleep(0.1)
