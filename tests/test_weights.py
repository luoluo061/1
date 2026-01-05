"""Tests for weight management."""

from flower_trait_modeling.weighting.manager import WeightManager
from flower_trait_modeling.weighting.constraints import WeightConstraints
from flower_trait_modeling.weighting.schemes import WeightScheme


def test_weight_manager_normalizes(tmp_path):
    yaml_path = tmp_path / "weights.yaml"
    yaml_path.write_text("weights:\n  a: 1\n  b: 1\n", encoding="utf-8")
    manager = WeightManager(WeightConstraints())
    scheme = manager.load(yaml_path)
    assert abs(scheme.weights["a"] - 0.5) < 1e-6


def test_apply_uses_scheme():
    manager = WeightManager(WeightConstraints())
    scheme = WeightScheme(name="inline", weights={"x": 0.2})
    scheme.normalize()
    values = {"x": 10.0}
    weighted = manager.apply(values, scheme)
    assert "x" in weighted
