"""Normalization reporting utilities for traceability."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class FieldNormalization:
    field: str
    raw: Any
    normalized: Any
    note: str = ""


@dataclass
class NormalizationReport:
    entries: List[FieldNormalization] = field(default_factory=list)

    def add(self, field: str, raw: Any, normalized: Any, note: str = "") -> None:
        self.entries.append(FieldNormalization(field=field, raw=raw, normalized=normalized, note=note))

    def summarize(self) -> Dict[str, Any]:
        return {entry.field: entry.normalized for entry in self.entries}

    def log(self) -> None:
        logger.info("Normalization report", extra={"fields": [e.field for e in self.entries]})


def capture_pipeline(payload: Dict[str, Any], steps: List[str]) -> NormalizationReport:
    report = NormalizationReport()
    for field in steps:
        report.add(field, payload.get(field), payload.get(field), note="post-pipeline")
    report.log()
    return report


__all__ = ["FieldNormalization", "NormalizationReport", "capture_pipeline"]
