from flask import Flask, request
from queue import Queue
app = Flask(__name__)

q = Queue()

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
user_ip = '127.0.0.1'


@app.route("/")
def hello():
    global user_ip
    if request.args.get('sk') == 'YourSecretKey':
        user_ip = request.remote_addr
    return "Hello World!"


@app.route("/push")
def push():
    if request.remote_addr not in [user_ip, '127.0.0.1']:
        return 'Error:403 Forbidden'
    message = request.args.get('message')
    q.put(message)
    return 'OK'


@app.route("/get")
def get():
    if request.remote_addr not in [user_ip, '127.0.0.1']:
        return 'Error:403 Forbidden'
    if q.empty():
        return 'Error:Empty'
    else:
        return q.get()


@app.route("/cls")
def cls():
    if request.remote_addr not in [user_ip, '127.0.0.1']:
        return 'Error:403 Forbidden'
    with q.mutex:
        q.queue.clear()
    return 'OK'


@app.route("/qsize")
def qsize():
    if request.remote_addr not in [user_ip, '127.0.0.1']:
        return 'Error:403 Forbidden'
    return str(q.qsize())


if __name__ == "__main__":
    print('Start')
    app.run(host='0.0.0.0', port='5000')
