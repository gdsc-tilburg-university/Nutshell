import threading
from queue import Queue
from flask import Flask, render_template, jsonify
from flaskwebgui import FlaskUI
from speech_to_text.service import transcribedTextStore
from summarization.service import get_summarized_text
from recording.service import isRecording
from threading import Thread

app = Flask(__name__)

ui = FlaskUI(app, width=500, height=800)


@app.route('/')
def index():
    return render_template("layout.html")


@app.route('/summarized_text')
def summarized_text():
    return jsonify(get_summarized_text())


@app.route('/transcribed_text')
def transcribed_text():
    return jsonify(transcribedTextStore)


@app.route('/pause_recording', methods=['POST'])
def pause_recording():
    global isRecording
    isRecording.clear()
    return jsonify(True)


@app.route('/start_recording', methods=['POST'])
def start_recording():
    global isRecording
    isRecording.set()
    return jsonify(True)


def renderGUI():
    thread = Thread(target=app.run, daemon=True)
    thread.start()


if __name__ == "__main__":
    renderGUI()
