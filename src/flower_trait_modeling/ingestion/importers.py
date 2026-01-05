"""Importers responsible for reading raw data sources."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable, List

from ..domain.models import FlowerVariety
from ..domain.enums import FlowerShape, Fragrance, Seasonality
from ..utils.errors import ValidationError
from ..utils.logging import get_logger

logger = get_logger(__name__)


def read_csv(path: str | Path) -> List[FlowerVariety]:
    """Read varieties from a CSV file.

    The importer is deliberately strict: missing required columns cause
    :class:`ValidationError` to surface immediately to keep datasets clean.
    """

    target = Path(path)
    if not target.exists():
        raise ValidationError("file", f"{target} does not exist")

    varieties: List[FlowerVariety] = []
    with target.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            variety = FlowerVariety(
                variety_id=row.get("variety_id", "").strip(),
                species=row.get("species", "unknown").strip(),
                flower_shape=FlowerShape(row.get("flower_shape", FlowerShape.SINGLE)),
                flower_diameter_cm=float(row.get("flower_diameter_cm", 0)),
                color_primary=row.get("color_primary", "#000000"),
                stem_length_cm=float(row.get("stem_length_cm", 0)),
                vase_life_days=float(row.get("vase_life_days", 0)),
                fragrance=Fragrance(row.get("fragrance", Fragrance.NONE)),
                seasonality=Seasonality(row.get("seasonality", Seasonality.ALL)),
            )
            variety.validate()
            varieties.append(variety)
            logger.debug("Imported variety", extra=variety.to_record())
    return varieties


def import_iterable(records: Iterable[dict]) -> List[FlowerVariety]:
    """Import from an iterable of dictionaries."""

    varieties: List[FlowerVariety] = []
    for record in records:
        try:
            variety = FlowerVariety(
                variety_id=str(record.get("variety_id", "")),
                species=str(record.get("species", "unknown")),
                flower_shape=FlowerShape(record.get("flower_shape", FlowerShape.SINGLE)),
                flower_diameter_cm=float(record.get("flower_diameter_cm", 0)),
                color_primary=str(record.get("color_primary", "#000")),
                stem_length_cm=float(record.get("stem_length_cm", 0)),
                vase_life_days=float(record.get("vase_life_days", 0)),
                fragrance=Fragrance(record.get("fragrance", Fragrance.NONE)),
                seasonality=Seasonality(record.get("seasonality", Seasonality.ALL)),
            )
            variety.validate()
            varieties.append(variety)
        except ValidationError as exc:
            logger.warning("Skipping invalid record", extra={"error": str(exc), "record": record})
    return varieties


__all__ = ["read_csv", "import_iterable"]
