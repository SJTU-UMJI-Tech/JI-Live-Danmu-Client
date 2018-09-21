from urllib.request import urlopen
from urllib.parse import urlencode, urljoin
import time
import socket
from queue import Queue
import threading as td


class MessageQueueManager:
    def __init__(self, url, port):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((url, port))
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        self.localmq = Queue()
        # try to create a thread to push message to queue
        for _ in range(60):
            try:
                self.clear()
                td.Thread(
                    target=self.getSocketMessage,
                    args=(self.localmq, url, port),
                    daemon=True).start()
                return
            except KeyError as e:
                print(e)
                time.sleep(1)

    def getSocketMessage(self, q, url, port):
        while True:
            try:
                buffer = []
                while True:
                    # receive 1024 byte in maximum
                    d = self.s.recv(1024)
                    if d:
                        buffer.append(d)
                    if len(d) < 1024:
                        break
                messages = b''.join(buffer).decode('utf-8')
                for msg in messages.split('\r\n'):
                    q.put(msg)
            except:
                messages = 'Error:Empty'
                pass
            print(messages)
            time.sleep(0.1)

    def add2DanmuManager(self, danmuManager):
        while not self.localmq.empty():
            danmuManager.addDanmu(self.localmq.get())

    # remove all messages in queue
    def clear(self):
        pass
