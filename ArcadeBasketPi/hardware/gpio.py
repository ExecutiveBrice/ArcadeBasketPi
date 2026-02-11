"""GPIO abstraction layer with optional fallback when not on Raspberry Pi."""

from __future__ import annotations

import logging
from types import SimpleNamespace
from typing import Callable, Optional

import config

try:
    import RPi.GPIO as GPIO  # type: ignore
except Exception:  # pragma: no cover - fallback is for non-Pi development
    GPIO = None

LOGGER = logging.getLogger(__name__)


class MockGPIO:
    """Minimal mock GPIO API so the app can run outside a Raspberry Pi."""

    BCM = "BCM"
    BOARD = "BOARD"
    IN = "IN"
    OUT = "OUT"
    PUD_UP = "PUD_UP"
    PUD_DOWN = "PUD_DOWN"
    FALLING = "FALLING"
    RISING = "RISING"
    BOTH = "BOTH"
    HIGH = 1
    LOW = 0

    def __init__(self) -> None:
        """Initialize internal state used by the mock implementation."""
        self._pin_state = {}

    def setwarnings(self, enabled: bool) -> None:
        """Ignore warning toggle in mock mode."""
        _ = enabled

    def setmode(self, mode: str) -> None:
        """Ignore mode selection in mock mode."""
        _ = mode

    def setup(self, pin: int, mode: str, pull_up_down: Optional[str] = None, initial: Optional[int] = None) -> None:
        """Register a pin in the mock state map."""
        _ = mode, pull_up_down
        if initial is not None:
            self._pin_state[pin] = initial
        else:
            self._pin_state.setdefault(pin, self.LOW)

    def output(self, pin: int, value: int) -> None:
        """Write a pin value in mock mode."""
        self._pin_state[pin] = value

    def add_event_detect(self, pin: int, edge: str, callback: Callable[[int], None], bouncetime: int = 0) -> None:
        """Log event registration only; no hardware interrupts in mock mode."""
        _ = pin, edge, callback, bouncetime

    def remove_event_detect(self, pin: int) -> None:
        """Ignore event removal in mock mode."""
        _ = pin

    def cleanup(self) -> None:
        """Clear mock state."""
        self._pin_state.clear()


GPIO_BACKEND = GPIO if GPIO is not None else MockGPIO()
IS_REAL_GPIO = GPIO is not None


def configure_gpio() -> SimpleNamespace:
    """Configure base GPIO behavior and return backend constants.

    Returns:
        Namespace containing GPIO object and resolved constants.
    """
    gpio = GPIO_BACKEND
    gpio.setwarnings(False)
    mode = getattr(gpio, config.GPIO_MODE, gpio.BCM)
    gpio.setmode(mode)

    if not IS_REAL_GPIO:
        LOGGER.warning("RPi.GPIO not available; running in mock GPIO mode.")

    return SimpleNamespace(gpio=gpio)


def cleanup_gpio() -> None:
    """Release GPIO resources."""
    GPIO_BACKEND.cleanup()
