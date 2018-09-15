from urllib.request import urlopen
from urllib.parse import urlencode
import os, time
from Danmu.config import sk
from queue import Queue
import threading as td


class MessageQueueManager:
    def __init__(self, url='http://127.0.0.1:5000/'):
        self.url = url
        self.localmq = Queue()
        for _ in range(60):
            try:
                self.acquire_ip()
                self.clear()
                t = td.Thread(target=self.push_all_message_to_queue, args=(self.localmq, self.url), daemon=True)
                t.start()
                return
            except KeyError as e:
                print(e)
                time.sleep(1)


    @staticmethod
    def push_all_message_to_queue(q, url):
        while True:
            try:
                message = urlopen(os.path.join(url, 'get')).read().decode('utf-8')
                if message == 'Error:403 Forbidden':
                    urlopen(url + '?' + urlencode({'sk': sk}))  # acquire_ip
                    message = urlopen(os.path.join(url, 'get')).read().decode('utf-8')
            except:
                message = 'Error:Empty'
            if message not in ['Error:Empty', 'Error:403 Forbidden']:
                q.put(message)
            else:
                time.sleep(0.1)


    def acquire_ip(self):
        urlopen(self.url + '?' + urlencode({'sk': sk}))

    def clear(self):
        return urlopen(os.path.join(self.url, 'cls'))

    def push_all_message_to_danmu_manager(self, danmu_manager):
        while not self.localmq.empty():
            danmu_manager.add(self.localmq.get())
