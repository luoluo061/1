"""Similarity engine coordinating metric selection and weighting."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from . import metrics
from ..domain.models import FeatureVector, SimilarityResult
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class SimilarityEngine:
    metric_weights: Dict[str, float]

    def compare(self, query: FeatureVector, candidate: FeatureVector) -> SimilarityResult:
        if query.schema_id != candidate.schema_id:
            raise ValueError("schema mismatch")
        score = metrics.cosine(query.values, candidate.values)
        weighted = score * self.metric_weights.get("vector", 1.0)
        logger.info("Similarity computed", extra={"score": weighted})
        return SimilarityResult(query_id=query.schema_id, candidate_id=candidate.schema_id, score=weighted)

    def explain(self, query: FeatureVector, candidate: FeatureVector, top_k: int = 3) -> List[str]:
        diffs = [abs(a - b) for a, b in zip(query.values, candidate.values)]
        pairs = list(zip(query.mapping, diffs))
        pairs.sort(key=lambda item: item[1])
        explanation = [f"{name} diff={diff:.4f}" for name, diff in pairs[:top_k]]
        logger.debug("Explanation built", extra={"items": explanation})
        return explanation


__all__ = ["SimilarityEngine"]
