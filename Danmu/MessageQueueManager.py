from urllib.request import urlopen
from urllib.parse import urlencode, urljoin
import time
from queue import Queue
import threading as td


class MessageQueueManager:
    def __init__(self, url, secretKey):
        self.url = url
        self.secretKey = secretKey
        self.localmq = Queue()
        # try to create a thread to push message to queue
        for _ in range(60):
            try:
                urlopen(self.url + '?' + urlencode({
                    'secretKey': self.secretKey
                }))
                self.clear()
                t = td.Thread(
                    target=self.getMessage,
                    args=(self.localmq, self.url, self.secretKey),
                    daemon=True)
                t.start()
                return
            except KeyError as e:
                print(e)
                time.sleep(1)

    @staticmethod
    def getMessage(q, url, secretKey):
        while True:
            try:
                message = urlopen(urljoin(url, 'get')).read().decode('utf-8')
                if message == 'Error:403 Forbidden':
                    urlopen(url + '?' + urlencode({'secretKey': secretKey}))
                    message = urlopen(urljoin(url,
                                              'get')).read().decode('utf-8')
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
        return urlopen(urljoin(self.url, 'cls'))
