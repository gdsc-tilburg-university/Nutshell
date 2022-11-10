from flask import Flask, render_template, jsonify
from flaskwebgui import FlaskUI
from speech_to_text.service import transcribedTextStore
from summarization.service import summarizedTextStore
from threading import Thread

app = Flask(__name__)

ui = FlaskUI(app, width=500, height=800)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/summarized_text')
def summarized_text():
    return jsonify(summarizedTextStore)

@app.route('/transcribed_text')
def transcribed_text():
    return jsonify(transcribedTextStore)


def renderGUI():
    thread = Thread(target=ui.run, daemon=True)
    thread.start()


if __name__ == "__main__":
    renderGUI()
