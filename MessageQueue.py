from flask import Flask,request
from queue import Queue
app = Flask(__name__)

q = Queue()

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/push")
def push():
    message = request.args.get('message')
    q.put(message)
    return 'OK'

@app.route("/get")
def get():
    if q.empty():
        return 'Error:Empty'
    else:
        return q.get()

@app.route("/cls")
def cls():
    with q.mutex:
        q.queue.clear()
    return 'OK'

if __name__ == "__main__":
    print('Start')
    app.run(host = '127.0.0.1', port = '5000')
