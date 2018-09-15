from urllib.request import urlopen
import os, time


class MessageQueueManager:
    def __init__(self, url='http://127.0.0.1:5000/'):
        self.url = url
        for _ in range(60):
            try:
                urlopen(self.url)
                self.clear()
                return
            except KeyError as e:
                print(e)
                time.sleep(1)

    def get(self):
        try:
            message = urlopen(os.path.join(self.url, 'get')).read().decode('utf-8')
            if message == 'Error:403 Forbidden':
                urlopen(self.url)
                message = urlopen(os.path.join(self.url, 'get')).read().decode('utf-8')
        except:
            message = 'Error:Empty'
        return message

    def clear(self):
        return urlopen(os.path.join(self.url, 'cls'))

    def push_all_message_to_danmu_manager(self, danmu_manager):
        message = self.get()
        while message != 'Error:Empty':
            danmu_manager.add(message)
            message = self.get()
