from flask import Flask

app = Flask(__name__)


@app.route("/")  # The route of the page is defined using the decorators
def homePage():
    return "<h1>Hello World</h1>"  # Returning the html page


if __name__ == '__main__':
    app.run(debug=True)   # Running the web program and debug=True is going to update the content without re-running the server many times
# Just run this particular python program to see the url to open this page in a browser