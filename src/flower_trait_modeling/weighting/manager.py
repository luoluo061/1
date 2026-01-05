"""Weight management utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from .schemes import WeightScheme, WeightConstraint
from ..utils.io import read_yaml
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class WeightManager:
    """Load and validate weights from configuration files."""

    constraint: WeightConstraint

    def load(self, path: str) -> WeightScheme:
        data = read_yaml(path)
        weights = data.get("weights", {})
        scheme = WeightScheme(name=data.get("name", "default"), weights=weights)
        self.constraint.validate(weights)
        scheme.normalize()
        logger.info("Loaded weight scheme", extra={"name": scheme.name, "count": len(weights)})
        return scheme

    def apply(self, values: Dict[str, float], scheme: WeightScheme) -> Dict[str, float]:
        weighted = {key: values.get(key, 0.0) * scheme.weights.get(key, 1.0) for key in values}
        logger.debug("Applied weight scheme", extra={"keys": list(weighted.keys())})
        return weighted


__all__ = ["WeightManager"]
