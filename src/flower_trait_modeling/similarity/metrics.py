"""Similarity metric implementations."""

from __future__ import annotations

from typing import Iterable, List

from ..utils.logging import get_logger

logger = get_logger(__name__)


def cosine(a: List[float], b: List[float]) -> float:
    import math

    if len(a) != len(b):
        raise ValueError("vectors must be same length")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a)) or 1.0
    norm_b = math.sqrt(sum(y * y for y in b)) or 1.0
    score = dot / (norm_a * norm_b)
    logger.debug("Cosine computed", extra={"score": score})
    return score


def jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    set_a, set_b = set(a), set(b)
    intersection = len(set_a & set_b)
    union = len(set_a | set_b) or 1
    score = intersection / union
    logger.debug("Jaccard computed", extra={"score": score})
    return score


def delta_e(lab_a: List[float], lab_b: List[float]) -> float:
    import math

    diff = math.sqrt(sum((x - y) ** 2 for x, y in zip(lab_a, lab_b)))
    logger.debug("Delta E computed", extra={"diff": diff})
    return diff


__all__ = ["cosine", "jaccard", "delta_e"]
