"""Rule-based profile extraction."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from ..utils.io import read_yaml
from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class ProfileRules:
    sections: List[Dict[str, object]]

    @classmethod
    def from_file(cls, path: str) -> "ProfileRules":
        data = read_yaml(path)
        sections = data.get("sections", [])
        return cls(sections=sections)

    def extract_sections(self, record: Dict[str, str | float]) -> Dict[str, Dict[str, str | float]]:
        result: Dict[str, Dict[str, str | float]] = {}
        for section in self.sections:
            name = section.get("name", "unknown")
            fields = section.get("fields", [])
            result[name] = {field: record.get(field, "") for field in fields}
            logger.debug("Extracted section", extra={"section": name})
        return result


__all__ = ["ProfileRules"]
