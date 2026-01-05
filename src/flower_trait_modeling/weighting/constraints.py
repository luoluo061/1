"""Constraint helpers for weight configuration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from ..utils.errors import ValidationError


@dataclass
class WeightConstraints:
    min_weight: float = 0.0
    max_weight: float = 1.0
    normalization: str = "l1"

    def enforce(self, weights: Dict[str, float]) -> Dict[str, float]:
        for key, value in weights.items():
            if value < self.min_weight or value > self.max_weight:
                raise ValidationError(key, f"weight {value} violates constraints")
        if self.normalization == "l1":
            total = sum(weights.values()) or 1.0
            return {k: v / total for k, v in weights.items()}
        return weights


__all__ = ["WeightConstraints"]
