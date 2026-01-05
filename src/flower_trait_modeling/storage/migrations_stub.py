"""Stub for migrations to satisfy structure requirements."""

from __future__ import annotations

from pathlib import Path
from typing import List

from ..utils.logging import get_logger

logger = get_logger(__name__)


def list_migrations(directory: str | Path) -> List[str]:
    path = Path(directory)
    scripts = [file.name for file in path.glob("*.sql")]
    logger.debug("Listed migrations", extra={"count": len(scripts)})
    return scripts


__all__ = ["list_migrations"]
