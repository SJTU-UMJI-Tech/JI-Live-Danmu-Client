from urllib.request import urlopen
from urllib.parse import urlencode, urljoin
import time
import socket
from queue import Queue
import threading as td
import ssl


class MessageQueueManager:
    def __init__(self, url, port):
        self.localmq = Queue()
        self.url = url
        self.port = port
        # try to create a thread to push message to queue
        self.connect()
        td.Thread(
            target=self.getSocketMessage,
            args=(self.localmq, url, port),
            daemon=True).start()

    def connect(self, retry=60):
        for i in range(retry):
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sslSock = ssl.wrap_socket(
                    self.s, ca_certs="cert.pem", cert_reqs=ssl.CERT_REQUIRED)
                self.sslSock.connect((self.url, self.port))
                print('\nConnected' if i > 0 else 'Connected')
                return
            except ConnectionRefusedError:
                print(
                    '\rConnectionRefused, retrying(%d/%d)' % (i + 1,
                                                              retry + 1),
                    end='')
                time.sleep(5)

    def getSocketMessage(self, q, url, port):
        emptyMessageCountdown = 0
        while True:
            try:
                buffer = []
                while True:
                    # receive 1024 byte in maximum
                    d = self.sslSock.recv(1024)
                    if d:
                        buffer.append(d)
                    if len(d) < 1024:
                        break
                messages = b''.join(buffer).decode('utf-8')
                for msg in messages.split('\0'):
                    q.put(msg)
            except:
                messages = 'Error:Empty'
                pass
            if messages == '':
                emptyMessageCountdown += 1
                print('Empty message %d' % emptyMessageCountdown)
                if emptyMessageCountdown > 20:
                    self.Connect()
                    emptyMessageCountdown = 0
            else:
                emptyMessageCountdown = 0
                print(messages)
            time.sleep(0.1)

    def add2DanmuManager(self, danmuManager):
        while not self.localmq.empty():
            danmuManager.addDanmu(self.localmq.get())
