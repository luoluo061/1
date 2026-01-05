"""Synthetic data generation utilities for demos and tests."""

from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Dict, Iterable, List

from ..domain.enums import FlowerShape, Fragrance, Seasonality
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class SyntheticConfig:
    species_pool: List[str]
    color_pool: List[str]
    shape_pool: List[FlowerShape]
    fragrance_pool: List[Fragrance]
    season_pool: List[Seasonality]
    diameter_range: tuple[int, int] = (5, 15)
    stem_range: tuple[int, int] = (30, 80)
    vase_range: tuple[int, int] = (5, 15)


DEFAULT_CONFIG = SyntheticConfig(
    species_pool=["rose", "lily", "tulip", "carnation", "chrysanthemum"],
    color_pool=["#ff6677", "#ffee00", "#ffffff", "#d02050"],
    shape_pool=[
        FlowerShape.SINGLE,
        FlowerShape.DOUBLE,
        FlowerShape.POMPON,
        FlowerShape.STAR,
        FlowerShape.TRUMPET,
    ],
    fragrance_pool=[Fragrance.NONE, Fragrance.LIGHT, Fragrance.MEDIUM, Fragrance.STRONG],
    season_pool=[Seasonality.SPRING, Seasonality.SUMMER, Seasonality.AUTUMN, Seasonality.WINTER],
)


def random_trait(pool: Iterable) -> object:
    return random.choice(list(pool))


def generate_record(seed: int, config: SyntheticConfig = DEFAULT_CONFIG) -> Dict[str, object]:
    random.seed(seed)
    record = {
        "variety_id": f"synth_{seed:04d}",
        "species": random_trait(config.species_pool),
        "flower_shape": random_trait(config.shape_pool).value,
        "flower_diameter_cm": random.randint(*config.diameter_range),
        "color_primary": random_trait(config.color_pool),
        "stem_length_cm": random.randint(*config.stem_range),
        "vase_life_days": random.randint(*config.vase_range),
        "fragrance": random_trait(config.fragrance_pool).value,
        "seasonality": random_trait(config.season_pool).value,
    }
    logger.debug("Generated synthetic record", extra={"record": record})
    return record


def generate_batch(count: int, start_seed: int = 1, config: SyntheticConfig = DEFAULT_CONFIG) -> List[Dict[str, object]]:
    records = [generate_record(start_seed + i, config) for i in range(count)]
    logger.info("Generated batch", extra={"count": len(records)})
    return records


def perturb_record(record: Dict[str, object], noise: float = 0.1) -> Dict[str, object]:
    perturbed = dict(record)
    perturbed["flower_diameter_cm"] = round(float(record.get("flower_diameter_cm", 0)) * (1 + noise), 2)
    perturbed["stem_length_cm"] = round(float(record.get("stem_length_cm", 0)) * (1 + noise), 2)
    perturbed["vase_life_days"] = round(float(record.get("vase_life_days", 0)) * (1 + noise), 2)
    logger.debug("Perturbed record", extra={"original": record, "perturbed": perturbed})
    return perturbed


def summarize_batch(records: List[Dict[str, object]]) -> Dict[str, float]:
    """Summarize numeric columns in synthetic records."""

    if not records:
        return {"flower_diameter_cm": 0.0, "stem_length_cm": 0.0, "vase_life_days": 0.0}
    diameter_avg = sum(float(r.get("flower_diameter_cm", 0)) for r in records) / len(records)
    stem_avg = sum(float(r.get("stem_length_cm", 0)) for r in records) / len(records)
    vase_avg = sum(float(r.get("vase_life_days", 0)) for r in records) / len(records)
    summary = {"flower_diameter_cm": diameter_avg, "stem_length_cm": stem_avg, "vase_life_days": vase_avg}
    logger.info("Summarized synthetic batch", extra=summary)
    return summary


__all__ = ["SyntheticConfig", "DEFAULT_CONFIG", "generate_record", "generate_batch", "perturb_record", "summarize_batch"]
