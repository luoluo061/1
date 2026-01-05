"""Tests for synthetic data generator."""

from flower_trait_modeling.ingestion.synthetic import (
    generate_record,
    generate_batch,
    perturb_record,
    summarize_batch,
    DEFAULT_CONFIG,
)


def test_generate_record_fields_present():
    record = generate_record(1)
    assert set(record.keys()) >= {"variety_id", "species", "flower_shape"}


def test_generate_batch_respects_count():
    records = generate_batch(3)
    assert len(records) == 3


def test_perturb_record_changes_numeric():
    record = generate_record(2, DEFAULT_CONFIG)
    perturbed = perturb_record(record, noise=0.2)
    assert perturbed["flower_diameter_cm"] != record["flower_diameter_cm"]


def test_summarize_batch_produces_means():
    records = generate_batch(2)
    summary = summarize_batch(records)
    assert "flower_diameter_cm" in summary
