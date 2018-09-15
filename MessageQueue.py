from flask import Flask, request
from queue import Queue

SECRET_KEY = 'YourSecretKey'

app = Flask(__name__)

q = Queue()

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)
userIP = '127.0.0.1'

# identify user's identity
@app.route("/")
def hello():
    global userIP
    if request.args.get('secretKey') == SECRET_KEY:
        userIP = request.remote_addr
    return "Hello World!"

# add message to queue
@app.route("/push")
def push():
    if request.remote_addr != '127.0.0.1':
        return 'Error:403 Forbidden'
    message = request.args.get('message')
    q.put(message)
    return 'OK'

# get message to queue
@app.route("/get")
def get():
    if request.remote_addr not in [userIP, '127.0.0.1']:
        return 'Error:403 Forbidden'
    if q.empty():
        return 'Error:Empty'
    else:
        return q.get()

# remove all messages in queue
@app.route("/cls")
def cls():
    if request.remote_addr not in [userIP, '127.0.0.1']:
        return 'Error:403 Forbidden'
    with q.mutex:
        q.queue.clear()
    return 'OK'

# get queue length
@app.route("/qsize")
def qsize():
    if request.remote_addr not in [userIP, '127.0.0.1']:
        return 'Error:403 Forbidden'
    return str(q.qsize())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')
