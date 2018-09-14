# -*- coding: utf-8 -*-
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QGraphicsDropShadowEffect
from PyQt5.QtGui import QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEventLoop, QTimer, QVariantAnimation, pyqtSlot, QVariant
import os
import time
import re
from urllib.request import urlopen


FONT_SIZE = 24
DISPLAY_AREA = 0.9
DISPLAY_TIME = 8000
INVL_TIME = 2000
WINDOW_OPACITY = 0.8
MAX_STR_LEN = 30
RAINBOW_RGB_LIST = ['#FF0000', '#FFA500', '#FFFF00',
                    '#00FF00', '#007FFF', '#0000FF', '#8B00FF']
RAINBOW_QRGB_LIST = [QColor(255, 0, 0), QColor(255, 165, 0), QColor(255, 255, 0), QColor(
    0, 255, 0), QColor(0, 127, 255), QColor(0, 0, 255), QColor(139, 0, 255)]
screenRect = None
screenWidth = None
screenHeight = None


class Danmu(QLabel):
    def __init__(self, text, color, y, parent=None):
        super(Danmu, self).__init__(parent)
        self.yPos = y
        text = re.sub(r'/Emoji\d+|/表情|^ | $', '',
                      text.replace('\n', ' '))[0:MAX_STR_LEN]
        self.setText(text)
        self.setFont(QFont('SimHei', FONT_SIZE, 100))
        pa = QPalette()
        pa.setColor(QPalette.Foreground, color)
        self.setPalette(pa)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowOpacity(WINDOW_OPACITY)
        if os.name == 'nt':
            self.setWindowFlags(Qt.FramelessWindowHint |
                                Qt.Tool | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint |
                                Qt.SubWindow | Qt.WindowStaysOnTopHint)

        self.eff = QGraphicsDropShadowEffect()
        self.eff.setBlurRadius(5)
        self.eff.setColor(QColor('#060606'))
        self.eff.setOffset(1.5, 1.5)
        self.setGraphicsEffect(self.eff)

        self.anim = QPropertyAnimation(self, b'geometry')
        self.setFixedSize(self.fontMetrics().boundingRect(self.text()).width(
        ) + 10, self.fontMetrics().boundingRect(self.text()).height())

    def speed(self):
        return (self.width() + screenWidth) / DISPLAY_TIME

    def showFlyDM(self, y=None):
        if y:
            self.yPos = y
        self.anim.setDuration(DISPLAY_TIME)
        self.anim.setStartValue(
            QRect(screenWidth - 1, self.yPos, self.width(), self.height()))
        self.anim.setEndValue(
            QRect(-self.width(), self.yPos, self.width(), self.height()))

        self.show()
        self.anim.start()

    def showFixedDM(self, y=None):
        if y:
            self.yPos = y
        self.anim.setDuration(DISPLAY_TIME)
        self.anim.setStartValue(
            QRect(int((screenWidth - self.width()) / 2), self.yPos, self.width(), self.height()))
        self.anim.setEndValue(
            QRect(int((screenWidth - self.width()) / 2), self.yPos, self.width(), self.height()))

        self.show()
        self.anim.start()


class DanmuManager:
    def __init__(self, display_area=0.8):
        self.flyDandaos = []
        self.topDandaos = []
        self.btmDandaos = []
        for _ in range(int(screenHeight * display_area / (FONT_SIZE + 20))):
            self.flyDandaos.append([])
            self.topDandaos.append([])
            self.btmDandaos.append([])

    def destroyDM(self):
        for dandao in self.flyDandaos:
            while dandao:
                if dandao[0][0] is not None and time.time() - dandao[0][1] > DISPLAY_TIME / 1000 + 2:
                    dandao[0][0].destroy()
                    dandao.pop(0)
                else:
                    break
        for dandao in self.topDandaos:
            while dandao:
                if dandao[0][0] is not None and time.time() - dandao[0][1] > DISPLAY_TIME / 1000 + 2:
                    dandao[0][0].destroy()
                    dandao.pop(0)
                else:
                    break
        for dandao in self.btmDandaos:
            while dandao:
                if dandao[0][0] is not None and time.time() - dandao[0][1] > DISPLAY_TIME / 1000 + 2:
                    dandao[0][0].destroy()
                    dandao.pop(0)
                else:
                    break

    def add(self, text):
        text, color, style = self.parse(text)
        flag = True if text else False
        if style == 'fly':
            danmu = Danmu(text, color, 1)
            v2 = danmu.speed()
            while flag:
                my_dandaos = self.flyDandaos
                for idx, dandao in enumerate(my_dandaos):
                    if flag and not dandao:
                        dandao.append(
                            (danmu, time.time())
                        )
                        dandao[-1][0].showFlyDM((FONT_SIZE + 20) * idx)
                        flag = False
                        break
                    else:
                        v1 = dandao[-1][0].speed()
                        min_interval_time = (
                            screenWidth + dandao[-1][0].width() - screenWidth * v1 / v2) / v1
                        min_interval_time = max(
                            min_interval_time, dandao[-1][0].width()/v1)
                        if flag and time.time() - dandao[-1][1] > min_interval_time / 1000:
                            dandao.append(
                                (danmu, time.time())
                            )
                            dandao[-1][0].showFlyDM((FONT_SIZE + 20) * idx)
                            flag = False
                            break
                if flag:
                    sleep(100)

        elif style == 'top':
            while flag:
                my_dandaos = self.topDandaos
                for idx, dandao in enumerate(my_dandaos):
                    if flag and (not dandao or time.time() - dandao[-1][1] > DISPLAY_TIME / 1000):
                        dandao.append(
                            (Danmu(text, color, (FONT_SIZE + 20) * idx), time.time())
                        )
                        dandao[-1][0].showFixedDM()
                        flag = False
                        break
                if flag:
                    sleep(100)

        elif style == 'btm':
            while flag:
                my_dandaos = self.btmDandaos
                for idx, dandao in enumerate(my_dandaos):
                    if flag and (not dandao or time.time() - dandao[-1][1] > DISPLAY_TIME / 1000):
                        dandao.append(
                            (Danmu(text, color, screenHeight - 30 -
                                   (FONT_SIZE + 20) * (1 + idx)), time.time())
                        )
                        dandao[-1][0].showFixedDM()
                        flag = False
                        break
                if flag:
                    sleep(100)

    def parse(self, text):
        textColor = QColor(240, 240, 240)
        style = 'fly'
        match_object = re.search(
            r'\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})', text)
        if match_object:
            textColor = QColor(int(match_object.group(1), 16), int(
                match_object.group(2), 16), int(match_object.group(3), 16))
            text = re.sub(r'\#[0-9a-fA-F]{6}', '', text)
        if re.search(r'\#top', text, re.I):
            style = 'top'
            text = re.sub(r'\#top', '', text, re.I)
        elif re.search(r'\#btm', text, re.I):
            style = 'btm'
            text = re.sub(r'\#btm', '', text, re.I)
        return text, textColor, style

class Footer(QLabel):
    CHANGE_TIMES = 20
    RAINBOW_QRGB_LIST = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 127, 255), (0, 0, 255), (139, 0, 255)]
    def __init__(self, text, parent=None):
        super(Footer, self).__init__(parent)
        self.changeIdx = 0
        self.clrIdx = 0
        self.changeRGB = [0,0,0]
        self.setText(text)
        self.setFont(QFont('SimHei', FONT_SIZE, 100))
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setWindowOpacity(WINDOW_OPACITY)
        if os.name == 'nt':
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow | Qt.WindowStaysOnTopHint)
        self.setFixedSize(self.fontMetrics().boundingRect(self.text()).width() + 10, self.fontMetrics().boundingRect(self.text()).height())
        self.setGeometry(QRect(screenWidth - self.width(), screenHeight - self.height() - 50, self.width(), self.height()))

        self.setColor()

        self.show()

    def setShadow(self):
        pa = QPalette()
        pa.setColor(QPalette.Foreground, QColor(0,0,0))
        self.setPalette(pa)
        self.eff = QGraphicsDropShadowEffect()
        self.eff.setBlurRadius(5)
        self.eff.setColor(QColor('#060606'))
        self.eff.setOffset(1.5, 1.5)
        self.setGraphicsEffect(self.eff)

    def setColor(self):
        if self.changeIdx < Footer.CHANGE_TIMES:
            pa = QPalette()
            pa.setColor(QPalette.Foreground, QColor(
                Footer.RAINBOW_QRGB_LIST[self.clrIdx][0] + self.changeRGB[0] / Footer.CHANGE_TIMES * self.changeIdx,
                Footer.RAINBOW_QRGB_LIST[self.clrIdx][1] + self.changeRGB[1] / Footer.CHANGE_TIMES * self.changeIdx,
                Footer.RAINBOW_QRGB_LIST[self.clrIdx][2] + self.changeRGB[2] / Footer.CHANGE_TIMES * self.changeIdx
            ))
            self.setPalette(pa)
            self.changeIdx += 1
            self.show()
        else:
            self.changeIdx = 0
            self.clrIdx = 0 if self.clrIdx == 6 else self.clrIdx + 1
            self.getChangeRGB(Footer.RAINBOW_QRGB_LIST[self.clrIdx], Footer.RAINBOW_QRGB_LIST[(self.clrIdx + 1) % 7])
    
    def getChangeRGB(self, clr1, clr2):
        self.changeRGB = [clr2[0] - clr1[0], clr2[1] - clr1[1], clr2[2] - clr1[2]]


def sleep(ms):
    loop = QEventLoop()
    QTimer.singleShot(ms, loop.quit)
    loop.exec()


if __name__ == '__main__':
    print("Started")
    app = QApplication(sys.argv)
    screenRect = QDesktopWidget.screenGeometry(QApplication.desktop())
    screenWidth = screenRect.width()
    screenHeight = screenRect.height()

    danmu_manager = DanmuManager(DISPLAY_AREA)
    danmu_manager.add('Hello, world!')

    footerShadow = Footer("Live Danmu powered by JI-Tech (zyayoung, BoYanZh)")
    footerShadow.setShadow()
    footer = Footer("Live Danmu powered by JI-Tech (zyayoung, BoYanZh)")
    
    while True:
        footer.setColor()
        danmu_manager.destroyDM()
        message = urlopen('http://127.0.0.1:5000/get').read().decode('utf-8')
        if message != 'Error:Empty':
            loopTime = 1
            matchObj = re.search(
                r'\#time(\d+)', message)
            if matchObj:
                RAINBOW_RGB_LIST_INDEX = 0
                loopTime = max(min(50, int(matchObj.group(1))), 1)
                message = re.sub('\#time\d+', '', message)
                if not re.search(r'\#[0-9a-fA-F]{6}', message):
                    for _ in range(loopTime):
                        danmu_manager.add(
                            RAINBOW_RGB_LIST[RAINBOW_RGB_LIST_INDEX] + message)
                        RAINBOW_RGB_LIST_INDEX = 0 if RAINBOW_RGB_LIST_INDEX == 6 else RAINBOW_RGB_LIST_INDEX + 1
                else:
                    for _ in range(loopTime):
                        danmu_manager.add(message)
                        RAINBOW_RGB_LIST_INDEX = 0 if RAINBOW_RGB_LIST_INDEX == 6 else RAINBOW_RGB_LIST_INDEX + 1
            else:
                danmu_manager.add(message)
        else:
            sleep(200)
