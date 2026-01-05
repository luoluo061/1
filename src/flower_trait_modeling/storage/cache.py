"""In-memory cache abstraction for transient artifacts."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Optional

from ..domain.models import FeatureVector, Profile
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class MemoryCache:
    vectors: Dict[str, FeatureVector] = field(default_factory=dict)
    profiles: Dict[str, Profile] = field(default_factory=dict)

    def put_vector(self, key: str, vector: FeatureVector) -> None:
        self.vectors[key] = vector
        logger.debug("Cached vector", extra={"key": key})

    def get_vector(self, key: str) -> Optional[FeatureVector]:
        return self.vectors.get(key)

    def put_profile(self, key: str, profile: Profile) -> None:
        self.profiles[key] = profile
        logger.debug("Cached profile", extra={"key": key})

    def get_profile(self, key: str) -> Optional[Profile]:
        return self.profiles.get(key)

    def clear(self) -> None:
        self.vectors.clear()
        self.profiles.clear()
        logger.info("Cache cleared")


__all__ = ["MemoryCache"]
