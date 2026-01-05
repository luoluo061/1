"""Tests for vector builder."""

from flower_trait_modeling.feature_engineering.vector_schema import VectorSchema
from flower_trait_modeling.feature_engineering.vector_builder import VectorBuilder


def test_vector_builder_encodes_fields(tmp_path):
    yaml_path = tmp_path / "schema.yaml"
    yaml_path.write_text(
        "schema:\n  id: demo\n  dimensions:\n    - name: shape\n      type: one_hot\n      vocab: [single,double]\n    - name: length\n      type: scaled_numeric\n",
        encoding="utf-8",
    )
    schema = VectorSchema.from_file(yaml_path)
    builder = VectorBuilder(schema)
    payload = {"shape": "single", "length": 10.0}
    vector = builder.build(payload)
    assert vector.mapping.count("shape") == 2
