"""Normalization pipeline that orchestrates field normalizers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List

from .base import Normalizer
from .numeric import MinMaxNormalizer
from .categorical import CategoricalNormalizer, OrdinalNormalizer
from .color import ColorNormalizer
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class NormalizationStep:
    field: str
    normalizer: Normalizer

    def apply(self, payload: Dict[str, Any]) -> Any:
        value = payload.get(self.field)
        normalized = self.normalizer(value)
        logger.debug("Normalization step", extra={"field": self.field, "normalized": normalized})
        payload[self.field] = normalized
        return normalized


@dataclass
class NormalizationPipeline:
    """Composable pipeline of normalization steps."""

    steps: List[NormalizationStep] = field(default_factory=list)

    def run(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        for step in self.steps:
            step.apply(payload)
        logger.info("Normalization complete", extra={"fields": list(payload.keys())})
        return payload

    @classmethod
    def default(cls) -> "NormalizationPipeline":
        steps = [
            NormalizationStep("flower_diameter_cm", MinMaxNormalizer("flower_diameter_cm", 0, 40)),
            NormalizationStep("stem_length_cm", MinMaxNormalizer("stem_length_cm", 0, 200)),
            NormalizationStep("vase_life_days", MinMaxNormalizer("vase_life_days", 0, 60)),
            NormalizationStep(
                "flower_shape",
                CategoricalNormalizer("flower_shape", ["single", "double", "pompon", "star", "trumpet"]),
            ),
            NormalizationStep(
                "fragrance",
                OrdinalNormalizer("fragrance", ["none", "light", "medium", "strong"]),
            ),
            NormalizationStep("color_primary", ColorNormalizer("color_primary")),
        ]
        return cls(steps=steps)


__all__ = ["NormalizationStep", "NormalizationPipeline"]
