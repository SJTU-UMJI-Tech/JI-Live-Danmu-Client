from urllib.request import urlopen
from urllib.parse import urlencode
import os, time
from Danmu.config import SECRET_KEY
from queue import Queue
import threading as td


class MessageQueueManager:
    def __init__(self, url='http://127.0.0.1:5000/'):
        self.url = url
        self.localmq = Queue()
        # try to create a thread to push message to queue
        for _ in range(60):
            try:
                urlopen(self.url + '?' + urlencode({'secretKey': SECRET_KEY}))
                self.clear()
                t = td.Thread(target=self.getMessage, args=(self.localmq, self.url), daemon=True)
                t.start()
                return
            except KeyError as e:
                print(e)
                time.sleep(1)


    @staticmethod
    def getMessage(q, url):
        while True:
            try:
                message = urlopen(os.path.join(url, 'get')).read().decode('utf-8')
                if message == 'Error:403 Forbidden':
                    urlopen(url + '?' + urlencode({'secretKey': SECRET_KEY}))
                    message = urlopen(os.path.join(url, 'get')).read().decode('utf-8')
            except:
                message = 'Error:Empty'
            if message not in ['Error:Empty', 'Error:403 Forbidden']:
                q.put(message)
            else:
                time.sleep(0.1)        

    def add2DanmuManager(self, danmuManager):
        while not self.localmq.empty():
            danmuManager.addDanmu(self.localmq.get())

    # remove all messages in queue
    def clear(self):
        return urlopen(os.path.join(self.url, 'cls'))
