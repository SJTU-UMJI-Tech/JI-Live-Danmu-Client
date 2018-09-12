# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode

def onQQMessage(bot, contact, member, content):
    if content == '-hello':
        bot.SendTo(contact, '你好，我是QQ机器人')
    elif content == '-stop':
        bot.SendTo(contact, 'QQ机器人已关闭')
        bot.Stop()
    else:
        urlopen('http://127.0.0.1:5000/push?'+urlencode({'message': content}))
