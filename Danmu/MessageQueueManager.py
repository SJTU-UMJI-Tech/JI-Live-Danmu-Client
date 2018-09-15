from urllib.request import urlopen
import os


class MessageQueueManager:
    def __init__(self, url='http://127.0.0.1:5000/'):
        self.url = url
        urlopen(self.url)
        self.clear()

    def get(self):
        message = urlopen(os.path.join(self.url, 'get')).read().decode('utf-8')
        return message

    def clear(self):
        return urlopen(os.path.join(self.url, 'cls'))

    def push_all_message_to_danmu_manager(self, danmu_manager):
        message = self.get()
        while message != 'Error:Empty':
            danmu_manager.add(message)
            message = self.get()
