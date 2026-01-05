"""Tests for profile report."""

from flower_trait_modeling.profiling.report import ProfileReport
from flower_trait_modeling.domain.models import Profile


def test_profile_report_collects_profiles():
    report = ProfileReport()
    profile = Profile(variety_id="v1", sections={}, summary="demo")
    report.add(profile)
    table = report.to_table()
    assert table[0]["variety_id"] == "v1"
