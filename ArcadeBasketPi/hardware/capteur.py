"""Optical basket sensor input module."""

from __future__ import annotations

import logging
from typing import Callable

import config

LOGGER = logging.getLogger(__name__)


class BasketSensor:
    """Manage basket sensor GPIO setup and interrupt callback."""

    def __init__(self, gpio, on_basket: Callable[[], None]) -> None:
        """Store GPIO backend and callback.

        Args:
            gpio: GPIO backend instance.
            on_basket: Function executed when a basket impulse is detected.
        """
        self.gpio = gpio
        self.on_basket = on_basket

    def setup(self) -> None:
        """Configure sensor pin and edge-detect event with debounce."""
        pull_mode = getattr(self.gpio, config.SENSOR_PULL_UP_DOWN)
        edge = getattr(self.gpio, config.SENSOR_EDGE)

        self.gpio.setup(config.SENSOR_PIN, self.gpio.IN, pull_up_down=pull_mode)
        self.gpio.add_event_detect(
            config.SENSOR_PIN,
            edge,
            callback=self._on_sensor_event,
            bouncetime=config.DEBOUNCE_SENSOR_MS,
        )
        LOGGER.info("Basket sensor ready on GPIO %s", config.SENSOR_PIN)

    def _on_sensor_event(self, channel: int) -> None:
        """Internal GPIO callback for sensor changes.

        Args:
            channel: GPIO channel number triggering the callback.
        """
        _ = channel
        try:
            self.on_basket()
        except Exception:  # pragma: no cover - protect callback thread
            LOGGER.exception("Failed to process basket event.")

    def cleanup(self) -> None:
        """Unregister sensor edge detection."""
        try:
            self.gpio.remove_event_detect(config.SENSOR_PIN)
        except Exception:
            LOGGER.debug("Sensor event detect already removed.")
