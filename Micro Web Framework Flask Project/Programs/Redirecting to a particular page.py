from flask import Flask, redirect, url_for

app = Flask(__name__)


@app.route("/")
def homePage():
    return "<h1>Welcome To The Home Page</h1><p>Try to go to .../admin then you will be redirected to home</p>"


@app.route("/admin")
def adminPage():
    print("Redirecting to the home page")
    return redirect(url_for("homePage"))  # Need to enter the method name to return to that in url_for method


if __name__ == '__main__':
    app.run()
