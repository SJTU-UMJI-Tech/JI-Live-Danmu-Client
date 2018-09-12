from flask import Flask,request
from queue import Queue
app = Flask(__name__)

q = Queue()

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

if __name__ == "__main__":
    app.run(host = '127.0.0.1', port = '5000')
