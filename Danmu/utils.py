from PyQt5.QtCore import QEventLoop, QTimer


def sleep(s):
    loop = QEventLoop()
    QTimer.singleShot(int(s * 1000), loop.quit)
    loop.exec()
