"""Tests for quality policies."""

import pytest

from flower_trait_modeling.policies.quality import PolicyRule, PolicySet, DEFAULT_POLICIES
from flower_trait_modeling.utils.errors import ValidationError


def test_policy_rule_passes_within_range():
    rule = PolicyRule(name="test", description="demo", field="value", min_value=1, max_value=3)
    assert rule.evaluate({"value": 2})


def test_policy_set_collects_results():
    policy_set = PolicySet(rules=[PolicyRule(name="min", description="", field="value", min_value=1)])
    results = policy_set.evaluate_record({"value": 2})
    assert results["min"] is True


def test_default_policies_enforce_raise():
    with pytest.raises(ValidationError):
        DEFAULT_POLICIES.enforce({"vase_life_days": 2, "stem_length_cm": 20, "flower_diameter_cm": 40})
