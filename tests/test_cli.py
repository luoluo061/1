"""Tests for CLI wiring."""

from flower_trait_modeling import cli


def test_build_parser_contains_arguments():
    parser = cli.build_parser()
    args = parser.parse_args(["data.csv", "--config-dir", "configs", "--storage", "out"])
    assert args.csv == "data.csv"
    assert args.config_dir == "configs"
    assert args.storage == "out"
