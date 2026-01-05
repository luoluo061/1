"""Tests for workflow helper."""

from flower_trait_modeling.app.workflow import build_default_workflow, WorkflowStep, Workflow


def test_workflow_execution_preserves_payload():
    workflow = build_default_workflow()
    result = workflow.execute({"value": 1})
    assert result["value"] == 1


def test_workflow_allows_custom_step():
    def increment(payload):
        payload = dict(payload)
        payload["value"] = payload.get("value", 0) + 1
        return payload

    workflow = Workflow()
    workflow.add_step(WorkflowStep(name="inc", description="increment", action=increment))
    output = workflow.execute({"value": 1})
    assert output["value"] == 2
