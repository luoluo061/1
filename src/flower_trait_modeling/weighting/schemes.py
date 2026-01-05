"""Weight scheme definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from ..utils.errors import ValidationError


@dataclass
class WeightScheme:
    name: str
    weights: Dict[str, float]

    def normalize(self) -> None:
        total = sum(self.weights.values())
        if total <= 0:
            raise ValidationError("weights", "sum must be positive")
        for key in list(self.weights.keys()):
            self.weights[key] = self.weights[key] / total


@dataclass
class WeightConstraint:
    min_weight: float
    max_weight: float

    def validate(self, weights: Dict[str, float]) -> None:
        for key, value in weights.items():
            if value < self.min_weight or value > self.max_weight:
                raise ValidationError(key, f"weight {value} outside bounds")


__all__ = ["WeightScheme", "WeightConstraint"]
