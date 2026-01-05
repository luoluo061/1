"""Preview sample profiles for given CSV input.

This script is a convenience wrapper around the ModelingService to quickly
produce a handful of profiles for manual inspection. It is intentionally light
on dependencies to remain portable in documentation environments.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from flower_trait_modeling.app.service import ModelingService
from flower_trait_modeling.utils.logging import configure_logging


def preview(csv_path: Path, config_dir: Path, limit: int) -> None:
    service = ModelingService(
        trait_schema_path=str(config_dir / "trait_schema.yaml"),
        vector_schema_path=str(config_dir / "vector_schema.yaml"),
        weights_path=str(config_dir / "weights_default.yaml"),
        profile_rules_path=str(config_dir / "profile_rules.yaml"),
        storage_dir="preview_output",
    )
    service._setup()
    records = service.ingest(str(csv_path))[:limit]
    normalized = service.normalize_and_vectorize(records)
    profiles = service.profile(normalized)
    for item in profiles:
        profile = item["profile"]
        print(f"[{profile.variety_id}] {profile.summary}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Preview profiles from CSV")
    parser.add_argument("csv", type=Path)
    parser.add_argument("--config-dir", type=Path, default=Path("configs"))
    parser.add_argument("--limit", type=int, default=5)
    return parser


def main(argv: List[str] | None = None) -> None:
    configure_logging()
    args = build_parser().parse_args(argv)
    preview(args.csv, args.config_dir, args.limit)


if __name__ == "__main__":
    main()
