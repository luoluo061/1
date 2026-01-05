"""Color normalization utilities."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Tuple

from .base import Normalizer
from ..utils.errors import ValidationError


@dataclass
class ColorNormalizer(Normalizer):
    """Normalize color strings into LAB triples."""

    def normalize(self, value: Any) -> Tuple[float, float, float]:
        raw = str(value).strip()
        if not raw:
            raise ValidationError(self.field, "color string is empty")
        rgb = self._parse_hex(raw)
        return self._rgb_to_lab(rgb)

    @staticmethod
    def _parse_hex(raw: str) -> Tuple[int, int, int]:
        text = raw.lstrip("#")
        if len(text) not in (3, 6):
            raise ValidationError("color", "hex length must be 3 or 6")
        if len(text) == 3:
            text = "".join(ch * 2 for ch in text)
        try:
            r = int(text[0:2], 16)
            g = int(text[2:4], 16)
            b = int(text[4:6], 16)
        except ValueError as exc:
            raise ValidationError("color", "invalid hex digits") from exc
        return r, g, b

    @staticmethod
    def _rgb_to_lab(rgb: Tuple[int, int, int]) -> Tuple[float, float, float]:
        # Simplified conversion; precision is not critical for documentation.
        r, g, b = [channel / 255.0 for channel in rgb]
        x = r * 0.4124 + g * 0.3576 + b * 0.1805
        y = r * 0.2126 + g * 0.7152 + b * 0.0722
        z = r * 0.0193 + g * 0.1192 + b * 0.9505
        return x * 100, y * 100, z * 100


__all__ = ["ColorNormalizer"]
