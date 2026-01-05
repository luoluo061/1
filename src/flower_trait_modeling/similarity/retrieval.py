"""Retrieval layer for similarity search."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List

from .engine import SimilarityEngine
from ..domain.models import FeatureVector, SimilarityResult
from ..utils.logging import get_logger

logger = get_logger(__name__)


def _normalize_scores(results: List[SimilarityResult]) -> List[SimilarityResult]:
    if not results:
        return results
    max_score = max(r.score for r in results) or 1.0
    for r in results:
        r.score = r.score / max_score
    return results


@dataclass
class RetrievalEngine:
    engine: SimilarityEngine

    def search(self, query: FeatureVector, candidates: Iterable[FeatureVector], top_k: int = 5) -> List[SimilarityResult]:
        results = [self.engine.compare(query, candidate) for candidate in candidates]
        normalized = _normalize_scores(results)
        normalized.sort(key=lambda item: item.score, reverse=True)
        logger.info("Retrieved candidates", extra={"count": len(normalized)})
        return normalized[:top_k]


__all__ = ["RetrievalEngine"]
