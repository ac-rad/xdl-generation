from flask import Flask, render_template, request
import nlp2xdl as generate_xdl
import threading

app = Flask(__name__)
app.secret_key = 'my_secret_key' 

def translate(input_xdl):
    with open("input_dir/Input.txt", "w") as f:
        f.write(input_xdl)
    generate_xdl.main("input_dir")
    with open("input_dir_output/Input.txt", "r") as f:
        return f.read()


@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST' and (request.form["submit_button"] == "Loading..." or request.form["submit_button"] == "Translate"):
        input_xdl = request.form['input_field']
        output_xdl = translate(input_xdl)
        return render_template("index.html", input_xdl=input_xdl, output_xdl=output_xdl)

    return render_template("index.html", input_xdl=None, output_xdl=None)

if __name__ == '__main__':
    app.run(debug=True)