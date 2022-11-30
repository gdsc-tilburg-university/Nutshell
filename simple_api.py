from flask import Flask

app = Flask(__name__)


@app.route("/", defaults={'greeting': None})
@app.route("/<greeting>")
def hello_world(greeting):
    if greeting:
        return "hello world!"
    return "🥲"


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
