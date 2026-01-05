"""Tests for ingestion reporters."""

from flower_trait_modeling.ingestion.reporters import build_report


def test_build_report_counts_invalid():
    records = [
        {"variety_id": "v1"},
        {"variety_id": "v2"},
    ]
    report = build_report(records, ["v1"])
    assert report.accepted == 1
    assert report.rejected == 1
