"""Hash utilities used for deterministic IDs and cache keys."""

from __future__ import annotations

import hashlib
from typing import Iterable

from .logging import get_logger

logger = get_logger(__name__)


def stable_hash(parts: Iterable[str]) -> str:
    """Compute a stable SHA256 hash from iterable string parts.

    Args:
        parts: Iterable pieces to concatenate.

    Returns:
        Hex digest string of the combined parts.
    """

    m = hashlib.sha256()
    for part in parts:
        logger.debug("Adding part to hash", extra={"part": part})
        m.update(part.encode("utf-8"))
    digest = m.hexdigest()
    logger.debug("Computed hash", extra={"digest": digest})
    return digest


def namespaced_hash(namespace: str, value: str) -> str:
    """Create a namespaced hash combining namespace and value."""

    return stable_hash([namespace, value])


__all__ = ["stable_hash", "namespaced_hash"]
