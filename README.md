# CLAIRify Web Interface
This directory contains the source code for CLAIRify Web interface

## Dependencies
- [OpenAI Python Library](https://pypi.org/project/openai/) 0.27.8
- [Flask](https://flask.palletsprojects.com/) 2.2.2
- [Flask SocketIO](https://flask-socketio.readthedocs.io/) 5.3.4

You can install dependencies by

```bash
pip install -r requirements.txt
```

## Getting Started
1. Set `OPENAI_API_KEY` environment variable. (cf. [Best Practices for API Key Safety](https://help.openai.com/en/articles/5112595-best-practices-for-api-key-safety))
2. Start the server
```bash
python main.py
```
3. Open `http://127.0.0.1:3000/` in your favorite browser.

## Usage
![](/images/screenshot.png)

1. Type your experiment in the left column.
2. Click "Translate" button.
3. You will see an execution log while translation
4. Final output XDL will be automatically shown after translation is done.
