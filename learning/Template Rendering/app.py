from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello World</h1>"

@app.route("/contacts/<username>")
def contacts(username):
    return render_template('profiles.html', username=username)