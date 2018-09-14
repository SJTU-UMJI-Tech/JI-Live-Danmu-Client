# -*- coding: utf-8 -*-
import sys, time, re, os, threading as td
from urllib.request import urlopen
from PyQt5.QtWidgets import QApplication, QLabel, QDesktopWidget, QGraphicsDropShadowEffect, QWidget
from PyQt5.QtGui import QFont, QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEventLoop, QTimer, QVariantAnimation, pyqtSlot, QVariant

MAX_STR_LEN = 30
FONT_SIZE = 24
WINDOW_OPACITY = 0.8
DISPLAY_TIME = 8000
RAINBOW_RGB_LIST = ['#FF0000', '#FFA500', '#FFFF00',
                    '#00FF00', '#007FFF', '#0000FF', '#8B00FF']
screenRect = None
screenWidth = None
screenHeight = None

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
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.show()
 
class Danmu(QLabel):
    def __init__(self, text, color, top):
        global myWindow
        super(Danmu, self).__init__(myWindow)
        self.top = top
        text = re.sub(r'/Emoji\d+|/表情|^ | $', '', text.replace('\n', ' '))[0:MAX_STR_LEN]
        self.setTextFormat(Qt.PlainText)
        self.setText(text)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setFont(QFont('SimHei', FONT_SIZE, 100))
        myRect = self.fontMetrics().boundingRect(text)
        self.setFixedSize(myRect.width() + 20, myRect.height() + 10)
        self.setColor(color)
        self.setShadow(QColor('#060606'), 5, 1.5)
        #self.setStyleSheet("border:1px solid red;")
        self.show()

    def setColor(self, color):
        pa = QPalette()
        pa.setColor(QPalette.Foreground, color)
        self.setPalette(pa)
    
    def setShadow(self, color, blurRadius, offset):
        self.eff = QGraphicsDropShadowEffect()
        self.eff.setColor(color)
        self.eff.setBlurRadius(blurRadius)
        self.eff.setOffset(offset, offset)
        self.setGraphicsEffect(self.eff)

    def showFlyDM(self, top=None):
        if top:
            self.top = top
        self.setFlyAnim(self.top, DISPLAY_TIME)
        self.show()
        self.anim.start()

    def setFlyAnim(self, top, displayTime):
        self.anim = QPropertyAnimation(self, b'geometry')
        self.anim.setDuration(displayTime)
        self.anim.setStartValue(QRect(screenWidth - 1, top, self.width(), self.height()))
        self.anim.setEndValue(QRect(- self.width(), top, self.width(), self.height()))
    
    def showFixedDM(self):
        self.setFixedAnim(self.top, DISPLAY_TIME)
        self.show()
        self.anim.start()

    def setFixedAnim(self, top, displayTime):
        self.anim = QPropertyAnimation(self, b'geometry')
        self.anim.setDuration(displayTime)
        self.anim.setDuration(DISPLAY_TIME)
        self.anim.setStartValue(QRect(int((screenWidth - self.width()) / 2), top, self.width(), self.height()))
        self.anim.setEndValue(QRect(int((screenWidth - self.width()) / 2), top, self.width(), self.height()))

    def speed(self):
        return (self.width() + screenWidth) / DISPLAY_TIME

class footerDanmu(Danmu):
    CHANGE_TIMES = 20
    RAINBOW_QRGB_LIST = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 127, 255), (0, 0, 255), (139, 0, 255)]
    def __init__(self, text):  # 先继承，在重构
        super(footerDanmu,self).__init__(text, QColor(255, 0, 0), 0)
        self.changeIdx = 0
        self.clrIdx = 0
        self.changeRGB = [0,0,0]
        self.setGeometry(QRect(screenWidth - self.width(), screenHeight - self.height() - 50, self.width(), self.height()))
    def changeColor(self):
        if self.changeIdx < self.CHANGE_TIMES:
            pa = QPalette()
            pa.setColor(QPalette.Foreground, QColor(
                self.RAINBOW_QRGB_LIST[self.clrIdx][0] + self.changeRGB[0] / self.CHANGE_TIMES * self.changeIdx,
                self.RAINBOW_QRGB_LIST[self.clrIdx][1] + self.changeRGB[1] / self.CHANGE_TIMES * self.changeIdx,
                self.RAINBOW_QRGB_LIST[self.clrIdx][2] + self.changeRGB[2] / self.CHANGE_TIMES * self.changeIdx
            ))
            self.setPalette(pa)
            self.changeIdx += 1
            self.show()
        else:
            self.changeIdx = 0
            self.clrIdx = 0 if self.clrIdx == 6 else self.clrIdx + 1
            self.getChangeRGB(self.RAINBOW_QRGB_LIST[self.clrIdx], self.RAINBOW_QRGB_LIST[(self.clrIdx + 1) % 7])
    
    def getChangeRGB(self, clr1, clr2):
        self.changeRGB = [clr2[0] - clr1[0], clr2[1] - clr1[1], clr2[2] - clr1[2]]

class DanmuManager:
    def __init__(self, display_area=0.9):
        self.flyDandaos = []
        self.topDandaos = []
        self.btmDandaos = []
        for _ in range(int(screenHeight * display_area / (FONT_SIZE + 20))):
            self.flyDandaos.append([])
            self.topDandaos.append([])
            self.btmDandaos.append([])

    def destroyDM(self):
        timeNow = time.time()
        invlTime = DISPLAY_TIME / 1000 + 0.5
        for dandao in self.flyDandaos:
            if len(dandao) == 0:
                continue
            if timeNow - dandao[0][1] > invlTime:
                dandao[0][0].deleteLater()
                dandao.pop(0)
            else:
                continue
        for dandao in self.topDandaos:
            if len(dandao) == 0:
                continue
            if timeNow - dandao[0][1] > invlTime:
                dandao[0][0].deleteLater()
                dandao.pop(0)
            else:
                continue
        for dandao in self.btmDandaos:
            if len(dandao) == 0:
                continue
            if timeNow - dandao[0][1] > invlTime:
                dandao[0][0].deleteLater()
                dandao.pop(0)
            else:
                continue

    def add(self, text):
        text, color, style = self.parse(text)
        flag = True if text else False
        if style == 'fly':
            danmu = Danmu(text, color, 0)
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
                    sleep(0.1)
        elif style == 'top':
            while flag:
                my_dandaos = self.topDandaos
                for idx, dandao in enumerate(my_dandaos):
                    if flag and (not dandao or time.time() - dandao[-1][1] > DISPLAY_TIME / 1000 + 1):
                        dandao.append(
                            (Danmu(text, color, (FONT_SIZE + 20) * idx), time.time())
                        )
                        dandao[-1][0].showFixedDM()
                        flag = False
                        break
                if flag:
                    sleep(0.1)
        elif style == 'btm':
            while flag:
                my_dandaos = self.btmDandaos
                for idx, dandao in enumerate(my_dandaos):
                    if flag and (not dandao or time.time() - dandao[-1][1] > DISPLAY_TIME / 1000 + 1):
                        dandao.append(
                            (Danmu(text, color, screenHeight - 30 - (FONT_SIZE + 20) * (1 + idx)), time.time())
                        )
                        dandao[-1][0].showFixedDM()
                        flag = False
                        break
                if flag:
                    sleep(0.1)

    def parse(self, text):
        textColor = QColor(240, 240, 240)
        style = 'fly'
        match_object = re.search(r'\#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})', text)
        if match_object:
            textColor = QColor(int(match_object.group(1), 16), int(match_object.group(2), 16), int(match_object.group(3), 16))
            text = re.sub(r'\#[0-9a-fA-F]{6}', '', text)
        if re.search(r'\#top', text, re.I):
            style = 'top'
            text = re.sub(r'\#top', '', text, re.I)
        elif re.search(r'\#btm', text, re.I):
            style = 'btm'
            text = re.sub(r'\#btm', '', text, re.I)
        return text, textColor, style

def sleep(s):
    loop = QEventLoop()
    QTimer.singleShot(int(s * 1000), loop.quit)
    loop.exec()

def DMMTask(danmu_manager):
    while True:
        danmu_manager.destroyDM()
        time.sleep(0.1)

def FDMTask(footerDM):
    while True:
        footerDM.changeColor()
        time.sleep(0.1)

if __name__ == '__main__':
    print("Start")
    urlopen('http://127.0.0.1:5000/cls')
    app = QApplication(sys.argv)
    screenRect = QDesktopWidget.screenGeometry(QApplication.desktop())
    screenWidth = screenRect.width()
    screenHeight = screenRect.height()
    ex = App()
    danmu_manager = DanmuManager()
    danmu_manager.add("Hello World!")
    footer_danmu = footerDanmu("zyatql")
    DMMThread = td.Thread(target=DMMTask, args=(danmu_manager,), daemon=True)
    DMMThread.start()
    FDMThread = td.Thread(target=FDMTask, args=(footer_danmu,), daemon=True)
    FDMThread.start()
    while True:
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
            sleep(0.1)
    