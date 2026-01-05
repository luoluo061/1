"""Tests for evaluation metrics."""

from flower_trait_modeling.evaluation.metrics import precision_at_k, coverage, ConsistencyReport


def test_precision_at_k_basic():
    score = precision_at_k(["a", "b"], ["a", "c", "d"], k=2)
    assert score == 0.5


def test_coverage_computes_ratio():
    score = coverage(["a", "b"], ["b", "c"])
    assert score == 0.5


def test_consistency_report_uses_cosine():
    report = ConsistencyReport.from_vectors([1.0, 0.0], [1.0, 0.0])
    assert report.cosine == 1.0
