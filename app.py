from flask_socketio import SocketIO, emit
from flask import Flask, render_template, request, json, Response, jsonify,escape
from libs import *
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template("index.html")


@socketio.on('demo', namespace='/tapi')
def demo(message):
    """
    构建训练数据
    """
    print('message',message)
    keyword = message.get('data')
    while  True:
        emit('demo response', {'data': time.time()})
        time.sleep(1)


if __name__ == "__main__":
    # app.run()
    # socketio.run(app)
    socketio.run(app, host="0.0.0.0", port=5000)