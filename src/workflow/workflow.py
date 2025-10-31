"""
A tiny, code-first workflow runner suitable for LLM-centered pipelines.

This module contains a minimal implementation of Step, Workflow, and Runner.
It is intentionally small and synchronous so it can be used in unit tests and
as a starting point for integrating real LLM calls (which should be made
token-efficient by sending compact prompts and reusing context/state).

Pseudocode (how an LLM would be used inside a Step):

    # PSEUDOCODE
    prompt = build_prompt(step_description, context_summary)
    llm_response = llm.call(prompt, max_tokens=...)  # token-aware
    parsed_output = parse_response(llm_response)
    return parsed_output  # a dict merged into workflow context

Notes:
 - Steps must return dicts. The Runner merges returned dicts into a shared
   context (later steps can read earlier outputs).
 - This is intentionally NOT performing network or LLM calls. Replace step
   functions with wrappers that call your LLM client and return dicts.

"""

from typing import Callable, Dict, Any, List, Optional


class Step:
    """A single step in a workflow.

    Attributes:
        name: unique step name (ordering is preserved by Workflow)
        func: a callable taking the current context (dict) and returning a dict
        description: optional human-readable description / pseudocode
    """

    def __init__(self, name: str, func: Callable[[Dict[str, Any]], Dict[str, Any]], description: str = ""):
        self.name = name
        self.func = func
        self.description = description


class Workflow:
    """A sequence of Steps to execute."""

    def __init__(self, steps: Optional[List[Step]] = None):
        self.steps: List[Step] = list(steps or [])

    def add_step(self, step: Step) -> None:
        self.steps.append(step)


class Runner:
    """Execute a Workflow sequentially and collect outputs.

    Execution contract:
      - Each step.func(context) must return a dict. That dict is merged into
        the shared context (context.update(step_result)).
      - The Runner returns a dict with the final context and per-step outputs.
    """

    def __init__(self) -> None:
        pass

    def run(self, workflow: Workflow, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        context: Dict[str, Any] = dict(initial_context or {})
        step_outputs: Dict[str, Dict[str, Any]] = {}

        for step in workflow.steps:
            # Pass a snapshot of the current context to the step implementation.
            result = step.func(dict(context))
            if not isinstance(result, dict):
                raise TypeError(f"Step '{step.name}' must return a dict, got {type(result).__name__}")

            # Simple merge strategy: later keys overwrite earlier ones.
            context.update(result)
            step_outputs[step.name] = result

        return {"context": context, "step_outputs": step_outputs}


def sample_workflow() -> Workflow:
    """Return a small sample workflow using pure-Python steps (no LLM).

    This function demonstrates how to structure steps so they can be
    replaced by LLM-calling wrappers later.
    """

    def step_extract(context: Dict[str, Any]) -> Dict[str, Any]:
        # Simulated extraction step (would be an llm call in real code)
        text = context.get("text", "")
        # pretend we extracted an 'entity' from text
        return {"entity": text.split()[0] if text else ""}

    def step_transform(context: Dict[str, Any]) -> Dict[str, Any]:
        entity = context.get("entity", "")
        return {"entity_upper": entity.upper()}

    def step_summarize(context: Dict[str, Any]) -> Dict[str, Any]:
        # Would call an LLM in practice; here we compose a short summary
        return {"summary": f"Entity={context.get('entity_upper')}"}

    wf = Workflow([
        Step("extract", step_extract, "Extract entity from text"),
        Step("transform", step_transform, "Transform entity to uppercase"),
        Step("summarize", step_summarize, "Create a compact summary"),
    ])

    return wf


__all__ = ["Step", "Workflow", "Runner", "sample_workflow"]
