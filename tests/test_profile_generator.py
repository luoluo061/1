"""Tests for profile generation."""

from flower_trait_modeling.profiling.generator import ProfileGenerator
from flower_trait_modeling.profiling.rules import ProfileRules
from flower_trait_modeling.profiling.templates import NarrativeTemplates


def test_profile_generator_builds_sections(tmp_path):
    yaml_path = tmp_path / "rules.yaml"
    yaml_path.write_text("sections:\n  - name: identity\n    fields: [variety_id, species]\n", encoding="utf-8")
    generator = ProfileGenerator(ProfileRules.from_file(yaml_path), NarrativeTemplates())
    profile = generator.generate({"variety_id": "v1", "species": "rose"}, None)
    assert "identity" in profile.sections
    assert profile.summary
