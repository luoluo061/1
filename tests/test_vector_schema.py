"""Tests for vector schema parsing."""

from flower_trait_modeling.feature_engineering.vector_schema import VectorSchema


def test_vector_schema_total_width(tmp_path):
    yaml_path = tmp_path / "schema.yaml"
    yaml_path.write_text(
        "schema:\n  id: demo\n  dimensions:\n    - name: species\n      type: one_hot\n      vocab: [a,b]\n    - name: size\n      type: scaled_numeric\n",
        encoding="utf-8",
    )
    schema = VectorSchema.from_file(yaml_path)
    assert schema.total_width() == 3
