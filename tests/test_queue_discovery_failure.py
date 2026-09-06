from rolepilot_agent.backend import MemoryBackend
from rolepilot_agent.tools import process_queue_safely


def test_queue_discovery_failure_fails_closed_without_private_error_text():
    private_value = "private-user@example.com secret casting payload"

    class DiscoveryFailsBackend(MemoryBackend):
        def list_opportunities(self) -> list[dict]:
            raise RuntimeError(private_value)

    result = process_queue_safely(DiscoveryFailsBackend())

    assert result == {
        "prepared": [],
        "decision_points": [
            {
                "opportunity_id": None,
                "title": None,
                "state": "REVIEW",
                "reasons": ["queue_discovery_error:RuntimeError"],
            }
        ],
        "execution_trace": [
            {
                "action": "list_opportunities",
                "outcome": "REVIEW",
                "reason": "queue_discovery_error:RuntimeError",
            }
        ],
        "external_submission_performed": False,
    }
    assert private_value not in repr(result)


def test_non_list_queue_response_fails_closed():
    class MalformedQueueBackend(MemoryBackend):
        def list_opportunities(self):
            return {"private": "payload"}

    result = process_queue_safely(MalformedQueueBackend())

    assert result["prepared"] == []
    assert result["external_submission_performed"] is False
    assert result["decision_points"][0]["state"] == "REVIEW"
    assert result["decision_points"][0]["reasons"] == ["queue_discovery_error:TypeError"]
