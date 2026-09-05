from rolepilot_agent.backend import MemoryBackend
from rolepilot_agent.tools import process_queue_safely


def test_boolean_opportunity_id_fails_closed_without_aliasing_real_id():
    class BooleanIdBackend(MemoryBackend):
        def list_opportunities(self) -> list[dict]:
            return [{"id": True, "title": "Malformed boolean id"}, *super().list_opportunities()[1:]]

    backend = BooleanIdBackend()
    result = process_queue_safely(backend)

    assert result["external_submission_performed"] is False
    assert result["prepared"] == []
    assert backend.runs == {}
    assert result["decision_points"][0] == {
        "opportunity_id": None,
        "title": "Malformed boolean id",
        "state": "REVIEW",
        "reasons": ["processing_error:TypeError"],
    }
    assert all(item.get("opportunity_id") != 1 for item in result["prepared"])
    assert {
        "action": "stop_for_human_decision",
        "opportunity_id": None,
        "outcome": "REVIEW",
        "reason": "processing_error:TypeError",
    } in result["execution_trace"]
