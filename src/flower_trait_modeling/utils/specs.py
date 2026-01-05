"""Specification readers for trait and vector schemas.

This module provides structured parsing helpers for configuration-driven
behavior. Each loader returns typed representations that make it easier for
callers to reason about completeness and defaults without manually touching
YAML dictionaries. The goal is readability over runtime performance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .io import read_yaml
from .errors import ConfigurationError
from .logging import get_logger

logger = get_logger(__name__)


@dataclass
class TraitField:
    name: str
    type: str
    required: bool
    description: str = ""
    allowed: Optional[List[str]] = None
    min_value: Optional[float] = None
    max_value: Optional[float] = None

    def validate_value(self, value: object) -> None:
        if value is None and self.required:
            raise ConfigurationError(f"Trait {self.name} is required but value missing")
        if self.allowed and str(value) not in self.allowed:
            raise ConfigurationError(f"Trait {self.name} must be in {self.allowed}")
        if self.min_value is not None and float(value) < self.min_value:
            raise ConfigurationError(f"Trait {self.name} below minimum {self.min_value}")
        if self.max_value is not None and float(value) > self.max_value:
            raise ConfigurationError(f"Trait {self.name} above maximum {self.max_value}")


@dataclass
class TraitSpec:
    """Represents the full trait schema."""

    fields: List[TraitField] = field(default_factory=list)

    @classmethod
    def from_file(cls, path: str) -> "TraitSpec":
        data = read_yaml(path)
        traits = []
        for entry in data.get("traits", []):
            traits.append(
                TraitField(
                    name=entry.get("name"),
                    type=entry.get("type"),
                    required=bool(entry.get("required", False)),
                    description=entry.get("description", ""),
                    allowed=entry.get("allowed"),
                    min_value=entry.get("min"),
                    max_value=entry.get("max"),
                )
            )
        logger.info("Trait spec loaded", extra={"count": len(traits)})
        return cls(fields=traits)

    def required_fields(self) -> List[str]:
        return [f.name for f in self.fields if f.required]

    def as_dict(self) -> Dict[str, Dict[str, object]]:
        return {
            field.name: {
                "type": field.type,
                "required": field.required,
                "description": field.description,
                "allowed": field.allowed or [],
                "range": (field.min_value, field.max_value),
            }
            for field in self.fields
        }


@dataclass
class VectorDimension:
    name: str
    kind: str
    width: int
    extras: Dict[str, object] = field(default_factory=dict)


@dataclass
class VectorSpec:
    schema_id: str
    dimensions: List[VectorDimension]

    @classmethod
    def from_file(cls, path: str) -> "VectorSpec":
        data = read_yaml(path)
        schema_data = data.get("schema")
        if not schema_data:
            raise ConfigurationError("Missing schema block")
        dims: List[VectorDimension] = []
        for entry in schema_data.get("dimensions", []):
            kind = entry.get("type")
            name = entry.get("name")
            if not kind or not name:
                raise ConfigurationError("Dimension missing name or type")
            width = _infer_width(kind, entry)
            dims.append(VectorDimension(name=name, kind=kind, width=width, extras={k: v for k, v in entry.items() if k not in {"name", "type"}}))
        logger.info("Vector spec loaded", extra={"dimensions": len(dims)})
        return cls(schema_id=schema_data.get("id", "unknown"), dimensions=dims)

    def width(self) -> int:
        return sum(dim.width for dim in self.dimensions)

    def describe(self) -> str:
        parts = [f"- {dim.name}: {dim.kind} ({dim.width})" for dim in self.dimensions]
        description = "\n".join(parts)
        logger.debug("Vector spec described", extra={"text": description})
        return description


def _infer_width(kind: str, entry: Dict[str, object]) -> int:
    if kind == "one_hot":
        return len(entry.get("vocab", []))
    if kind == "color_lab":
        return 3
    return 1


__all__ = ["TraitField", "TraitSpec", "VectorDimension", "VectorSpec"]
