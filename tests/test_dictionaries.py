"""Tests for trait dictionaries."""

from flower_trait_modeling.utils.dictionaries import (
    TRAIT_DICTIONARY,
    describe_traits,
    ensure_trait,
    list_trait_names,
    render_markdown_table,
)


def test_describe_traits_outputs_all():
    text = describe_traits()
    for key in TRAIT_DICTIONARY:
        assert key in text


def test_ensure_trait_returns_entry():
    entry = ensure_trait("species")
    assert entry.name == "species"


def test_list_trait_names_sorted():
    names = list_trait_names()
    assert names == sorted(names)


def test_render_markdown_table_contains_header():
    table = render_markdown_table()
    assert "Trait" in table.splitlines()[0]
