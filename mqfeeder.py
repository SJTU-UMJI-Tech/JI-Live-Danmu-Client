# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.parse import urlencode

HELP_CONTENT = 'To send normal white Danmu by just send your words.\n' + \
               'Add "#FF0000" or other RGBs to send Danmu in red or other colors.\n' + \
               'Add "#top" or "#btm" to send Danmu at the top or bottom.\n' + \
               'The max length of your words is 30.\n' + \
               'e.g "#top #00FF00 Life is short,use Python."'


def onQQMessage(bot, contact, member, content):
    if '#help' in content:
        bot.SendTo(contact, HELP_CONTENT)
    elif not bot.isMe(contact, member):
        try:
            urlopen('http://127.0.0.1:5000/push?'+urlencode({'message': content}), timeout=1)
        except KeyError as e:
            print(e)
