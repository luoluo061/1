"""Evaluation metrics for the modeling pipeline."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..similarity import metrics as sim_metrics
from ..utils.logging import get_logger

logger = get_logger(__name__)


def precision_at_k(relevants: List[str], retrieved: List[str], k: int = 5) -> float:
    top_k = retrieved[:k]
    true_positive = len([item for item in top_k if item in relevants])
    score = true_positive / (k or 1)
    logger.debug("Precision@k computed", extra={"score": score})
    return score


def coverage(expected: List[str], retrieved: List[str]) -> float:
    intersection = len(set(expected) & set(retrieved))
    score = intersection / (len(expected) or 1)
    logger.debug("Coverage computed", extra={"score": score})
    return score


@dataclass
class ConsistencyReport:
    cosine: float
    jaccard: float
    delta_e: float

    @classmethod
    def from_vectors(cls, a: List[float], b: List[float]) -> "ConsistencyReport":
        return cls(cosine=sim_metrics.cosine(a, b), jaccard=0.0, delta_e=0.0)


__all__ = ["precision_at_k", "coverage", "ConsistencyReport"]
