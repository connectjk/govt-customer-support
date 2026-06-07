"""
Multi-step workflow scaffold for govt-customer-support.

This module provides a basic workflow pattern inspired by
Microsoft Agent Framework workflow concepts.
Reference: https://learn.microsoft.com/en-us/agent-framework/workflows/
"""

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class WorkflowStep:
    name: str
    executor: Callable[[dict[str, Any]], dict[str, Any]]


class AgentWorkflow:
    """A simple sequential workflow runner."""

    def __init__(self, name: str = "govt-customer-support_workflow"):
        self.name = name
        self.steps: list[WorkflowStep] = []

    def add_step(self, name: str, executor: Callable) -> "AgentWorkflow":
        self.steps.append(WorkflowStep(name=name, executor=executor))
        return self

    def run(self, initial_context: dict[str, Any] | None = None) -> dict[str, Any]:
        context = initial_context or {}
        for step in self.steps:
            print(f"[Workflow] Running step: {step.name}")
            context = step.executor(context)
        print(f"[Workflow] Completed all {len(self.steps)} steps.")
        return context


# Example usage:
# workflow = AgentWorkflow()
# workflow.add_step("analyse", lambda ctx: {**ctx, "analysis": "done"})
# workflow.add_step("respond", lambda ctx: {**ctx, "response": "done"})
# result = workflow.run()
