"""Tests for pre-flight checks."""

from flower_trait_modeling.utils.specs import TraitSpec, VectorSpec
from flower_trait_modeling.utils.checks import check_trait_coverage, check_vector_alignment, check_weight_bounds


def build_specs(tmp_path):
    trait_path = tmp_path / "traits.yaml"
    trait_path.write_text(
        "traits:\n  - name: variety_id\n    type: string\n    required: true\n  - name: species\n    type: string\n    required: true\n  - name: flower_shape\n    type: categorical\n    required: true\n",
        encoding="utf-8",
    )
    vector_path = tmp_path / "vector.yaml"
    vector_path.write_text(
        "schema:\n  id: demo\n  dimensions:\n    - name: variety_id\n      type: scaled_numeric\n    - name: species\n      type: one_hot\n      vocab: [a]\n    - name: flower_shape\n      type: one_hot\n      vocab: [single]\n",
        encoding="utf-8",
    )
    return TraitSpec.from_file(trait_path), VectorSpec.from_file(vector_path)


def test_trait_coverage(tmp_path):
    trait_spec, _ = build_specs(tmp_path)
    result = check_trait_coverage(trait_spec, ["variety_id", "species", "flower_shape"])
    assert result.passed


def test_vector_alignment(tmp_path):
    trait_spec, vector_spec = build_specs(tmp_path)
    result = check_vector_alignment(trait_spec, vector_spec)
    assert result.passed


def test_weight_bounds():
    result = check_weight_bounds({"a": 0.5, "b": 1.1}, 0.0, 1.0)
    assert not result.passed
