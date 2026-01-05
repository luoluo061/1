"""Workflow helper describing typical processing stages."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable, Dict, List

from ..utils.logging import get_logger

logger = get_logger(__name__)


@dataclass
class WorkflowStep:
    name: str
    description: str
    action: Callable[[Dict[str, object]], Dict[str, object]]

    def run(self, payload: Dict[str, object]) -> Dict[str, object]:
        logger.debug("Running workflow step", extra={"name": self.name})
        return self.action(payload)


@dataclass
class Workflow:
    """Composable workflow for modeling pipeline."""

    steps: List[WorkflowStep] = field(default_factory=list)

    def add_step(self, step: WorkflowStep) -> None:
        self.steps.append(step)
        logger.info("Added workflow step", extra={"name": step.name})

    def execute(self, payload: Dict[str, object]) -> Dict[str, object]:
        state = dict(payload)
        for step in self.steps:
            state = step.run(state)
        logger.info("Workflow executed", extra={"steps": [s.name for s in self.steps]})
        return state

    def describe(self) -> str:
        return " -> ".join(step.name for step in self.steps)


def noop_action(payload: Dict[str, object]) -> Dict[str, object]:
    return payload


def build_default_workflow() -> Workflow:
    workflow = Workflow()
    workflow.add_step(WorkflowStep(name="ingestion", description="Data intake", action=noop_action))
    workflow.add_step(WorkflowStep(name="validation", description="Field checks", action=noop_action))
    workflow.add_step(WorkflowStep(name="normalization", description="Standardize traits", action=noop_action))
    workflow.add_step(WorkflowStep(name="vectorization", description="Build feature vectors", action=noop_action))
    workflow.add_step(WorkflowStep(name="profiling", description="Generate profile", action=noop_action))
    return workflow


__all__ = ["WorkflowStep", "Workflow", "build_default_workflow"]
