import pytest

from rolepilot_agent.backend import MemoryBackend
from rolepilot_agent.tools import (
    _require_confirmed_analysis,
    _require_confirmed_run,
    process_queue_safely,
)


def test_analysis_identity_rejects_lossy_numeric_alias():
    with pytest.raises(TypeError, match="Malformed analysis identity"):
        _require_confirmed_analysis(
            {"opportunity_id": 1.7, "state": "READY", "can_prepare": True}, 1
        )


def test_persisted_run_identity_rejects_lossy_numeric_aliases():
    with pytest.raises(TypeError, match="Malformed run identity"):
        _require_confirmed_run({"id": 41.2, "opportunity_id": 1}, 1)

    with pytest.raises(TypeError, match="Malformed run identity"):
        _require_confirmed_run({"id": 41, "opportunity_id": 1.7}, 1)


def test_queue_opportunity_id_rejects_lossy_numeric_alias_before_analysis():
    class FloatIdBackend(MemoryBackend):
        def list_opportunities(self) -> list[dict]:
            return [{"id": 1.7, "title": "Malformed float id"}]

        def analyze(self, opportunity_id: int):
            raise AssertionError("lossy queue id must fail before analysis")

    backend = FloatIdBackend()
    result = process_queue_safely(backend)

    assert result["prepared"] == []
    assert backend.runs == {}
    assert result["decision_points"] == [
        {
            "opportunity_id": None,
            "title": "Malformed float id",
            "state": "REVIEW",
            "reasons": ["processing_error:TypeError"],
        }
    ]
    assert result["external_submission_performed"] is False
