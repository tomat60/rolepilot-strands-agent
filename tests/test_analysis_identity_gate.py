import pytest

from rolepilot_agent.tools import _require_confirmed_analysis, process_queue_safely


class MismatchedAnalysisBackend:
    def list_opportunities(self):
        return [
            {"id": 1, "title": "First"},
            {"id": 2, "title": "Second"},
        ]

    def analyze(self, opportunity_id):
        if opportunity_id == 1:
            return {
                "opportunity_id": 2,
                "state": "READY",
                "can_prepare": True,
                "reasons": ["ready_for_preparation"],
            }
        return {
            "opportunity_id": 2,
            "state": "REVIEW",
            "can_prepare": False,
            "reasons": ["manual_review_required"],
        }

    def create_run(self, opportunity_id):
        raise AssertionError("mismatched analysis must never reach preparation")

    def record_human_decision(self, run_id, approved):
        raise AssertionError("not used")


def test_analysis_identity_requires_explicit_matching_opportunity_id():
    with pytest.raises(TypeError, match="Malformed analysis identity"):
        _require_confirmed_analysis({"state": "READY", "can_prepare": True}, 1)

    with pytest.raises(TypeError, match="Malformed analysis identity"):
        _require_confirmed_analysis(
            {"opportunity_id": True, "state": "READY", "can_prepare": True}, 1
        )

    with pytest.raises(ValueError, match="Analysis opportunity mismatch"):
        _require_confirmed_analysis(
            {"opportunity_id": 2, "state": "READY", "can_prepare": True}, 1
        )


def test_queue_fails_mismatched_analysis_closed_and_continues():
    result = process_queue_safely(MismatchedAnalysisBackend())

    assert result["prepared"] == []
    assert result["external_submission_performed"] is False
    assert result["decision_points"] == [
        {
            "opportunity_id": 1,
            "title": "First",
            "state": "REVIEW",
            "reasons": ["processing_error:ValueError"],
        },
        {
            "opportunity_id": 2,
            "title": "Second",
            "state": "REVIEW",
            "reasons": ["manual_review_required"],
        },
    ]
