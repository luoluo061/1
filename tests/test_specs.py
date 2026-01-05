"""Tests for specification loaders."""

from pathlib import Path

from flower_trait_modeling.utils.specs import TraitSpec, VectorSpec


def test_trait_spec_parses_required(tmp_path):
    yaml_path = tmp_path / "traits.yaml"
    yaml_path.write_text(
        "traits:\n  - name: variety_id\n    type: string\n    required: true\n    description: id\n",
        encoding="utf-8",
    )
    spec = TraitSpec.from_file(yaml_path)
    assert spec.required_fields() == ["variety_id"]


def test_vector_spec_width(tmp_path):
    yaml_path = tmp_path / "vector.yaml"
    yaml_path.write_text(
        "schema:\n  id: demo\n  dimensions:\n    - name: shape\n      type: one_hot\n      vocab: [a,b,c]\n",
        encoding="utf-8",
    )
    spec = VectorSpec.from_file(yaml_path)
    assert spec.width() == 3
