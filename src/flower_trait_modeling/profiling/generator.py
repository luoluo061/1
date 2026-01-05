"""Profile generator for flower varieties."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict

from ..domain.models import FeatureVector, Profile
from .rules import ProfileRules
from .templates import NarrativeTemplates
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ProfileGenerator:
    rules: ProfileRules
    templates: NarrativeTemplates

    def generate(self, record: Dict[str, str | float], vector: FeatureVector | None = None) -> Profile:
        sections = self.rules.extract_sections(record)
        summary = self.templates.render_summary(record)
        profile = Profile(variety_id=str(record.get("variety_id", "unknown")), sections=sections, summary=summary, vector_snapshot=vector)
        logger.info("Generated profile", extra={"variety_id": profile.variety_id})
        return profile


__all__ = ["ProfileGenerator"]
