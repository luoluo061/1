"""Tests for vector validators."""

import pytest

from flower_trait_modeling.feature_engineering.validators import VectorValidator, DimensionExpectation, run_expectations
from flower_trait_modeling.domain.models import FeatureVector


def test_vector_validator_checks_width():
    validator = VectorValidator(expected_width=2)
    vector = FeatureVector(schema_id="s", values=[0.1, 0.2], mapping=["a", "b"])
    validator.validate(vector)


def test_dimension_expectation_enforces_bounds():
    vector = FeatureVector(schema_id="s", values=[0.5, 1.5], mapping=["x", "y"])
    expectation = DimensionExpectation(name="y", min_value=0.0, max_value=2.0)
    expectation.enforce(vector)


def test_run_expectations_handles_multiple():
    vector = FeatureVector(schema_id="s", values=[0.1, 0.2], mapping=["x", "y"])
    expectations = [DimensionExpectation(name="x"), DimensionExpectation(name="y")]
    run_expectations(vector, expectations)
