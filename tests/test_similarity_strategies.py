"""Tests for similarity strategies."""

from flower_trait_modeling.similarity.strategies import SimilarityStrategy, FusionConfig
from flower_trait_modeling.domain.models import FeatureVector


def test_similarity_strategy_combines_scores():
    strategy = SimilarityStrategy(FusionConfig(weights={"vector": 0.7, "categorical": 0.2, "color": 0.1}))
    combined = strategy.combine(1.0, 0.5, 0.5)
    assert round(combined, 2) == 0.85


def test_compare_color_returns_scaled_score():
    strategy = SimilarityStrategy(FusionConfig(weights={"vector": 1.0}))
    score = strategy.compare_color([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    assert score == 1.0


def test_compare_categories_uses_jaccard():
    strategy = SimilarityStrategy(FusionConfig(weights={"vector": 1.0}))
    score = strategy.compare_categories(["a", "b"], ["b", "c"])
    assert 0 <= score <= 1
