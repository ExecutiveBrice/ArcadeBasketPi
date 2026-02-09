from flask import Flask, jsonify, render_template
from core import state


app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/state")
def api_state():
    return jsonify({
    "score": state.state["score"],
    "time": state.elapsed(),
    "running": state.state["running"]
    })