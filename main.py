from flask import Flask, render_template, request
import nlp2xdl as generate_xdl
import random
from flask_socketio import SocketIO, send
import time
from threading import Thread, Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = "".join([chr(random.randint(97, 122)) for _ in range(10)])
app.config["SESSION_COOKIE_SECURE"] = True
socketio = SocketIO(app)

thread = None
thread_lock = Lock()
input_xdl = ""


def translate(input_xdl):
    global output_xdl
    with open("input_dir/Input.txt", "w") as f:
        f.write(input_xdl)
    generate_xdl.main("input_dir", socketio)
    with open("input_dir_output/Input.txt", "r") as f:
        output_xdl = f.read()


def run_translation(input_xdl):
    global thread
    print("translation is running")
    with thread_lock:
        thread = Thread(target=translate, args=(input_xdl,))
        thread.start()


@app.route('/', methods=['GET', 'POST'])
def index():
    global input_xdl

    if request.method == 'POST':
        input_xdl = request.form['input_field']
        run_translation(input_xdl)

    return render_template("index.html", input_xdl=input_xdl)

@app.route('/device')
def device():
    return render_template("device.html")


if __name__ == '__main__':
    socketio.run(app, debug=True)
