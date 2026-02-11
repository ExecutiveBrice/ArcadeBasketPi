"""Scoring orchestration service."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Dict

from core.state import MatchState
from storage.db import MatchDatabase

LOGGER = logging.getLogger(__name__)


class ScorerService:
    """Coordinate scoring events, LEDs, sound, and persistence."""

    def __init__(self, state: MatchState, db: MatchDatabase, leds, sound_player) -> None:
        """Store all collaborators used by scoring flow."""
        self.state = state
        self.db = db
        self.leds = leds
        self.sound_player = sound_player

    def start_match(self) -> None:
        """Start a fresh match and enable active LED."""
        if self.state.snapshot()["active"]:
            return
        self.state.start_match()
        self.leds.set_match_active(True)
        LOGGER.info("Match started.")

    def basket_scored(self) -> None:
        """Handle one valid basket event."""
        snapshot = self.state.snapshot()
        if not snapshot["active"]:
            return

        score = self.state.basket_scored()
        self.leds.pulse_score_led()
        self.sound_player.play_basket_sound()
        LOGGER.info("Basket counted. Score=%s", score)

    def reset_match(self) -> None:
        """Finalize active match to DB, then start a fresh one."""
        self._save_and_stop_if_active()
        self.start_match()

    def stop_match(self) -> None:
        """Finalize active match to DB and mark match as inactive."""
        self._save_and_stop_if_active()

    def _save_and_stop_if_active(self) -> None:
        """Persist current active match and switch off active LED."""
        snapshot = self.state.snapshot()
        if not snapshot["active"]:
            self.leds.set_match_active(False)
            return

        score, duration, _ = self.state.stop_match()
        self.leds.set_match_active(False)

        if duration > 0 or score > 0:
            timestamp = datetime.now(timezone.utc).isoformat()
            self.db.insert_match(score=score, duration=duration, timestamp=timestamp)
            LOGGER.info("Match saved. score=%s duration=%ss", score, duration)

    def status_payload(self) -> Dict[str, object]:
        """Build API payload for current status and best score."""
        state = self.state.snapshot()
        best_score = self.db.get_best_score()
        return {
            **state,
            "best_score": best_score,
        }
