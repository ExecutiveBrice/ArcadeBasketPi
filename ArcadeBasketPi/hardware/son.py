"""Sound feedback module using ALSA aplay."""

from __future__ import annotations

import logging
import subprocess
from pathlib import Path

LOGGER = logging.getLogger(__name__)


class SoundPlayer:
    """Play short sound effects asynchronously with `aplay`."""

    def __init__(self, sound_file: Path) -> None:
        """Store wav file path.

        Args:
            sound_file: Path to wav file played for each basket.
        """
        self.sound_file = Path(sound_file)

    def play_basket_sound(self) -> None:
        """Play basket sound if file exists and ALSA is available."""
        if not self.sound_file.exists():
            LOGGER.warning("Sound file missing: %s", self.sound_file)
            return

        try:
            subprocess.Popen(
                ["aplay", "-q", str(self.sound_file)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except FileNotFoundError:
            LOGGER.warning("`aplay` not found. Install ALSA utilities.")
        except Exception:
            LOGGER.exception("Failed to play basket sound.")
