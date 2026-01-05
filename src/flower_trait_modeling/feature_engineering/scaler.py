"""Scaling utilities for feature vectors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class VectorScaler:
    """Apply simple scaling strategies to feature vectors."""

    strategy: str = "unit"

    def scale(self, values: List[float]) -> List[float]:
        if self.strategy == "unit":
            return self._unit_scale(values)
        if self.strategy == "max_abs":
            return self._max_abs(values)
        return values

    def _unit_scale(self, values: List[float]) -> List[float]:
        import math

        norm = math.sqrt(sum(v * v for v in values)) or 1.0
        scaled = [v / norm for v in values]
        logger.debug("Unit scaled", extra={"norm": norm})
        return scaled

    def _max_abs(self, values: List[float]) -> List[float]:
        max_abs = max(abs(v) for v in values) or 1.0
        scaled = [v / max_abs for v in values]
        logger.debug("Max-abs scaled", extra={"max_abs": max_abs})
        return scaled


__all__ = ["VectorScaler"]
