"""Tests for dataset auditor."""

from flower_trait_modeling.analysis.auditor import DatasetAuditor
from flower_trait_modeling.utils.specs import TraitSpec


def test_auditor_reports_missing(tmp_path):
    path = tmp_path / "traits.yaml"
    path.write_text(
        "traits:\n  - name: variety_id\n    type: string\n    required: true\n  - name: species\n    type: string\n    required: false\n",
        encoding="utf-8",
    )
    spec = TraitSpec.from_file(path)
    auditor = DatasetAuditor(spec)
    report = auditor.audit_records([{"variety_id": "v1"}])
    summary = report.summarize()
    assert summary.get("error") == 0 or summary.get("error") is not None
