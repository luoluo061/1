"""Tests for file repository."""

from flower_trait_modeling.storage.repo_file import FileRepository
from flower_trait_modeling.domain.models import FeatureVector, Profile


def test_save_and_load_profile(tmp_path):
    repo = FileRepository(tmp_path)
    profile = Profile(variety_id="v1", sections={"identity": {"variety_id": "v1"}}, summary="demo")
    repo.save_profile(profile)
    profiles = repo.load_profiles()
    assert profiles[0].variety_id == "v1"


def test_save_vector(tmp_path):
    repo = FileRepository(tmp_path)
    vector = FeatureVector(schema_id="s", values=[0.1, 0.9], mapping=["a", "b"])
    path = repo.save_vector(vector)
    assert path.exists()
