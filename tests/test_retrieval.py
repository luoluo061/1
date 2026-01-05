"""Tests for retrieval engine."""

from flower_trait_modeling.similarity.engine import SimilarityEngine
from flower_trait_modeling.similarity.retrieval import RetrievalEngine
from flower_trait_modeling.domain.models import FeatureVector


def test_retrieval_sorts_by_score():
    engine = SimilarityEngine({"vector": 1.0})
    retriever = RetrievalEngine(engine)
    query = FeatureVector(schema_id="s", values=[1.0, 0.0], mapping=["a", "b"])
    candidates = [
        FeatureVector(schema_id="s", values=[0.0, 1.0], mapping=["a", "b"]),
        FeatureVector(schema_id="s", values=[1.0, 0.0], mapping=["a", "b"]),
    ]
    results = retriever.search(query, candidates, top_k=1)
    assert len(results) == 1
    assert results[0].score <= 1.0
