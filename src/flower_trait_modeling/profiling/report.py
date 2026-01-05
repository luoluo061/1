"""Reporting helpers for profile outputs."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List

from ..domain.models import Profile
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ProfileReport:
    profiles: List[Profile] = field(default_factory=list)

    def add(self, profile: Profile) -> None:
        self.profiles.append(profile)

    def to_table(self) -> List[Dict[str, str]]:
        return [
            {
                "variety_id": profile.variety_id,
                "sections": ",".join(profile.sections.keys()),
                "summary_len": str(len(profile.summary)),
            }
            for profile in self.profiles
        ]

    def log(self) -> None:
        logger.info("Profile report", extra={"count": len(self.profiles)})


__all__ = ["ProfileReport"]
