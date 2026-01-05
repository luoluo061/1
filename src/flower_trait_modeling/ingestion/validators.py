"""Validation helpers for incoming flower trait data."""

from __future__ import annotations

from typing import Dict, List

from ..utils.errors import ValidationError
from ..utils.logging import get_logger

logger = get_logger(__name__)

REQUIRED_FIELDS = [
    "variety_id",
    "species",
    "flower_shape",
    "flower_diameter_cm",
    "color_primary",
    "stem_length_cm",
    "vase_life_days",
]


def validate_record(record: Dict[str, str]) -> None:
    """Validate a raw dictionary record."""

    for field in REQUIRED_FIELDS:
        if field not in record:
            raise ValidationError(field, "missing required field")
        if str(record[field]).strip() == "":
            raise ValidationError(field, "value is empty")
    try:
        diameter = float(record["flower_diameter_cm"])
        stem = float(record["stem_length_cm"])
        vase = float(record["vase_life_days"])
    except ValueError as exc:
        raise ValidationError("numeric", "cannot parse numeric fields") from exc
    if diameter <= 0 or stem <= 0 or vase <= 0:
        raise ValidationError("numeric", "values must be positive")
    logger.debug("Record validated", extra={"variety_id": record.get("variety_id")})


def batch_validate(records: List[Dict[str, str]]) -> List[str]:
    """Validate multiple records and return IDs of valid entries."""

    valid_ids: List[str] = []
    for record in records:
        try:
            validate_record(record)
            valid_ids.append(str(record.get("variety_id")))
        except ValidationError as exc:
            logger.warning("Record failed validation", extra={"error": str(exc)})
    return valid_ids


__all__ = ["validate_record", "batch_validate", "REQUIRED_FIELDS"]
