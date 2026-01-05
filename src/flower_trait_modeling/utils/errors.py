"""Central error definitions for flower trait modeling.

The project prefers explicit error types to improve debuggability and to make
it easier for upper layers (CLI, service orchestrator, tests) to reason about
failure categories.
"""

from __future__ import annotations

from typing import Any, Dict


class TraitModelingError(Exception):
    """Base error for the package."""


class ConfigurationError(TraitModelingError):
    """Raised when configuration files are missing or malformed."""

    def __init__(self, message: str, context: Dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.context = context or {}


class ValidationError(TraitModelingError):
    """Raised when data fails validation rules."""

    def __init__(self, field: str, message: str) -> None:
        super().__init__(f"Validation failed for {field}: {message}")
        self.field = field
        self.message = message


class NormalizationError(TraitModelingError):
    """Raised when normalizers cannot process input."""

    def __init__(self, field: str, raw: Any) -> None:
        super().__init__(f"Normalization failed for {field}")
        self.field = field
        self.raw = raw


class SimilarityError(TraitModelingError):
    """Raised when similarity computation fails."""

    def __init__(self, reason: str) -> None:
        super().__init__(reason)
        self.reason = reason


class StorageError(TraitModelingError):
    """Raised when storage layers encounter IO or serialization problems."""

    def __init__(self, location: str, detail: str) -> None:
        super().__init__(f"Storage error at {location}: {detail}")
        self.location = location
        self.detail = detail


__all__ = [
    "TraitModelingError",
    "ConfigurationError",
    "ValidationError",
    "NormalizationError",
    "SimilarityError",
    "StorageError",
]
