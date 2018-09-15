from PyQt5.QtWidgets import QLabel, QGraphicsDropShadowEffect, QFrame
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import QPropertyAnimation, QRect

class RunLabel(QFrame):
    CHANGE_TIMES = 20
    RAINBOW_RGB_LIST = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 127, 255), (0, 0, 255),
                        (139, 0, 255)]

    def __init__(self, parent, text, color, screenWidth, screenHeight):
        super().__init__(parent)
        self.changeIdx = 0
        self.clrIdx = 0
        self.changeRGB = [0, 0, 0]
        self.label = QLabel(self)
        self.label.left = 0
        self.initUi(text, color, screenWidth, screenHeight)

    def initUi(self, text, color, screenWidth, screenHeight):
        # self.setStyleSheet("border:1px solid blue;")
        self.setFont(QFont('SimHei', 24, 100))
        self.myRect = self.fontMetrics().boundingRect(text)
        self.setGeometry(screenWidth - self.myRect.width() - 40, screenHeight - self.height() - 60,
                         self.myRect.width() + 20, self.myRect.height() + 10)
        self.initLabel(self.label, text + " " + text)
        self.label.anim = QPropertyAnimation(self.label, b'geometry')
        self.label.anim.setDuration(8000)
        self.label.anim.setStartValue(
            QRect(0, 0, self.fontMetrics().boundingRect(text + " " + text).width() + 20, self.myRect.height() + 10))
        self.label.anim.setEndValue(
            QRect(- self.width(), 0, self.fontMetrics().boundingRect(text + " " + text).width() + 20,
                  self.myRect.height() + 10))
        self.label.anim.setLoopCount(-1)
        self.label.anim.start()
        # self.label.setStyleSheet("border:1px solid red;")
        self.getChangeRGB(self.RAINBOW_RGB_LIST[self.clrIdx], self.RAINBOW_RGB_LIST[(self.clrIdx + 1) % 7])
        self.label.show()

    def initLabel(self, label, text):
        label.setText(text)
        label.setFont(QFont('SimHei', 24, 100))
        eff = QGraphicsDropShadowEffect()
        eff.setColor(QColor(6, 6, 6))
        eff.setBlurRadius(5)
        eff.setOffset(1.5, 1.5)
        label.setGraphicsEffect(eff)
        label.setGeometry(0, 0, self.fontMetrics().boundingRect(text).width() + 20,
                          self.fontMetrics().boundingRect(text).height() + 10)

    def changeLabel(self):
        if self.changeIdx < self.CHANGE_TIMES:
            pa = QPalette()
            pa.setColor(QPalette.Foreground, QColor(
                self.RAINBOW_RGB_LIST[self.clrIdx][0] + self.changeRGB[0] / self.CHANGE_TIMES * self.changeIdx,
                self.RAINBOW_RGB_LIST[self.clrIdx][1] + self.changeRGB[1] / self.CHANGE_TIMES * self.changeIdx,
                self.RAINBOW_RGB_LIST[self.clrIdx][2] + self.changeRGB[2] / self.CHANGE_TIMES * self.changeIdx
            ))
            self.label.setPalette(pa)
            self.changeIdx += 1
            self.show()
        else:
            self.changeIdx = 0
            self.clrIdx = 0 if self.clrIdx == 6 else self.clrIdx + 1
            self.getChangeRGB(self.RAINBOW_RGB_LIST[self.clrIdx], self.RAINBOW_RGB_LIST[(self.clrIdx + 1) % 7])

    def setShadow(self, color, blurRadius, offset):
        self.eff = QGraphicsDropShadowEffect()
        self.eff.setColor(color)
        self.eff.setBlurRadius(blurRadius)
        self.eff.setOffset(offset, offset)
        self.setGraphicsEffect(self.eff)

    def getChangeRGB(self, clr1, clr2):
        self.changeRGB = [clr2[0] - clr1[0], clr2[1] - clr1[1], clr2[2] - clr1[2]]
