"""Explainability helpers for similarity results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..domain.models import SimilarityResult
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ExplanationBuilder:
    template: str = "{candidate} resembles {query} because: {reasons}"

    def build(self, result: SimilarityResult, reasons: List[str]) -> str:
        message = self.template.format(candidate=result.candidate_id, query=result.query_id, reasons=", ".join(reasons))
        logger.debug("Built explanation", extra={"message": message})
        return message


__all__ = ["ExplanationBuilder"]
