"""Tests for similarity engine."""

from flower_trait_modeling.similarity.engine import SimilarityEngine
from flower_trait_modeling.domain.models import FeatureVector


def test_similarity_returns_score():
    engine = SimilarityEngine({"vector": 1.0})
    a = FeatureVector(schema_id="s", values=[1.0, 0.0], mapping=["x", "y"])
    b = FeatureVector(schema_id="s", values=[1.0, 0.0], mapping=["x", "y"])
    result = engine.compare(a, b)
    assert result.score == 1.0


def test_explain_returns_top_features():
    engine = SimilarityEngine({"vector": 1.0})
    a = FeatureVector(schema_id="s", values=[1.0, 0.0, 0.5], mapping=["x", "y", "z"])
    b = FeatureVector(schema_id="s", values=[0.5, 0.0, 0.25], mapping=["x", "y", "z"])
    explanation = engine.explain(a, b, top_k=2)
    assert len(explanation) == 2
