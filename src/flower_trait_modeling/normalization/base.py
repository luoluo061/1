"""Base normalization interfaces."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from ..utils.errors import NormalizationError
from ..utils.logging import get_logger

logger = get_logger(__name__)


class Normalizer(ABC):
    """Abstract normalizer contract."""

    field: str

    def __init__(self, field: str) -> None:
        self.field = field

    @abstractmethod
    def normalize(self, value: Any) -> Any:
        """Normalize incoming value and return normalized representation."""

    def __call__(self, value: Any) -> Any:
        try:
            normalized = self.normalize(value)
            logger.debug("Normalized value", extra={"field": self.field, "value": value, "normalized": normalized})
            return normalized
        except Exception as exc:  # pragma: no cover - defensive
            raise NormalizationError(self.field, value) from exc


__all__ = ["Normalizer"]
