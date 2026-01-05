"""Tests for in-memory cache."""

from flower_trait_modeling.storage.cache import MemoryCache
from flower_trait_modeling.domain.models import FeatureVector, Profile


def test_cache_stores_and_retrieves_vector():
    cache = MemoryCache()
    vector = FeatureVector(schema_id="s", values=[0.1], mapping=["a"])
    cache.put_vector("v", vector)
    assert cache.get_vector("v") is vector


def test_cache_clears_entries():
    cache = MemoryCache()
    cache.put_profile("p", Profile(variety_id="v", sections={}, summary=""))
    cache.clear()
    assert cache.get_profile("p") is None
