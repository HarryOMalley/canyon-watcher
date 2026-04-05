import sqlite3
from datetime import datetime
from pathlib import Path

from application.ports.repository import ObservationRepository
from domain.enums import StockState
from domain.models import StockObservation


class SQLiteObservationRepository(ObservationRepository):
    """SQLite implementation of the ObservationRepository protocol."""

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        try:
            with self._get_connection() as conn:
                conn.execute(
                    """
                    CREATE TABLE IF NOT EXISTS observations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        target_id TEXT NOT NULL,
                        timestamp TEXT NOT NULL,
                        state TEXT NOT NULL,
                        is_buyable INTEGER NOT NULL,
                        price TEXT,
                        availability_text TEXT,
                        config_match INTEGER NOT NULL
                    )
                    """
                )
                conn.execute(
                    """
                    CREATE INDEX IF NOT EXISTS idx_target_timestamp
                    ON observations (target_id, timestamp DESC)
                    """
                )
        except sqlite3.Error as e:
            raise RuntimeError(
                f"Failed to initialize database at {self.db_path}: {e}. "
                "Ensure the directory exists and is writable."
            ) from e

    def save(self, observation: StockObservation) -> None:
        with self._get_connection() as conn:
            conn.execute(
                """
                INSERT INTO observations (
                    target_id, timestamp, state, is_buyable,
                    price, availability_text, config_match
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    observation.target_id,
                    observation.timestamp.isoformat(),
                    observation.state.value,
                    1 if observation.is_buyable else 0,
                    observation.price,
                    observation.availability_text,
                    1 if observation.config_match else 0,
                ),
            )

    def get_latest(self, target_id: str) -> StockObservation | None:
        with self._get_connection() as conn:
            row = conn.execute(
                """
                SELECT
                    target_id, timestamp, state, is_buyable,
                    price, availability_text, config_match
                FROM observations
                WHERE target_id = ?
                ORDER BY timestamp DESC
                LIMIT 1
                """,
                (target_id,),
            ).fetchone()

            if not row:
                return None

            return StockObservation(
                target_id=row["target_id"],
                timestamp=datetime.fromisoformat(row["timestamp"]),
                state=StockState(row["state"]),
                is_buyable=bool(row["is_buyable"]),
                price=row["price"],
                availability_text=row["availability_text"],
                config_match=bool(row["config_match"]),
            )
