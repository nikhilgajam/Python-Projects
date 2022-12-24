from flask import Flask

app = Flask(__name__)


@app.route("/")
def homePage():
    return "<h1>Welcome To The Home Page</h1><p>Try to type something in the url like .../hello etc</p>"


@app.route("/<name>")  # This tag works as a parameter passing to the takeAnything method and parameter name and <name> should be same
def takeAnything(name):
    return "You entered: " + name


if __name__ == '__main__':
    app.run()
