from rolepilot_agent.agent import SYSTEM_PROMPT
from rolepilot_agent.backend import MemoryBackend
from rolepilot_agent.tools import build_tools


def test_agent_prompt_preserves_external_action_boundary():
    prompt = SYSTEM_PROMPT.lower()
    assert "never claim a real casting application was submitted" in prompt
    assert "human approval may update internal demo state only" in prompt


def test_strands_toolset_contains_real_product_actions():
    tools = build_tools(MemoryBackend())
    names = {getattr(item, "tool_name", getattr(item, "__name__", "")) for item in tools}

    assert len(tools) == 4
    assert any("opportun" in name for name in names)
    assert any("prepare" in name for name in names)
    assert any("human" in name or "decision" in name for name in names)
