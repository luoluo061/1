"""Tests for normalization reporters."""

from flower_trait_modeling.normalization.reporters import capture_pipeline


def test_capture_pipeline_returns_report():
    payload = {"a": 1, "b": 2}
    report = capture_pipeline(payload, ["a", "b"])
    assert report.summarize()["a"] == 1
