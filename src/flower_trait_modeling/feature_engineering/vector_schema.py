"""Vector schema parsing and validation."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from ..utils.errors import ConfigurationError
from ..utils.io import read_yaml
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class Dimension:
    name: str
    type: str
    config: Dict[str, object]

    @property
    def width(self) -> int:
        if self.type == "one_hot":
            return len(self.config.get("vocab", []))
        if self.type == "color_lab":
            return 3
        return 1


@dataclass
class VectorSchema:
    """Vector schema derived from YAML configuration."""

    schema_id: str
    dimensions: List[Dimension]

    @classmethod
    def from_file(cls, path: str) -> "VectorSchema":
        data = read_yaml(path)
        if "schema" not in data:
            raise ConfigurationError("vector schema missing root key")
        schema_data = data["schema"]
        dims = [
            Dimension(name=entry["name"], type=entry["type"], config={k: v for k, v in entry.items() if k not in {"name", "type"}})
            for entry in schema_data.get("dimensions", [])
        ]
        logger.debug("Vector schema loaded", extra={"dimensions": len(dims)})
        return cls(schema_id=schema_data.get("id", "unknown"), dimensions=dims)

    def total_width(self) -> int:
        width = sum(d.width for d in self.dimensions)
        logger.debug("Computed total width", extra={"width": width})
        return width


__all__ = ["Dimension", "VectorSchema"]
