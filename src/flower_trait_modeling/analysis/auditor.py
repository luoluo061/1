"""Auditing utilities to review dataset completeness and schema adherence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from ..utils.specs import TraitSpec
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class AuditFinding:
    field: str
    level: str
    message: str
    count: int = 0


@dataclass
class AuditReport:
    findings: List[AuditFinding] = field(default_factory=list)

    def add(self, field: str, level: str, message: str, count: int = 0) -> None:
        self.findings.append(AuditFinding(field=field, level=level, message=message, count=count))

    def by_level(self, level: str) -> List[AuditFinding]:
        return [finding for finding in self.findings if finding.level == level]

    def summarize(self) -> Dict[str, int]:
        summary: Dict[str, int] = {}
        for finding in self.findings:
            summary[finding.level] = summary.get(finding.level, 0) + 1
        logger.info("Audit summary", extra=summary)
        return summary


@dataclass
class DatasetAuditor:
    trait_spec: TraitSpec

    def audit_records(self, records: List[Dict[str, object]]) -> AuditReport:
        report = AuditReport()
        for record in records:
            self._audit_single(record, report)
        report.summarize()
        return report

    def _audit_single(self, record: Dict[str, object], report: AuditReport) -> None:
        for field in self.trait_spec.fields:
            value = record.get(field.name)
            if field.required and (value is None or str(value) == ""):
                report.add(field.name, "error", "missing required value", 1)
            elif value is None:
                report.add(field.name, "warning", "optional value absent", 1)
            else:
                report.add(field.name, "info", "value present", 1)
        logger.debug("Audited record", extra={"variety_id": record.get("variety_id")})


def audit_from_config(config_path: str, records: List[Dict[str, object]]) -> AuditReport:
    spec = TraitSpec.from_file(config_path)
    auditor = DatasetAuditor(spec)
    return auditor.audit_records(records)


__all__ = ["AuditFinding", "AuditReport", "DatasetAuditor", "audit_from_config"]
