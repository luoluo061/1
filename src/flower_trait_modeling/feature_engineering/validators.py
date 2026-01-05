"""Validators for feature vectors to ensure structural integrity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..domain.models import FeatureVector
from ..utils.errors import ValidationError
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class VectorValidator:
    expected_width: int

    def validate(self, vector: FeatureVector) -> None:
        if len(vector.values) != self.expected_width:
            raise ValidationError("vector", f"expected width {self.expected_width}, got {len(vector.values)}")
        if any(v is None for v in vector.values):
            raise ValidationError("vector", "contains None values")
        if not vector.mapping:
            raise ValidationError("mapping", "mapping missing or empty")
        logger.debug("Vector validated", extra={"width": len(vector.values)})


@dataclass
class DimensionExpectation:
    name: str
    min_value: float = 0.0
    max_value: float = 1.0

    def enforce(self, vector: FeatureVector) -> None:
        for value, feature in zip(vector.values, vector.mapping):
            if feature == self.name and (value < self.min_value or value > self.max_value):
                raise ValidationError(feature, f"value {value} outside [{self.min_value}, {self.max_value}]")


def run_expectations(vector: FeatureVector, expectations: List[DimensionExpectation]) -> None:
    for expectation in expectations:
        expectation.enforce(vector)
    logger.info("Expectations executed", extra={"count": len(expectations)})


__all__ = ["VectorValidator", "DimensionExpectation", "run_expectations"]
