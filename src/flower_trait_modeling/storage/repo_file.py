"""File-based repository for storing vectors and profiles."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List

from ..domain.models import FeatureVector, Profile
from ..utils.io import ensure_dir
from ..utils.logging import get_logger

logger = get_logger(__name__)


class FileRepository:
    base_dir: Path

    def __init__(self, base_dir: str | Path) -> None:
        self.base_dir = ensure_dir(base_dir)

    def save_vector(self, vector: FeatureVector) -> Path:
        path = self.base_dir / f"vector_{vector.schema_id}.json"
        payload = {"schema_id": vector.schema_id, "values": vector.values, "mapping": vector.mapping}
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("Saved vector", extra={"path": str(path)})
        return path

    def save_profile(self, profile: Profile) -> Path:
        path = self.base_dir / f"profile_{profile.variety_id}.json"
        payload: Dict[str, object] = {
            "variety_id": profile.variety_id,
            "sections": profile.sections,
            "summary": profile.summary,
        }
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("Saved profile", extra={"path": str(path)})
        return path

    def load_profiles(self) -> List[Profile]:
        profiles: List[Profile] = []
        for file in self.base_dir.glob("profile_*.json"):
            data = json.loads(file.read_text(encoding="utf-8"))
            profiles.append(Profile(variety_id=data["variety_id"], sections=data["sections"], summary=data["summary"]))
        logger.debug("Loaded profiles", extra={"count": len(profiles)})
        return profiles


__all__ = ["FileRepository"]
