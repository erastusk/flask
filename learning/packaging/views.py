from  packaging import app

@app.route("/")
def hello():
    return "<h1>Hello World</h1>"
@app.route("/contacts")
def contacts():
    return "<h1>Contacts</h1>"    

