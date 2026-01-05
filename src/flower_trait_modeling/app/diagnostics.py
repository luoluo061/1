"""Diagnostics helpers to inspect pipeline state."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class DiagnosticProbe:
    name: str
    description: str

    def run(self, payload: Dict[str, object]) -> Dict[str, object]:
        logger.debug("Running diagnostic probe", extra={"name": self.name})
        return {"name": self.name, "status": "ok", "detail": self.description, "payload_keys": list(payload.keys())}


@dataclass
class DiagnosticReport:
    probes: List[DiagnosticProbe]

    def execute(self, payload: Dict[str, object]) -> List[Dict[str, object]]:
        results = [probe.run(payload) for probe in self.probes]
        logger.info("Diagnostics executed", extra={"count": len(results)})
        return results

    def summarize(self, results: List[Dict[str, object]]) -> str:
        lines = ["| Probe | Status | Detail | Keys |", "| --- | --- | --- | --- |"]
        for result in results:
            lines.append(f"| {result['name']} | {result['status']} | {result['detail']} | {','.join(result['payload_keys'])} |")
        summary = "\n".join(lines)
        logger.debug("Diagnostic summary", extra={"lines": len(lines)})
        return summary


@dataclass
class TraceRecord:
    name: str
    payload_snapshot: Dict[str, object]
    note: str


@dataclass
class TraceRecorder:
    """Capture intermediate payloads for later inspection."""

    records: List[TraceRecord]

    def record(self, name: str, payload: Dict[str, object], note: str = "") -> None:
        self.records.append(TraceRecord(name=name, payload_snapshot=dict(payload), note=note))
        logger.debug("Recorded trace", extra={"name": name, "keys": list(payload.keys())})

    def as_markdown(self) -> str:
        lines = ["| Name | Keys | Note |", "| --- | --- | --- |"]
        for record in self.records:
            lines.append(f"| {record.name} | {','.join(record.payload_snapshot.keys())} | {record.note} |")
        return "\n".join(lines)

    def clear(self) -> None:
        self.records.clear()
        logger.info("Trace recorder cleared")


def default_diagnostics() -> DiagnosticReport:
    probes = [
        DiagnosticProbe(name="shape", description="Check presence of flower shape"),
        DiagnosticProbe(name="color", description="Check presence of color information"),
        DiagnosticProbe(name="vase_life", description="Check vase life availability"),
    ]
    return DiagnosticReport(probes=probes)


__all__ = ["DiagnosticProbe", "DiagnosticReport", "TraceRecorder", "TraceRecord", "default_diagnostics"]
