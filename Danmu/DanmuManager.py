import time, re, sip
from PyQt5.QtGui import QColor
from Danmu.Danmu import Danmu
from Danmu.config import *

class DanmuManager:
    def __init__(self, window, screenWidth, screenHeight, display_area=0.9):
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.window = window
        self.flyDandaos = []
        self.topDandaos = []
        self.btmDandaos = []
        for _ in range(int(screenHeight * display_area / (FONT_SIZE + 20))):
            self.flyDandaos.append([])
            self.topDandaos.append([])
            self.btmDandaos.append([])
        self.flyQ = []
        self.topQ = []
        self.btmQ = []

    def destroyDM(self):
        timeNow = time.time()
        invlTime = DISPLAY_TIME / 1000 + 0.5
        for dandao in self.flyDandaos:
            if len(dandao) == 0:
                continue
            if timeNow - dandao[0][1] > invlTime:
                sip.delete(dandao[0][0])
                dandao.pop(0)
            else:
                continue
        for dandao in self.topDandaos:
            if len(dandao) == 0:
                continue
            if timeNow - dandao[0][1] > invlTime:
                sip.delete(dandao[0][0])
                dandao.pop(0)
            else:
                continue
        for dandao in self.btmDandaos:
            if len(dandao) == 0:
                continue
            if timeNow - dandao[0][1] > invlTime:
                sip.delete(dandao[0][0])
                dandao.pop(0)
            else:
                continue

    def show(self):
        added_successfully = True
        while self.flyQ and added_successfully:
            added_successfully = False
            text, color = self.flyQ[0]
            danmu = Danmu(text, color, 0, self.window)
            v2 = danmu.speed()
            for idx, dandao in enumerate(self.flyDandaos):
                if not dandao:
                    dandao.append((danmu, time.time()))
                    dandao[-1][0].showFlyDM((FONT_SIZE + 20) * idx)
                    added_successfully = True
                    break
                else:
                    v1 = dandao[-1][0].speed()
                    min_interval_time = (
                                                self.screenWidth + dandao[-1][0].width() - self.screenWidth * v1 / v2) / v1
                    min_interval_time = max(
                        min_interval_time, dandao[-1][0].width() / v1)
                    if time.time() - dandao[-1][1] > min_interval_time / 1000:
                        dandao.append((danmu, time.time()))
                        dandao[-1][0].showFlyDM((FONT_SIZE + 20) * idx)
                        added_successfully = True
                        break
            if added_successfully:
                self.flyQ.pop(0)
            else:
                sip.delete(danmu)

        added_successfully = True
        while self.topQ and added_successfully:
            added_successfully = False
            text, color = self.topQ[0]
            for idx, dandao in enumerate(self.topDandaos):
                if not dandao or time.time() - dandao[-1][1] > DISPLAY_TIME / 1000 + 1:
                    dandao.append((Danmu(text, color, (FONT_SIZE + 20) * idx, self.window), time.time()))
                    dandao[-1][0].showFixedDM()
                    added_successfully = True
                    break
            if added_successfully:
                self.topQ.pop(0)

        added_successfully = True
        while self.btmQ and added_successfully:
            added_successfully = False
            text, color = self.btmQ[0]
            for idx, dandao in enumerate(self.btmDandaos):
                if not dandao or time.time() - dandao[-1][1] > DISPLAY_TIME / 1000 + 1:
                    dandao.append((Danmu(text, color, self.screenHeight - 30 - (FONT_SIZE + 20) * (1 + idx), self.window), time.time()))
                    dandao[-1][0].showFixedDM()
                    added_successfully = True
                    break
            if added_successfully:
                self.btmQ.pop(0)


    def add(self, text):
        repeat = re.search(r'\#time(\d+)', text)
        if repeat:
            repeat_count = max(min(50, int(repeat.group(1))), 1)
            message = re.sub('\#time\d+', '', text)
            if not re.search(r'\#[0-9a-fA-F]{6}', message):
                rainbow_rgb_index = 0
                for _ in range(repeat_count):
                    self.add(RAINBOW_RGB_LIST[rainbow_rgb_index] + message)
                    rainbow_rgb_index = 0 if rainbow_rgb_index == 6 else rainbow_rgb_index + 1
            else:
                for _ in range(repeat_count):
                    self.add(message)
        else:
            text, color, style = self.parse(text)
            if text.strip() == '':
                return
            if style == 'fly':
                self.flyQ.append((text, color))
            elif style == 'top':
                self.topQ.append((text, color))
            elif style == 'btm':
                self.btmQ.append((text, color))

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
