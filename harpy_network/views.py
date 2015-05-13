from harpy_network import app

@app.route("/")
def hello_world():
    return "Hello World"