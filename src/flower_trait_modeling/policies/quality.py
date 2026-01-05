"""Quality policies applied across the pipeline.

The policy layer expresses human-understandable constraints such as minimum
vase life or acceptable stem length bands. Policies are decoupled from
normalizers so they can be tuned for different market scenarios without
changing code structure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from ..utils.errors import ValidationError
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class PolicyRule:
    name: str
    description: str
    field: str
    min_value: float | None = None
    max_value: float | None = None

    def evaluate(self, record: Dict[str, object]) -> bool:
        value = record.get(self.field)
        if value is None:
            logger.debug("Policy value missing", extra={"field": self.field})
            return False
        numeric = float(value)
        if self.min_value is not None and numeric < self.min_value:
            return False
        if self.max_value is not None and numeric > self.max_value:
            return False
        return True


@dataclass
class PolicySet:
    rules: List[PolicyRule]

    def evaluate_record(self, record: Dict[str, object]) -> Dict[str, bool]:
        results: Dict[str, bool] = {}
        for rule in self.rules:
            results[rule.name] = rule.evaluate(record)
        logger.info("Policy evaluation complete", extra={"results": results})
        return results

    def enforce(self, record: Dict[str, object]) -> None:
        for rule in self.rules:
            if not rule.evaluate(record):
                raise ValidationError(rule.field, f"policy '{rule.name}' violated")


DEFAULT_POLICIES = PolicySet(
    rules=[
        PolicyRule(name="vase_life_minimum", description="Ensure vase life >= 5 days", field="vase_life_days", min_value=5),
        PolicyRule(name="stem_length_minimum", description="Ensure stems are practical for bouquets", field="stem_length_cm", min_value=30),
        PolicyRule(name="diameter_reasonable", description="Filter out abnormally large blooms", field="flower_diameter_cm", max_value=30),
    ]
)


__all__ = ["PolicyRule", "PolicySet", "DEFAULT_POLICIES"]
