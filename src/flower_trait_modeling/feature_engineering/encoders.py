"""Encoders for transforming normalized traits into numeric representations."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..utils.logging import get_logger

logger = get_logger(__name__)


def one_hot(value: str, vocab: List[str]) -> List[float]:
    vector = [1.0 if term == value else 0.0 for term in vocab]
    logger.debug("One-hot encoded", extra={"value": value, "vector": vector})
    return vector


def ordinal(value: float, size: int) -> List[float]:
    vector = [1.0 if idx == int(value) else 0.0 for idx in range(size)]
    logger.debug("Ordinal encoded", extra={"value": value, "vector": vector})
    return vector


def passthrough(value: float) -> List[float]:
    return [float(value)]


def lab_to_vector(lab: tuple[float, float, float]) -> List[float]:
    return [float(component) for component in lab]


@dataclass
class EncoderContext:
    """Context for encoder execution."""

    schema_name: str
    debug: bool = False

    def log(self, message: str, payload: dict) -> None:
        if self.debug:
            logger.info(message, extra=payload)


__all__ = ["one_hot", "ordinal", "passthrough", "lab_to_vector", "EncoderContext"]
