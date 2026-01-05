"""Data dictionaries for trait definitions and narrative labels.

This module centralizes vocabulary used across the system so that tests and
documentation can consume the same canonical mapping. Each dictionary is
annotated with descriptions to help auditors review whether traits cover
expected business dimensions such as花型、花径、颜色、茎长和瓶插期。
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List

from .logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class TraitDictionaryEntry:
    name: str
    description: str
    examples: List[str]


TRAIT_DICTIONARY: Dict[str, TraitDictionaryEntry] = {
    "species": TraitDictionaryEntry(
        name="species",
        description="Botanical category such as rose or lily",
        examples=["rose", "lily", "tulip", "carnation", "chrysanthemum"],
    ),
    "flower_shape": TraitDictionaryEntry(
        name="flower_shape",
        description="High-level petal geometry classification",
        examples=["single", "double", "pompon", "star", "trumpet"],
    ),
    "flower_diameter_cm": TraitDictionaryEntry(
        name="flower_diameter_cm",
        description="Measured bloom diameter in centimeters",
        examples=["6", "8", "12", "15"],
    ),
    "color_primary": TraitDictionaryEntry(
        name="color_primary",
        description="Primary visible color expressed as hex",
        examples=["#ff6677", "#ffee00", "#ffffff"],
    ),
    "stem_length_cm": TraitDictionaryEntry(
        name="stem_length_cm",
        description="Usable stem length for vase arrangements",
        examples=["40", "60", "80"],
    ),
    "vase_life_days": TraitDictionaryEntry(
        name="vase_life_days",
        description="Expected vase life under baseline conditions",
        examples=["7", "12", "15"],
    ),
    "fragrance": TraitDictionaryEntry(
        name="fragrance",
        description="Subjective fragrance intensity rating",
        examples=["none", "light", "medium", "strong"],
    ),
    "seasonality": TraitDictionaryEntry(
        name="seasonality",
        description="Typical season when the variety is harvested",
        examples=["spring", "summer", "autumn", "winter", "all"],
    ),
}


def describe_traits() -> str:
    """Render a markdown bullet list of trait definitions."""

    lines: List[str] = []
    for entry in TRAIT_DICTIONARY.values():
        examples = ", ".join(entry.examples)
        lines.append(f"- **{entry.name}**: {entry.description}. 示例: {examples}.")
    description = "\n".join(lines)
    logger.debug("Trait descriptions built", extra={"count": len(lines)})
    return description


def ensure_trait(name: str) -> TraitDictionaryEntry:
    """Fetch a trait entry or raise a KeyError with helpful message."""

    if name not in TRAIT_DICTIONARY:
        raise KeyError(f"Trait {name} not defined in dictionary")
    return TRAIT_DICTIONARY[name]


def list_trait_names() -> List[str]:
    """Return trait names in deterministic order."""

    return sorted(TRAIT_DICTIONARY.keys())


def build_vocab_map() -> Dict[str, List[str]]:
    """Return a mapping from trait to example vocabulary."""

    vocab_map = {name: entry.examples for name, entry in TRAIT_DICTIONARY.items()}
    logger.debug("Vocabulary map built", extra={"traits": list(vocab_map.keys())})
    return vocab_map


def render_markdown_table() -> str:
    """Render a markdown table enumerating traits and examples."""

    lines = ["| Trait | Description | Examples |", "| --- | --- | --- |"]
    for entry in TRAIT_DICTIONARY.values():
        lines.append(f"| {entry.name} | {entry.description} | {', '.join(entry.examples)} |")
    table = "\n".join(lines)
    logger.debug("Rendered trait table", extra={"lines": len(lines)})
    return table


__all__ = ["TRAIT_DICTIONARY", "TraitDictionaryEntry", "describe_traits", "ensure_trait"]
