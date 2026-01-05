"""I/O helpers for reading and writing lightweight artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict
import yaml

from .errors import ConfigurationError, StorageError
from .logging import get_logger

logger = get_logger(__name__)


def read_yaml(path: str | Path) -> Dict[str, Any]:
    """Load a YAML file with error handling."""

    target = Path(path)
    if not target.exists():
        raise ConfigurationError(f"Missing configuration {target}")
    try:
        content = yaml.safe_load(target.read_text(encoding="utf-8"))
        logger.debug("Loaded YAML", extra={"path": str(target)})
        return content or {}
    except yaml.YAMLError as exc:
        raise ConfigurationError("Invalid YAML", {"path": str(target)}) from exc


def write_json(path: str | Path, payload: Dict[str, Any]) -> None:
    """Write a JSON payload to disk."""

    target = Path(path)
    try:
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info("Wrote JSON", extra={"path": str(target)})
    except OSError as exc:
        raise StorageError(str(target), str(exc)) from exc


def ensure_dir(path: str | Path) -> Path:
    """Ensure a directory exists and return the resolved path."""

    target = Path(path)
    target.mkdir(parents=True, exist_ok=True)
    logger.debug("Ensured directory", extra={"path": str(target)})
    return target


__all__ = ["read_yaml", "write_json", "ensure_dir"]
