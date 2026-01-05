"""Tests for reporting summaries."""

from flower_trait_modeling.reporting.summary import render_audit_section, render_profile_section, assemble_report, MarkdownSection
from flower_trait_modeling.analysis.auditor import AuditReport, AuditFinding
from flower_trait_modeling.profiling.report import ProfileReport
from flower_trait_modeling.domain.models import Profile


def test_render_audit_section_counts():
    report = AuditReport(findings=[AuditFinding(field="a", level="info", message="", count=1)])
    section = render_audit_section(report)
    assert "Audit" in section.render()


def test_render_profile_section_contains_variety():
    pr = ProfileReport()
    pr.add(Profile(variety_id="v1", sections={}, summary=""))
    section = render_profile_section(pr)
    assert "v1" in section.render()


def test_assemble_report_concatenates():
    content = assemble_report([MarkdownSection(title="A", lines=["test"])])
    assert "## A" in content
