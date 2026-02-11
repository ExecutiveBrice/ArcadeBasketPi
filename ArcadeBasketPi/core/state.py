"""Thread-safe in-memory match state."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
import threading
from typing import Dict, Optional, Tuple


@dataclass
class MatchState:
    """Represent current match state shared by GPIO and Flask threads."""

    score: int = 0
    active: bool = False
    started_at: Optional[datetime] = None
    lock: threading.Lock = field(default_factory=threading.Lock)

    def start_match(self) -> None:
        """Start a new active match and reset score/time."""
        with self.lock:
            self.score = 0
            self.active = True
            self.started_at = datetime.now(timezone.utc)

    def basket_scored(self) -> int:
        """Increment score if match is active.

        Returns:
            Updated score.
        """
        with self.lock:
            if not self.active:
                return self.score
            self.score += 1
            return self.score

    def stop_match(self) -> Tuple[int, int, Optional[datetime]]:
        """Stop current match and return final metrics.

        Returns:
            Tuple of (score, duration_seconds, started_at).
        """
        with self.lock:
            score = self.score
            started_at = self.started_at
            duration = 0
            if started_at is not None:
                duration = int((datetime.now(timezone.utc) - started_at).total_seconds())

            self.active = False
            self.score = 0
            self.started_at = None
            return score, duration, started_at

    def snapshot(self) -> Dict[str, object]:
        """Return a consistent view of live match status for web/API use."""
        with self.lock:
            elapsed = 0
            if self.active and self.started_at is not None:
                elapsed = int((datetime.now(timezone.utc) - self.started_at).total_seconds())

            return {
                "score": self.score,
                "active": self.active,
                "elapsed_seconds": elapsed,
            }
