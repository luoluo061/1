"""Enum definitions for flower trait modeling domain."""

from __future__ import annotations

from enum import Enum


class FlowerShape(str, Enum):
    SINGLE = "single"
    DOUBLE = "double"
    POMPON = "pompon"
    STAR = "star"
    TRUMPET = "trumpet"


class Fragrance(str, Enum):
    NONE = "none"
    LIGHT = "light"
    MEDIUM = "medium"
    STRONG = "strong"


class Seasonality(str, Enum):
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"
    ALL = "all"


__all__ = ["FlowerShape", "Fragrance", "Seasonality"]
