"""SQLite persistence layer for match history."""

from __future__ import annotations

import sqlite3
import threading
from pathlib import Path
from typing import Dict, List

import config


class MatchDatabase:
    """Encapsulate SQLite operations with thread-safe access."""

    def __init__(self, db_path: Path, schema_path: Path) -> None:
        """Store file paths for DB and schema initialization."""
        self.db_path = Path(db_path)
        self.schema_path = Path(schema_path)
        self._lock = threading.Lock()

    def initialize(self) -> None:
        """Create database tables if they do not exist."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        schema_sql = self.schema_path.read_text(encoding="utf-8")

        with self._connect() as conn:
            conn.executescript(schema_sql)
            conn.commit()

    def insert_match(self, score: int, duration: int, timestamp: str) -> None:
        """Insert one match result row."""
        with self._lock:
            with self._connect() as conn:
                conn.execute(
                    "INSERT INTO matches (score, duration, timestamp) VALUES (?, ?, ?)",
                    (score, duration, timestamp),
                )
                conn.commit()

    def get_best_score(self) -> int:
        """Return maximum historical score, or 0 if history is empty."""
        with self._lock:
            with self._connect() as conn:
                row = conn.execute("SELECT MAX(score) FROM matches").fetchone()
                return int(row[0]) if row and row[0] is not None else 0

    def get_history(self, limit: int = config.HISTORY_LIMIT) -> List[Dict[str, object]]:
        """Return latest matches ordered by timestamp descending."""
        with self._lock:
            with self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT match_id, score, duration, timestamp
                    FROM matches
                    ORDER BY match_id DESC
                    LIMIT ?
                    """,
                    (limit,),
                ).fetchall()

        return [
            {
                "match_id": row[0],
                "score": row[1],
                "duration": row[2],
                "timestamp": row[3],
            }
            for row in rows
        ]

    def _connect(self) -> sqlite3.Connection:
        """Create a new SQLite connection with row tuple results."""
        return sqlite3.connect(self.db_path)
