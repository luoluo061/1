"""Similarity fusion strategies."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .metrics import cosine, jaccard, delta_e
from ..domain.models import FeatureVector
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class FusionConfig:
    weights: Dict[str, float]
    strategy: str = "weighted_sum"


@dataclass
class SimilarityStrategy:
    config: FusionConfig

    def compute_vector_score(self, query: FeatureVector, candidate: FeatureVector) -> float:
        return cosine(query.values, candidate.values)

    def combine(self, vector_score: float, categorical_score: float, color_score: float) -> float:
        if self.config.strategy == "weighted_sum":
            score = (
                vector_score * self.config.weights.get("vector", 1.0)
                + categorical_score * self.config.weights.get("categorical", 0.0)
                + color_score * self.config.weights.get("color", 0.0)
            )
            logger.debug("Combined weighted score", extra={"score": score})
            return score
        return vector_score

    def compare_color(self, a: List[float], b: List[float]) -> float:
        distance = delta_e(a, b)
        return max(0.0, 1.0 - distance / 100.0)

    def compare_categories(self, a: List[str], b: List[str]) -> float:
        return jaccard(a, b)


__all__ = ["FusionConfig", "SimilarityStrategy"]
