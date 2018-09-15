# -*- coding: utf-8 -*-
import sys
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QDesktopWidget
from Danmu.MessageQueueManager import MessageQueueManager
from Danmu.DanmuManager import DanmuManager
from Danmu.RunLabel import RunLabel
from Danmu.App import App
from Danmu.config import *
from Danmu.utils import *


if __name__ == '__main__':
    app = QApplication(sys.argv)
    screenRect = QDesktopWidget.screenGeometry(QApplication.desktop())
    screenWidth = screenRect.width()
    screenHeight = screenRect.height()
    ex = App(screenWidth, screenHeight)

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
        sleep(0.01)

