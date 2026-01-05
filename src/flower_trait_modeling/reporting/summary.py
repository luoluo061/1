"""Reporting helpers to summarize pipeline status into markdown."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from ..analysis.auditor import AuditReport
from ..profiling.report import ProfileReport
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class MarkdownSection:
    title: str
    lines: List[str]

    def render(self) -> str:
        body = "\n".join(self.lines)
        return f"## {self.title}\n{body}\n"


def render_audit_section(report: AuditReport) -> MarkdownSection:
    counts = report.summarize()
    lines = ["| Level | Count |", "| --- | --- |"]
    for level, count in counts.items():
        lines.append(f"| {level} | {count} |")
    logger.debug("Rendered audit section", extra={"counts": counts})
    return MarkdownSection(title="Audit", lines=lines)


def render_profile_section(report: ProfileReport) -> MarkdownSection:
    table = report.to_table()
    lines = ["| Variety | Sections | Summary Length |", "| --- | --- | --- |"]
    for row in table:
        lines.append(f"| {row['variety_id']} | {row['sections']} | {row['summary_len']} |")
    logger.debug("Rendered profile section", extra={"rows": len(table)})
    return MarkdownSection(title="Profiles", lines=lines)


def assemble_report(sections: List[MarkdownSection]) -> str:
    content = "\n".join(section.render() for section in sections)
    logger.info("Assembled markdown report", extra={"sections": len(sections)})
    return content


__all__ = ["MarkdownSection", "render_audit_section", "render_profile_section", "assemble_report"]
