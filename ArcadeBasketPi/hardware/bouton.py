"""Physical reset/start button module."""

from __future__ import annotations

import logging
from typing import Callable

import config

LOGGER = logging.getLogger(__name__)


class ResetButton:
    """Manage the GPIO reset/start button with debounce."""

    def __init__(self, gpio, on_press: Callable[[], None]) -> None:
        """Create button handler.

        Args:
            gpio: GPIO backend instance.
            on_press: Function called when button is pressed.
        """
        self.gpio = gpio
        self.on_press = on_press

    def setup(self) -> None:
        """Configure button pin and edge-detect event."""
        pull_mode = getattr(self.gpio, config.BUTTON_PULL_UP_DOWN)
        edge = getattr(self.gpio, config.BUTTON_EDGE)

        self.gpio.setup(config.RESET_BUTTON_PIN, self.gpio.IN, pull_up_down=pull_mode)
        self.gpio.add_event_detect(
            config.RESET_BUTTON_PIN,
            edge,
            callback=self._on_button_event,
            bouncetime=config.DEBOUNCE_BUTTON_MS,
        )
        LOGGER.info("Reset button ready on GPIO %s", config.RESET_BUTTON_PIN)

    def _on_button_event(self, channel: int) -> None:
        """Internal callback that executes the reset/start action."""
        _ = channel
        try:
            self.on_press()
        except Exception:  # pragma: no cover
            LOGGER.exception("Failed to process reset button press.")

    def cleanup(self) -> None:
        """Unregister button edge detection."""
        try:
            self.gpio.remove_event_detect(config.RESET_BUTTON_PIN)
        except Exception:
            LOGGER.debug("Button event detect already removed.")
