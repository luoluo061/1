"""Command-line interface for the flower trait modeling system."""

from __future__ import annotations

import argparse
from typing import List

from .app.service import ModelingService
from .utils.logging import configure_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="鲜花品种性状参数建模系统 CLI")
    parser.add_argument("csv", help="Path to input CSV file")
    parser.add_argument("--config-dir", default="configs", help="Configuration directory")
    parser.add_argument("--storage", default="output", help="Storage directory for artifacts")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logs")
    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging()
    service = ModelingService(
        trait_schema_path=f"{args.config_dir}/trait_schema.yaml",
        vector_schema_path=f"{args.config_dir}/vector_schema.yaml",
        weights_path=f"{args.config_dir}/weights_default.yaml",
        profile_rules_path=f"{args.config_dir}/profile_rules.yaml",
        storage_dir=args.storage,
    )
    service._setup()
    records = service.ingest(args.csv)
    normalized = service.normalize_and_vectorize(records)
    service.profile(normalized)


if __name__ == "__main__":  # pragma: no cover
    main()
