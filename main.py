import json
import os
from threading import Lock, Thread

import openai
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit

from verify import verify_xdl


def prompt(instructions, description, max_tokens):
    """Function that calls the OpenAI API"""
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=description + "\nConvert to XDL:\n" + instructions,
        temperature=0,
        max_tokens=max_tokens,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["text"]


def translate(input_xdl):
    """Function that translates the input XDL"""

     # Get API key
    
    openai.api_key = os.environ["OPENAI_API_KEY"]

    # Get XDL description
    with open("XDL_description.txt", "r") as f:
        XDL_description = f.read()

    correct_syntax = False
    errors = {}
    prev_input_xdl = input_xdl

    # Start 10 iteration for loop to limit token usage
    for step in range(10):
        socketio.emit("message", f"Convert to XDL: {input_xdl}")
        try:
            gpt3_output = prompt(input_xdl, XDL_description, 1000)
        except:
            socketio.emit(
                "message", "Error. Too many tokens required or invalid API key.")
            break

        socketio.emit("message", "gpt3_output:::")
        socketio.emit("message_xdl", f"{gpt3_output}")

        if "<XDL>" in gpt3_output:
            gpt3_output = gpt3_output[gpt3_output.index("<XDL>"):]
            compile_correct = verify_xdl(gpt3_output)
            errors[step] = {
                "errors": compile_correct,
                "input_xdl": input_xdl,
                "gpt3_output": gpt3_output,
            }
            if not compile_correct:
                correct_syntax = True
                break
            else:
                error_list = set()
                for item in compile_correct:
                    for error in item["errors"]:
                        error_list.add(error)
                error_message = f"\n{gpt3_output}\nThis XDL was not correct. These were the errors\n{os.linesep.join(list(error_list))}\nPlease fix the errors."
                input_xdl = f"{prev_input_xdl} {error_message}"

        else:
            error_message = f"\n{gpt3_output}\nThis XDL was not correct. XDL should start with <XDL>. Please fix the errors."
            input_xdl = f"{prev_input_xdl} {error_message}"

    try:
        if correct_syntax:
            xdl = gpt3_output
        else:
            xdl = "The correct XDL could not be generated."

    except Exception as e:
        socketio.emit("message", f"Error: {e}")

    socketio.emit("message", f"XDL: {xdl}")
    socketio.emit("correct_xdl", f"{xdl}")
    socketio.emit("message", f"Final syntax valid: {correct_syntax}")


# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config["SESSION_COOKIE_SECURE"] = True
socketio = SocketIO(app)

# Global variables
thread = None
thread_lock = Lock()
input_xdl = ""


def run_translation(input_xdl):
    """Function that runs the translation in a separate thread."""
    global thread
    with thread_lock:
        thread = Thread(target=translate, args=(input_xdl,))
        thread.start()


@app.route("/", methods=["GET", "POST"])
def index():
    """Function that renders the index page."""
    global input_xdl
    if request.method == "POST":
        input_xdl = request.form["input_field"]
        run_translation(input_xdl)

    return render_template("index.html", input_xdl=input_xdl)


socketio.run(app, port=3000)
