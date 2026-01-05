"""Tests for ingestion importers and validators."""

from flower_trait_modeling.ingestion import importers, validators
from flower_trait_modeling.domain.enums import FlowerShape, Fragrance, Seasonality


def test_read_csv_and_validate(tmp_path):
    csv_path = tmp_path / "data.csv"
    csv_path.write_text(
        "variety_id,species,flower_shape,flower_diameter_cm,color_primary,stem_length_cm,vase_life_days,fragrance,seasonality\n"
        "v001,rose,double,10,#ff0000,60,10,medium,summer\n",
        encoding="utf-8",
    )
    varieties = importers.read_csv(csv_path)
    assert varieties[0].flower_shape == FlowerShape.DOUBLE


def test_batch_validate_collects_ids():
    ids = validators.batch_validate([
        {
            "variety_id": "v001",
            "species": "rose",
            "flower_shape": "single",
            "flower_diameter_cm": "5",
            "color_primary": "#ff0000",
            "stem_length_cm": "30",
            "vase_life_days": "5",
        }
    ])
    assert ids == ["v001"]


def test_import_iterable_skips_invalid():
    records = [
        {"variety_id": "v1", "species": "rose", "flower_shape": "single", "flower_diameter_cm": 5, "color_primary": "#000", "stem_length_cm": 10, "vase_life_days": 5, "fragrance": Fragrance.NONE, "seasonality": Seasonality.SUMMER},
        {"variety_id": "", "species": "rose", "flower_shape": "single", "flower_diameter_cm": 0, "color_primary": "#000", "stem_length_cm": 0, "vase_life_days": 0, "fragrance": Fragrance.NONE, "seasonality": Seasonality.SUMMER},
    ]
    varieties = importers.import_iterable(records)
    assert len(varieties) == 1
