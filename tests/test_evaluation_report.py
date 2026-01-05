"""Tests for evaluation report."""

from flower_trait_modeling.evaluation.report import EvaluationReport, EvaluationCase


def test_evaluation_report_runs_cases():
    report = EvaluationReport()
    report.add_case(EvaluationCase(name="case1", relevants=["a", "b"], retrieved=["a", "c"], k=2))
    report.run()
    assert "case1" in report.scores
