"""Vector builder that maps normalized payloads to numeric vectors."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .vector_schema import VectorSchema
from . import encoders
from ..domain.models import FeatureVector
from ..utils.errors import ValidationError
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class VectorBuilder:
    schema: VectorSchema

    def build(self, payload: Dict[str, object]) -> FeatureVector:
        """Build a feature vector according to the schema."""

        values: List[float] = []
        mapping: List[str] = []
        for dimension in self.schema.dimensions:
            field_value = payload.get(dimension.name)
            if field_value is None:
                raise ValidationError(dimension.name, "missing value for vectorization")
            encoded = self._encode_dimension(dimension.type, field_value, dimension.config)
            values.extend(encoded)
            mapping.extend([dimension.name] * len(encoded))
        vector = FeatureVector(schema_id=self.schema.schema_id, values=values, mapping=mapping)
        vector.ensure_dimension(expected=self.schema.total_width())
        logger.info("Vector built", extra={"schema": self.schema.schema_id, "width": len(values)})
        return vector

    def _encode_dimension(self, dtype: str, value: object, config: Dict[str, object]) -> List[float]:
        if dtype == "one_hot":
            return encoders.one_hot(str(value), config.get("vocab", []))
        if dtype == "scaled_numeric":
            return encoders.passthrough(float(value))
        if dtype == "color_lab":
            return encoders.lab_to_vector(value)  # type: ignore[arg-type]
        if dtype == "ordinal":
            return encoders.ordinal(float(value), len(config.get("order", [])))
        if dtype == "cyclical":
            return encoders.passthrough(float(value))
        raise ValidationError(dtype, "unknown dimension type")


__all__ = ["VectorBuilder"]
