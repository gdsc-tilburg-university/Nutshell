from flask import Flask, render_template
from flaskwebgui import FlaskUI

app = Flask(__name__)

ui = FlaskUI(app, width=500, height=800)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == "__main__":
    ui.run()