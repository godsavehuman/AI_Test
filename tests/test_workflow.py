import pytest

from src.workflow.workflow import Step, Workflow, Runner, sample_workflow


def test_sample_workflow_runs():
    # Use the included sample_workflow (pure-Python, no network)
    wf = sample_workflow()
    # provide initial input the sample steps expect
    runner = Runner()
    result = runner.run(wf, initial_context={"text": "Alice data"})

    assert "context" in result
    assert result["context"]["entity"] == "Alice"
    assert result["context"]["entity_upper"] == "ALICE"
    assert result["context"]["summary"] == "Entity=ALICE"
    assert list(result["step_outputs"].keys()) == ["extract", "transform", "summarize"]


def test_step_returns_non_dict_raises():
    def bad_step(ctx):
        return 123  # invalid: must be dict

    wf = Workflow([Step("bad", bad_step)])
    with pytest.raises(TypeError):
        Runner().run(wf)


def test_custom_small_workflow():
    # Basic arithmetic pipeline
    def s1(ctx):
        return {"x": 1}

    def s2(ctx):
        return {"y": ctx["x"] + 2}

    def s3(ctx):
        return {"z": ctx["x"] + ctx["y"]}

    wf = Workflow([Step("s1", s1), Step("s2", s2), Step("s3", s3)])
    out = Runner().run(wf)
    assert out["context"]["x"] == 1
    assert out["context"]["y"] == 3
    assert out["context"]["z"] == 4
