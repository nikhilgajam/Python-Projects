from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def homePage():
    return render_template("index.html", content=["hello", "world", "ok"])


if __name__ == '__main__':
    app.run()
