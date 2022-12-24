from flask import Flask, render_template
import random

app = Flask(__name__)


@app.route("/")
def homePage():
    return render_template("index.html")  # This page should be inside the templates directory which in the program directory


@app.route("/<name>")
def namePage(name):
    return render_template("name.html", content=name, rand=random.randint(1, 101))  # We need to use content variable using {{content}} in web page 


if __name__ == '__main__':
    app.run()
