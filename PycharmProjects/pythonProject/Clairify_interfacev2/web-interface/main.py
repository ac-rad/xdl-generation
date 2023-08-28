import os
from threading import Lock, Thread

import openai
from flask import Flask, render_template, request
from flask_socketio import SocketIO, join_room, leave_room

from verify import verify_xdl


def emit(event, data, sid):
    """Function that emits data to the client."""
    socketio.emit(event, data, to=sid)

def prompt(instructions, description, max_tokens, model="text-davinci-003"):
    """Function that calls the OpenAI API"""
    if model == "text-davinci-003":
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
    
    elif model == "gpt-3.5-turbo" or model == "gpt-4":
        response = openai.ChatCompletion.create(
            model=model,
            messages = [
                {"role":"system", "content":"You are a natural language to XDL translator, you must also do your best to correct any incorrect XDL, only use items contained in the description, here is a description of XDL:\n"+description },
                {"role":"user", "content": f"\nConvert/Correct the following to proper XDL:\n{instructions}"}
            ],
            temperature=0,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        return response["choices"][0]["message"]["content"]



def translate(input_xdl, model, sid):
    """Function that translates the input XDL"""

    openai.api_key = os.environ["OPENAI_API_KEY"]
    openai.organization = os.environ["OPENAI_ORGANIZATION_ID"]
    
    # Get XDL description
    with open(os.path.join(os.path.dirname(__file__), "XDL_description.txt"), "r") as f:
        XDL_description = f.read()

    correct_syntax = False
    errors = {}
    prev_input_xdl = input_xdl

    # Start 10 iteration for loop to limit token usage
    for step in range(10):
        emit("message", f"Convert to XDL: {input_xdl}", sid)
        try:
            gpt3_output = prompt(input_xdl, XDL_description, 1000, model)
        except:
            emit("message", "Error. Too many tokens required or invalid API key.", sid)
            break

        if "<XDL>" in gpt3_output:
            gpt3_output = gpt3_output[gpt3_output.index("<XDL>"):gpt3_output.rindex("</XDL>") + 6]
            print(gpt3_output)
            emit("message", "gpt3_output:::", sid)
            emit("message_xdl", f"{gpt3_output}", sid)
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
            error_message = f"\n{gpt3_output}\nThis XDL was not correct. XDL should start with <XDL> and end with </XDL>. Please fix the errors."
            input_xdl = f"{prev_input_xdl} {error_message}"

    try:
        if correct_syntax:
            xdl = gpt3_output
        else:
            xdl = "The correct XDL could not be generated."

    except Exception as e:
        emit("message", f"Error: {e}", sid)

    emit("correct_xdl", f"{xdl}", sid)
    emit("message", f"Final syntax valid: {correct_syntax}", sid)


# Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
app.config["SESSION_COOKIE_SECURE"] = True
socketio = SocketIO(app)

# Global variables
thread = None
thread_lock = Lock()
clients = set()


def run_translation(input_xdl, model, sid):
    """Function that runs the translation in a separate thread."""
    global thread
    with thread_lock:
        thread = Thread(target=translate, args=(input_xdl, model, sid))
        thread.start()


@socketio.on("connect")
def on_connect():
    """Function that runs when a client connects."""
    emit("message", "Connected", request.sid)
    if request.sid not in clients:
        clients.add(request.sid)
        print(clients)
        join_room(request.sid)

@socketio.on("disconnect")
def on_disconnect():
    emit("message", "Disconnected", request.sid)
    if request.sid in clients:
        clients.remove(request.sid)
        leave_room(request.sid)


@app.route("/", methods=["GET", "POST"])
def index():
    input_xdl = ""
    
    """Function that renders the index page."""
    if request.method == "POST":
        input_xdl = request.form["input_field"]
        model = request.form["gptVersion"]
        sid = request.form["sid"]
        emit("message", f"Model: {model}", sid)
        run_translation(input_xdl, model, sid)

    return render_template("index.html", input_xdl=input_xdl)


socketio.run(app, port=3000)
