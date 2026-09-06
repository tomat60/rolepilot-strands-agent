from rolepilot_agent.tools import process_queue_safely


class UnconfirmedRunBackend:
    def list_opportunities(self):
        return [
            {"id": 1, "title": "Safe synthetic role"},
            {"id": 2, "title": "Later synthetic role"},
        ]

    def analyze(self, opportunity_id: int):
        return {
            "opportunity_id": opportunity_id,
            "state": "READY",
            "can_prepare": True,
            "reasons": ["ready_for_preparation"],
        }

    def create_run(self, opportunity_id: int):
        if opportunity_id == 1:
            return {"id": 41, "opportunity_id": 999, "private_note": "do not expose"}
        return {"id": 42, "opportunity_id": 2}

    def record_human_decision(self, run_id: int, approved: bool):
        raise AssertionError("not used")


def test_queue_requires_persisted_run_identity_and_continues_other_lanes():
    result = process_queue_safely(UnconfirmedRunBackend())

    assert [item["opportunity_id"] for item in result["prepared"]] == [2]
    assert result["prepared"][0]["run"] == {"id": 42, "opportunity_id": 2}

    failed = result["decision_points"][0]
    assert failed == {
        "opportunity_id": 1,
        "title": "Safe synthetic role",
        "state": "REVIEW",
        "reasons": ["processing_error:ValueError"],
    }

    public_result = repr(result)
    assert "private_note" not in public_result
    assert "do not expose" not in public_result
    assert result["external_submission_performed"] is False


def test_queue_rejects_missing_run_identity():
    backend = UnconfirmedRunBackend()
    backend.create_run = lambda opportunity_id: {"id": 41}

    result = process_queue_safely(backend)

    assert result["prepared"] == []
    assert all(item["state"] == "REVIEW" for item in result["decision_points"])
    assert all(
        item["reasons"] == ["processing_error:TypeError"]
        for item in result["decision_points"]
    )
