"""Categorical normalization."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from .base import Normalizer
from ..utils.errors import ValidationError


@dataclass
class CategoricalNormalizer(Normalizer):
    """Validate categorical value against allowed set."""

    allowed: List[str]
    mapping: Dict[str, str] | None = None

    def normalize(self, value: Any) -> str:
        raw = str(value).strip().lower()
        mapped = self.mapping.get(raw, raw) if self.mapping else raw
        if mapped not in self.allowed:
            raise ValidationError(self.field, f"unexpected category '{mapped}'")
        return mapped


@dataclass
class OrdinalNormalizer(Normalizer):
    """Map ordinal categories to numerical ranks."""

    order: List[str]

    def normalize(self, value: Any) -> float:
        raw = str(value).strip().lower()
        if raw not in self.order:
            raise ValidationError(self.field, f"{raw} not in order list")
        return float(self.order.index(raw))


__all__ = ["CategoricalNormalizer", "OrdinalNormalizer"]
