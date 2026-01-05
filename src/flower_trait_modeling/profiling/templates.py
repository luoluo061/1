"""Narrative templates for profiles."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class NarrativeTemplates:
    """Simple narrative template renderer."""

    def render_summary(self, record: Dict[str, str | float]) -> str:
        shape = record.get("flower_shape", "?")
        color = record.get("color_primary", "?")
        diameter = record.get("flower_diameter_cm", "?")
        stem = record.get("stem_length_cm", "?")
        summary = (
            f"品种 {record.get('variety_id', '未知')} 展现 {shape} 形态，主色为 {color}，"
            f"花径约 {diameter}cm，茎长 {stem}cm，适用于多场景瓶插。"
        )
        logger.debug("Rendered summary", extra={"summary": summary})
        return summary


__all__ = ["NarrativeTemplates"]
