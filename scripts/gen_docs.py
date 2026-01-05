"""Generate Markdown documentation from configuration files.

The script reads configuration YAML files and produces minimal Markdown
summaries that can be referenced when撰写软著材料。
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any, Dict

import yaml

OUTPUT_FILES = {
    "trait_schema": "docs/generated_trait_schema.md",
    "vector_schema": "docs/generated_vector_schema.md",
    "weights": "docs/generated_weights.md",
    "similarity": "docs/generated_similarity.md",
    "profile_rules": "docs/generated_profile_rules.md",
}


def load_yaml(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def render_table(title: str, rows: Dict[str, Any]) -> str:
    lines = [f"# {title}", "", "| Key | Value |", "| --- | --- |"]
    for key, value in rows.items():
        lines.append(f"| {key} | {value} |")
    return "\n".join(lines)


def write_output(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def generate_docs(config_dir: Path) -> None:
    trait = load_yaml(config_dir / "trait_schema.yaml")
    vector = load_yaml(config_dir / "vector_schema.yaml")
    weights = load_yaml(config_dir / "weights_default.yaml")
    similarity = load_yaml(config_dir / "similarity.yaml")
    profile_rules = load_yaml(config_dir / "profile_rules.yaml")

    write_output(Path(OUTPUT_FILES["trait_schema"]), render_table("Trait Schema", {t.get("name"): t.get("type") for t in trait.get("traits", [])}))
    write_output(Path(OUTPUT_FILES["vector_schema"]), render_table("Vector Schema", {d.get("name"): d.get("type") for d in vector.get("schema", {}).get("dimensions", [])}))
    write_output(Path(OUTPUT_FILES["weights"]), render_table("Default Weights", weights.get("weights", {})))
    write_output(Path(OUTPUT_FILES["similarity"]), render_table("Similarity", similarity.get("metrics", {})))
    write_output(Path(OUTPUT_FILES["profile_rules"]), render_table("Profile Sections", {sec.get("name"): ",".join(sec.get("fields", [])) for sec in profile_rules.get("sections", [])}))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate documentation from configuration")
    parser.add_argument("--config-dir", default="configs", help="Directory containing YAML configs")
    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    generate_docs(Path(args.config_dir))


if __name__ == "__main__":
    main()
