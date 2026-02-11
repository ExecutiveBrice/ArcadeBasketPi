"""LED feedback control module."""

from __future__ import annotations

import logging
import threading
import time

import config

LOGGER = logging.getLogger(__name__)


class LedController:
    """Control score pulse LED and match-active LED."""

    def __init__(self, gpio) -> None:
        """Initialize LED controller with GPIO backend."""
        self.gpio = gpio
        self._lock = threading.Lock()

    def setup(self) -> None:
        """Configure LED pins as outputs and set default state."""
        self.gpio.setup(config.LED_SCORE_PIN, self.gpio.OUT, initial=self.gpio.LOW)
        self.gpio.setup(config.LED_MATCH_ACTIVE_PIN, self.gpio.OUT, initial=self.gpio.LOW)
        LOGGER.info(
            "LEDs ready (score=%s, active=%s)",
            config.LED_SCORE_PIN,
            config.LED_MATCH_ACTIVE_PIN,
        )

    def pulse_score_led(self) -> None:
        """Flash the score LED briefly in a background thread."""
        threading.Thread(target=self._pulse_worker, daemon=True).start()

    def _pulse_worker(self) -> None:
        """Drive score LED pulse while avoiding concurrent write races."""
        with self._lock:
            self.gpio.output(config.LED_SCORE_PIN, self.gpio.HIGH)
            time.sleep(config.SCORE_LED_PULSE_SECONDS)
            self.gpio.output(config.LED_SCORE_PIN, self.gpio.LOW)

    def set_match_active(self, active: bool) -> None:
        """Set the match-active LED state.

        Args:
            active: True to turn on the LED, False to turn it off.
        """
        value = self.gpio.HIGH if active else self.gpio.LOW
        self.gpio.output(config.LED_MATCH_ACTIVE_PIN, value)

    def cleanup(self) -> None:
        """Turn off LEDs during shutdown."""
        self.gpio.output(config.LED_SCORE_PIN, self.gpio.LOW)
        self.gpio.output(config.LED_MATCH_ACTIVE_PIN, self.gpio.LOW)
