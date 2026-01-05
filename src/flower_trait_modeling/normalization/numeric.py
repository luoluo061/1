"""Numeric normalizers for continuous traits."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .base import Normalizer
from ..utils.errors import ValidationError


@dataclass
class MinMaxNormalizer(Normalizer):
    """Scale numeric values between a min and max range."""

    min_value: float
    max_value: float

    def normalize(self, value: Any) -> float:
        try:
            numeric = float(value)
        except (TypeError, ValueError) as exc:
            raise ValidationError(self.field, "not a number") from exc
        if numeric < self.min_value or numeric > self.max_value:
            raise ValidationError(self.field, f"value {numeric} outside [{self.min_value}, {self.max_value}]")
        return (numeric - self.min_value) / (self.max_value - self.min_value)


@dataclass
class LogNormalizer(Normalizer):
    """Apply log transformation for skewed measurements."""

    base: float = 10.0

    def normalize(self, value: Any) -> float:
        import math

        numeric = float(value)
        if numeric <= 0:
            raise ValidationError(self.field, "log requires positive value")
        return math.log(numeric, self.base)


__all__ = ["MinMaxNormalizer", "LogNormalizer"]
