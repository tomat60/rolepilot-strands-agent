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

    trace = result["execution_trace"]
    assert trace[0] == {"action": "list_opportunities", "outcome": "ok", "count": 3}
    assert {
        "action": "prepare_application_run",
        "opportunity_id": 1,
        "outcome": "PENDING_HUMAN_APPROVAL",
        "run_id": 1,
    } in trace
    assert {
        "action": "stop_for_human_decision",
        "opportunity_id": 2,
        "outcome": "NEEDS_RECORDING",
    } in trace
    assert {
        "action": "stop_for_human_decision",
        "opportunity_id": 3,
        "outcome": "REVIEW",
    } in trace


def test_queue_rerun_reuses_existing_active_preparation_run():
    backend = MemoryBackend()

    first = process_queue_safely(backend)
    second = process_queue_safely(backend)

    assert len(backend.runs) == 1
    assert first["prepared"][0]["run"]["id"] == 1
    assert second["prepared"][0]["run"]["id"] == 1
    assert second["prepared"][0]["run"]["approval_state"] == "PENDING_HUMAN_APPROVAL"
    assert second["external_submission_performed"] is False


def test_changes_requested_allows_fresh_preparation_run():
    backend = MemoryBackend()

    first = process_queue_safely(backend)
    first_run_id = first["prepared"][0]["run"]["id"]
    backend.record_human_decision(first_run_id, approved=False)

    second = process_queue_safely(backend)

    assert len(backend.runs) == 2
    assert second["prepared"][0]["run"]["id"] == 2
    assert second["prepared"][0]["run"]["approval_state"] == "PENDING_HUMAN_APPROVAL"
    assert second["external_submission_performed"] is False


def test_queue_failure_isolated_to_one_opportunity_and_fails_closed():
    class OneOpportunityFailsBackend(MemoryBackend):
        def analyze(self, opportunity_id: int) -> dict:
            if opportunity_id == 2:
                raise RuntimeError("private backend detail must not escape")
            return super().analyze(opportunity_id)

    backend = OneOpportunityFailsBackend()
    result = process_queue_safely(backend)

    assert result["external_submission_performed"] is False
    assert [item["opportunity_id"] for item in result["prepared"]] == [1]

    decisions = {item["opportunity_id"]: item for item in result["decision_points"]}
    assert decisions[2]["state"] == "REVIEW"
    assert decisions[2]["reasons"] == ["processing_error:RuntimeError"]
    assert "private backend detail" not in str(decisions[2])
    assert decisions[3]["state"] == "REVIEW"
    assert "private backend detail" not in str(result["execution_trace"])
    assert {
        "action": "stop_for_human_decision",
        "opportunity_id": 2,
        "outcome": "REVIEW",
        "reason": "processing_error:RuntimeError",
    } in result["execution_trace"]


def test_prepare_failure_becomes_review_and_queue_continues():
    class PrepareFailsBackend(MemoryBackend):
        def create_run(self, opportunity_id: int) -> dict:
            if opportunity_id == 1:
                raise TimeoutError("temporary persistence failure")
            return super().create_run(opportunity_id)

    backend = PrepareFailsBackend()
    result = process_queue_safely(backend)

    assert result["prepared"] == []
    decisions = {item["opportunity_id"]: item for item in result["decision_points"]}
    assert decisions[1]["state"] == "REVIEW"
    assert decisions[1]["reasons"] == ["processing_error:TimeoutError"]
    assert decisions[2]["state"] == "NEEDS_RECORDING"
    assert decisions[3]["state"] == "REVIEW"
    assert backend.runs == {}
