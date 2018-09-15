import os
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from Danmu.config import *


class App(QWidget):
    def __init__(self, screenWidth, screenHeight):
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
