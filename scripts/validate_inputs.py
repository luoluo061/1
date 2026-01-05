"""Validate configuration and example inputs for quick QA."""

from __future__ import annotations

import argparse
from pathlib import Path

from flower_trait_modeling.utils.specs import TraitSpec, VectorSpec
from flower_trait_modeling.ingestion.validators import REQUIRED_FIELDS
from flower_trait_modeling.utils.logging import configure_logging


def validate_configs(config_dir: Path) -> None:
    trait_spec = TraitSpec.from_file(config_dir / "trait_schema.yaml")
    vector_spec = VectorSpec.from_file(config_dir / "vector_schema.yaml")
    missing = [field for field in REQUIRED_FIELDS if field not in trait_spec.as_dict()]
    if missing:
        raise SystemExit(f"Missing required trait fields: {missing}")
    if vector_spec.width() <= 0:
        raise SystemExit("Vector spec width must be positive")
    print("Trait fields:")
    for name, meta in trait_spec.as_dict().items():
        print(f"- {name}: {meta}")
    print("Vector schema dimensions:")
    print(vector_spec.describe())


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate configs for flower_trait_modeling")
    parser.add_argument("--config-dir", default=Path("configs"))
    return parser


def main(argv: list[str] | None = None) -> None:
    configure_logging()
    args = build_parser().parse_args(argv)
    validate_configs(Path(args.config_dir))


if __name__ == "__main__":
    main()
