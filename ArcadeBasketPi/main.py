"""ArcadeBasketPi entrypoint: initializes hardware, storage, and Flask app."""

from __future__ import annotations

import atexit
import logging
import signal
import sys
from typing import Dict

from flask import Flask, jsonify, redirect, render_template, url_for

import config
from core.scorer import ScorerService
from core.timer import format_duration
from core.state import MatchState
from hardware.bouton import ResetButton
from hardware.capteur import BasketSensor
from hardware.gpio import cleanup_gpio, configure_gpio
from hardware.leds import LedController
from hardware.son import SoundPlayer
from storage.db import MatchDatabase

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
LOGGER = logging.getLogger(__name__)


class AppContext:
    """Container for long-lived app services."""

    def __init__(self) -> None:
        """Initialize placeholders for services set during bootstrap."""
        self.gpio = None
        self.db = None
        self.state = None
        self.scorer = None
        self.leds = None
        self.sensor = None
        self.button = None


CONTEXT = AppContext()


def build_app() -> Flask:
    """Create and configure Flask application and route handlers."""
    app = Flask(__name__)

    @app.route("/")
    def index():
        """Render the main scoreboard page."""
        status = CONTEXT.scorer.status_payload()
        history = CONTEXT.db.get_history()
        return render_template(
            "index.html",
            score=status["score"],
            elapsed=format_duration(status["elapsed_seconds"]),
            active=status["active"],
            best_score=status["best_score"],
            history=history,
            format_duration=format_duration,
        )

    @app.route("/api/status")
    def api_status():
        """Return live match status as JSON."""
        payload: Dict[str, object] = CONTEXT.scorer.status_payload()
        payload["elapsed"] = format_duration(payload["elapsed_seconds"])
        return jsonify(payload)

    @app.route("/api/history")
    def api_history():
        """Return historical matches as JSON."""
        return jsonify(CONTEXT.db.get_history())

    @app.route("/start", methods=["POST", "GET"])
    def start_match():
        """Start a match from web UI."""
        CONTEXT.scorer.start_match()
        return redirect(url_for("index"))

    @app.route("/reset", methods=["POST", "GET"])
    def reset_match():
        """Reset/start a new match from web UI."""
        CONTEXT.scorer.reset_match()
        return redirect(url_for("index"))

    @app.route("/stop", methods=["POST", "GET"])
    def stop_match():
        """Stop current match and store result."""
        CONTEXT.scorer.stop_match()
        return redirect(url_for("index"))

    return app


def setup_services() -> None:
    """Initialize database, GPIO, hardware modules, and scorer service."""
    CONTEXT.db = MatchDatabase(config.DB_PATH, config.SCHEMA_PATH)
    CONTEXT.db.initialize()

    gpio_namespace = configure_gpio()
    CONTEXT.gpio = gpio_namespace.gpio

    CONTEXT.state = MatchState()
    CONTEXT.leds = LedController(CONTEXT.gpio)
    CONTEXT.leds.setup()

    sound = SoundPlayer(config.SOUND_FILE)
    CONTEXT.scorer = ScorerService(CONTEXT.state, CONTEXT.db, CONTEXT.leds, sound)

    def on_basket() -> None:
        """Callback executed on each valid basket sensor pulse."""
        CONTEXT.scorer.basket_scored()

    def on_button() -> None:
        """Button callback: start when idle, reset when active."""
        status = CONTEXT.scorer.status_payload()
        if status["active"]:
            CONTEXT.scorer.reset_match()
        else:
            CONTEXT.scorer.start_match()

    CONTEXT.sensor = BasketSensor(CONTEXT.gpio, on_basket)
    CONTEXT.sensor.setup()

    CONTEXT.button = ResetButton(CONTEXT.gpio, on_button)
    CONTEXT.button.setup()


def shutdown(*_: object) -> None:
    """Gracefully release hardware resources and store final match."""
    try:
        if CONTEXT.scorer is not None:
            CONTEXT.scorer.stop_match()
    except Exception:
        LOGGER.exception("Failed while saving match during shutdown.")

    try:
        if CONTEXT.sensor is not None:
            CONTEXT.sensor.cleanup()
        if CONTEXT.button is not None:
            CONTEXT.button.cleanup()
        if CONTEXT.leds is not None:
            CONTEXT.leds.cleanup()
        cleanup_gpio()
    except Exception:
        LOGGER.exception("GPIO cleanup failed.")


def main() -> None:
    """Application bootstrap and Flask server startup."""
    setup_services()
    app = build_app()

    atexit.register(shutdown)
    signal.signal(signal.SIGINT, shutdown)
    signal.signal(signal.SIGTERM, shutdown)

    LOGGER.info("Starting Flask server on %s:%s", config.HOST, config.PORT)
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG, use_reloader=False)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        LOGGER.exception("Fatal error. Application will exit.")
        shutdown()
        sys.exit(1)
