"""Tests for normalization pipeline."""

from flower_trait_modeling.normalization.numeric import MinMaxNormalizer
from flower_trait_modeling.normalization.categorical import CategoricalNormalizer, OrdinalNormalizer
from flower_trait_modeling.normalization.pipeline import NormalizationPipeline


def test_minmax_normalizer():
    norm = MinMaxNormalizer("flower_diameter_cm", 0, 20)
    assert norm.normalize(10) == 0.5


def test_categorical_normalizer_maps_allowed():
    norm = CategoricalNormalizer("flower_shape", ["single", "double"], mapping={"Single": "single"})
    assert norm.normalize("Single") == "single"


def test_ordinal_normalizer_returns_rank():
    norm = OrdinalNormalizer("fragrance", ["none", "light", "medium", "strong"])
    assert norm.normalize("medium") == 2.0


def test_pipeline_runs_default():
    payload = {
        "flower_diameter_cm": 10,
        "stem_length_cm": 50,
        "vase_life_days": 10,
        "flower_shape": "single",
        "fragrance": "light",
        "color_primary": "#ffffff",
    }
    pipeline = NormalizationPipeline.default()
    normalized = pipeline.run(payload)
    assert "flower_diameter_cm" in normalized
