# -*-coding:utf-8 -*-
from PyQt5.QtCore import QEventLoop, QTimer


# sleep in Qt
def sleep(s):
    loop = QEventLoop()
    QTimer.singleShot(int(s * 1000), loop.quit)
    loop.exec()
