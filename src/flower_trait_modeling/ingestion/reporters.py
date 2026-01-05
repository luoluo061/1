"""Reporting helpers for ingestion phase."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ValidationIssue:
    field: str
    message: str
    record: Dict[str, object]


@dataclass
class IngestionReport:
    total: int
    accepted: int
    rejected: int
    issues: List[ValidationIssue] = field(default_factory=list)

    def to_dict(self) -> Dict[str, object]:
        return {
            "total": self.total,
            "accepted": self.accepted,
            "rejected": self.rejected,
            "issues": [issue.__dict__ for issue in self.issues],
        }

    def log(self) -> None:
        logger.info("Ingestion report", extra=self.to_dict())


def build_report(records: List[Dict[str, object]], valid_ids: List[str]) -> IngestionReport:
    issues: List[ValidationIssue] = []
    for record in records:
        if record.get("variety_id") not in valid_ids:
            issues.append(ValidationIssue(field="variety_id", message="failed validation", record=record))
    report = IngestionReport(total=len(records), accepted=len(valid_ids), rejected=len(records) - len(valid_ids), issues=issues)
    report.log()
    return report


__all__ = ["ValidationIssue", "IngestionReport", "build_report"]
