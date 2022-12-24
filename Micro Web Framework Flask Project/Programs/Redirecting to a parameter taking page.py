from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route("/")
def homePage():
    return "<h1>Welcome To The Home Page</h1><p>Try to type something in the url like .../hello etc</p>"


@app.route("/<name>")
def takeAnything(name):
    return "You entered: " + name


@app.route("/admin")
def adminPage():
    return redirect(url_for("takeAnything", name="Admin!"))  # Providing the parameter in url_for method


if __name__ == '__main__':
    app.run()
