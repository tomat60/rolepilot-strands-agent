from rolepilot_agent.agent import SYSTEM_PROMPT
from rolepilot_agent.backend import MemoryBackend
from rolepilot_agent.tools import build_tools, process_queue_safely


def test_agent_prompt_preserves_external_action_boundary():
    prompt = SYSTEM_PROMPT.lower()
    assert "never claim a real casting application was submitted" in prompt
    assert "human approval may update internal demo state only" in prompt


def test_strands_toolset_contains_real_product_actions():
    tools = build_tools(MemoryBackend())
    names = {getattr(item, "tool_name", getattr(item, "__name__", "")) for item in tools}

    assert len(tools) == 5
    assert any("opportun" in name for name in names)
    assert any("prepare" in name for name in names)
    assert any("queue" in name for name in names)
    assert any("human" in name or "decision" in name for name in names)


def test_queue_autonomy_prepares_only_ready_and_surfaces_real_decisions():
    backend = MemoryBackend()

    result = process_queue_safely(backend)

    assert result["external_submission_performed"] is False
    assert len(result["prepared"]) == 1
    assert result["prepared"][0]["opportunity_id"] == 1
    assert result["prepared"][0]["run"]["approval_state"] == "PENDING_HUMAN_APPROVAL"

    decisions = {item["opportunity_id"]: item for item in result["decision_points"]}
    assert decisions[2]["state"] == "NEEDS_RECORDING"
    assert decisions[3]["state"] == "REVIEW"

    assert len(backend.runs) == 1
    assert backend.runs[1].external_submission_performed is False
