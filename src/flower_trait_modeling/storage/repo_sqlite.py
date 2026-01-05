"""SQLite repository stub for demonstration."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List

from ..domain.models import FeatureVector
from ..utils.logging import get_logger

logger = get_logger(__name__)


class SQLiteRepository:
    path: Path

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._ensure_tables()

    def _ensure_tables(self) -> None:
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS feature_vectors (
                schema_id TEXT,
                values_json TEXT
            )
            """
        )
        conn.commit()
        conn.close()
        logger.debug("Ensured SQLite tables")

    def save_vector(self, vector: FeatureVector) -> None:
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute("INSERT INTO feature_vectors (schema_id, values_json) VALUES (?, ?)", (vector.schema_id, str(vector.values)))
        conn.commit()
        conn.close()
        logger.info("Stored vector in sqlite", extra={"schema_id": vector.schema_id})

    def load_vectors(self) -> List[FeatureVector]:
        conn = sqlite3.connect(self.path)
        cur = conn.cursor()
        cur.execute("SELECT schema_id, values_json FROM feature_vectors")
        rows = cur.fetchall()
        conn.close()
        vectors = [FeatureVector(schema_id=row[0], values=[float(x) for x in row[1].strip("[]").split(',')], mapping=[]) for row in rows]
        logger.debug("Loaded vectors", extra={"count": len(vectors)})
        return vectors


__all__ = ["SQLiteRepository"]
