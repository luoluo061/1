"""Tests for vector scaler."""

from flower_trait_modeling.feature_engineering.scaler import VectorScaler


def test_unit_scaler_normalizes_length():
    scaler = VectorScaler("unit")
    scaled = scaler.scale([3.0, 4.0])
    assert round(sum(v * v for v in scaled), 5) == 1.0


def test_max_abs_scaler_handles_zero():
    scaler = VectorScaler("max_abs")
    scaled = scaler.scale([0.0, 0.0, 1.0])
    assert max(scaled) == 1.0
