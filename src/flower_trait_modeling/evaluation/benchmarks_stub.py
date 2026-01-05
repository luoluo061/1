"""Benchmark stubs describing how to measure system performance."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Dict, List

from ..similarity.engine import SimilarityEngine
from ..domain.models import FeatureVector
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class BenchmarkCase:
    name: str
    query: FeatureVector
    candidates: List[FeatureVector]
    expected_order: List[str]


@dataclass
class BenchmarkSuite:
    """Collection of benchmark cases."""

    engine_factory: Callable[[], SimilarityEngine]
    cases: List[BenchmarkCase]

    def run(self) -> Dict[str, float]:
        results: Dict[str, float] = {}
        engine = self.engine_factory()
        for case in self.cases:
            retrieved = engine.compare(case.query, case.candidates[0])
            results[case.name] = retrieved.score
            logger.info("Benchmark executed", extra={"case": case.name, "score": retrieved.score})
        return results


__all__ = ["BenchmarkCase", "BenchmarkSuite"]
