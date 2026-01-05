"""Reporting utilities for evaluation results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from .metrics import precision_at_k, coverage
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class EvaluationCase:
    name: str
    relevants: List[str]
    retrieved: List[str]
    k: int = 5


@dataclass
class EvaluationReport:
    cases: List[EvaluationCase] = field(default_factory=list)
    scores: Dict[str, Dict[str, float]] = field(default_factory=dict)

    def add_case(self, case: EvaluationCase) -> None:
        self.cases.append(case)

    def run(self) -> None:
        for case in self.cases:
            p_at_k = precision_at_k(case.relevants, case.retrieved, case.k)
            cov = coverage(case.relevants, case.retrieved)
            self.scores[case.name] = {"precision_at_k": p_at_k, "coverage": cov}
            logger.info("Evaluation case computed", extra={"name": case.name, "scores": self.scores[case.name]})

    def as_markdown(self) -> str:
        lines = ["| Case | Precision@K | Coverage |", "| --- | --- | --- |"]
        for name, metrics in self.scores.items():
            lines.append(f"| {name} | {metrics['precision_at_k']:.2f} | {metrics['coverage']:.2f} |")
        return "\n".join(lines)


__all__ = ["EvaluationCase", "EvaluationReport"]
