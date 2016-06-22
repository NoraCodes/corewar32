from flask import request, render_template
from corestore import app


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/warriors/add")
def add_warrior():
    return "Not Implemented!", 500


@app.route("/warriors/list")
def list_warriors():
    return "Not Implemented!", 500


@app.route("/warriors/remove")
def remove_warrior():
    return "Not Implemented!", 500
