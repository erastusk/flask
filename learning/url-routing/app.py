from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello World</h1>"

@app.route("/contact-us/")
def contact_us():
    return "<h1>Contact Us</h1>"