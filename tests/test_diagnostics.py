"""Tests for diagnostics module."""

from flower_trait_modeling.app.diagnostics import DiagnosticProbe, DiagnosticReport, default_diagnostics, TraceRecorder


def test_diagnostic_probe_returns_status():
    probe = DiagnosticProbe(name="demo", description="desc")
    result = probe.run({"a": 1})
    assert result["status"] == "ok"


def test_diagnostic_report_summarize_formats():
    report = DiagnosticReport(probes=[DiagnosticProbe(name="a", description="")])
    results = report.execute({"x": 1})
    summary = report.summarize(results)
    assert "Probe" in summary


def test_default_diagnostics_contains_probes():
    report = default_diagnostics()
    assert len(report.probes) >= 3


def test_trace_recorder_stores_records():
    recorder = TraceRecorder(records=[])
    recorder.record("step1", {"x": 1}, note="normalized")
    markdown = recorder.as_markdown()
    assert "step1" in markdown
    recorder.clear()
    assert recorder.records == []
