from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def homePage():
    return render_template("index.html")  # This page should be inside the templates directory which in the program directory



if __name__ == '__main__':
    app.run()
