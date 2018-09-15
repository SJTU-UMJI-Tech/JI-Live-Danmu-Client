# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode
from Danmu.config import HELP_CONTENT

# qqbot onMessage event
def onQQMessage(bot, contact, member, content):
    # reply help content
    if '#help' in content:
        bot.SendTo(contact, HELP_CONTENT)
    # send message to queue
    elif not bot.isMe(contact, member):
        try:
            urlopen('http://127.0.0.1:5000/push?' + urlencode({'message': content}), timeout = 1)
        except KeyError as e:
            print(e)
