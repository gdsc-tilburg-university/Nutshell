from flask import Flask, Response, render_template, jsonify
from flaskwebgui import FlaskUI
from summarization.service import summarizedTextStore
from time import sleep
from threading import Thread

app = Flask(__name__)

ui = FlaskUI(app, width=500, height=800)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/summarized_text')
def summarized_text():
    return jsonify(summarizedTextStore)


def renderGUI():
    thread = Thread(target=app.run, daemon=True)
    thread.start()


if __name__ == "__main__":
    renderGUI()
