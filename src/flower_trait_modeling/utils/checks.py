"""Pre-flight checks for configuration completeness and dataset sanity."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .specs import TraitSpec, VectorSpec
from .logging import get_logger

logger = get_logger(__name__)


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


def check_trait_coverage(trait_spec: TraitSpec, required_fields: List[str]) -> CheckResult:
    missing = [field for field in required_fields if field not in trait_spec.as_dict()]
    passed = len(missing) == 0
    detail = "All required traits present" if passed else f"Missing: {missing}"
    logger.info("Trait coverage check", extra={"passed": passed, "missing": missing})
    return CheckResult(name="trait_coverage", passed=passed, detail=detail)


def check_vector_alignment(trait_spec: TraitSpec, vector_spec: VectorSpec) -> CheckResult:
    trait_names = {field.name for field in trait_spec.fields}
    vector_names = {dim.name for dim in vector_spec.dimensions}
    missing = trait_names - vector_names
    extra = vector_names - trait_names
    passed = not missing
    detail = "Aligned" if passed else f"Vector missing: {missing}; Extra: {extra}"
    logger.info("Vector alignment check", extra={"passed": passed})
    return CheckResult(name="vector_alignment", passed=passed, detail=detail)


def check_weight_bounds(weights: Dict[str, float], min_weight: float, max_weight: float) -> CheckResult:
    violations = {k: v for k, v in weights.items() if v < min_weight or v > max_weight}
    passed = len(violations) == 0
    detail = "Weights within bounds" if passed else f"Violations: {violations}"
    logger.info("Weight bounds check", extra={"passed": passed})
    return CheckResult(name="weight_bounds", passed=passed, detail=detail)


def run_all_checks(trait_spec: TraitSpec, vector_spec: VectorSpec, weights: Dict[str, float]) -> List[CheckResult]:
    results = [
        check_trait_coverage(trait_spec, ["variety_id", "species", "flower_shape", "flower_diameter_cm", "color_primary", "stem_length_cm", "vase_life_days"]),
        check_vector_alignment(trait_spec, vector_spec),
        check_weight_bounds(weights, 0.0, 1.0),
    ]
    logger.info("Completed pre-flight checks", extra={"results": [r.detail for r in results]})
    return results


__all__ = ["CheckResult", "check_trait_coverage", "check_vector_alignment", "check_weight_bounds", "run_all_checks"]
