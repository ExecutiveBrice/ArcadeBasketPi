from flask import Flask, jsonify, render_template
from core import state


app = Flask(__name__)


@app.route("/")
def index():
    return render_template(
        "index.html",
        score=state.score(),
        minutes=state.elapsed() // 60,
        seconds=str(state.elapsed() % 60).zfill(2),
        best_score=225,
    )


@app.route("/api/state")
def api_state():
    return jsonify({
        "score": state.score(),
        "time": state.elapsed(),
        "running": state.is_running(),
    })
