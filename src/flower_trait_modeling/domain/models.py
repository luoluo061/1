"""Domain models capturing flower trait structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .enums import FlowerShape, Fragrance, Seasonality
from ..utils.errors import ValidationError
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class TraitValue:
    """Generic trait value container with provenance."""

    name: str
    raw: str | float | int
    normalized: float | str | None = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class FlowerVariety:
    """Core domain model describing a flower variety."""

    variety_id: str
    species: str
    flower_shape: FlowerShape
    flower_diameter_cm: float
    color_primary: str
    stem_length_cm: float
    vase_life_days: float
    fragrance: Fragrance = Fragrance.NONE
    seasonality: Seasonality = Seasonality.ALL
    traits: List[TraitValue] = field(default_factory=list)

    def validate(self) -> None:
        """Validate fields with basic constraints."""

        if not self.variety_id:
            raise ValidationError("variety_id", "must not be empty")
        if self.flower_diameter_cm <= 0:
            raise ValidationError("flower_diameter_cm", "must be positive")
        if self.stem_length_cm <= 0:
            raise ValidationError("stem_length_cm", "must be positive")
        if self.vase_life_days <= 0:
            raise ValidationError("vase_life_days", "must be positive")
        logger.debug("Validated FlowerVariety", extra={"variety_id": self.variety_id})

    def to_record(self) -> Dict[str, str | float]:
        """Convert to flat record for serialization."""

        return {
            "variety_id": self.variety_id,
            "species": self.species,
            "flower_shape": self.flower_shape.value,
            "flower_diameter_cm": self.flower_diameter_cm,
            "color_primary": self.color_primary,
            "stem_length_cm": self.stem_length_cm,
            "vase_life_days": self.vase_life_days,
            "fragrance": self.fragrance.value,
            "seasonality": self.seasonality.value,
        }


@dataclass
class FeatureVector:
    """Container for feature vector and schema id."""

    schema_id: str
    values: List[float]
    mapping: List[str]

    def ensure_dimension(self, expected: int) -> None:
        """Validate dimension size."""

        if len(self.values) != expected:
            raise ValidationError("feature_vector", f"expected {expected} values, got {len(self.values)}")
        logger.debug("FeatureVector dimension ok", extra={"expected": expected})


@dataclass
class SimilarityResult:
    """Similarity result with explanation."""

    query_id: str
    candidate_id: str
    score: float
    highlights: List[str] = field(default_factory=list)


@dataclass
class Profile:
    """Profile output structure for a variety."""

    variety_id: str
    sections: Dict[str, Dict[str, str | float]]
    summary: str
    vector_snapshot: Optional[FeatureVector] = None


__all__ = [
    "TraitValue",
    "FlowerVariety",
    "FeatureVector",
    "SimilarityResult",
    "Profile",
]
