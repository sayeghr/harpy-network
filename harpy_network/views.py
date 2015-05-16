from flask import render_template

from harpy_network import app

@app.route("/")
def landing_page():
    return render_template("landing_page.html")