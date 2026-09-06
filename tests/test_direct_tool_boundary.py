import pytest

from rolepilot_agent.backend import MemoryBackend
from rolepilot_agent.tools import (
    prepare_application_run_safely,
    record_human_decision_safely,
)


def test_direct_prepare_rejects_boolean_opportunity_identifier():
    backend = MemoryBackend()

    with pytest.raises(TypeError, match="Malformed opportunity id"):
        prepare_application_run_safely(backend, True)

    assert backend.runs == {}


def test_direct_prepare_requires_persisted_identity_confirmation():
    class WrongRunBackend(MemoryBackend):
        def create_run(self, opportunity_id: int) -> dict:
            run = super().create_run(opportunity_id)
            run["opportunity_id"] = opportunity_id + 1
            return run

    backend = WrongRunBackend()

    with pytest.raises(ValueError, match="Persisted run opportunity mismatch"):
        prepare_application_run_safely(backend, 1)


def test_human_decision_rejects_boolean_run_identifier():
    backend = MemoryBackend()
    run = prepare_application_run_safely(backend, 1)

    with pytest.raises(TypeError, match="Malformed run id"):
        record_human_decision_safely(backend, True, True)

    assert backend.runs[run["id"]].approval_state == "PENDING_HUMAN_APPROVAL"


def test_human_decision_requires_explicit_boolean_decision():
    backend = MemoryBackend()
    run = prepare_application_run_safely(backend, 1)

    with pytest.raises(TypeError, match="Malformed approval decision"):
        record_human_decision_safely(backend, run["id"], 1)

    assert backend.runs[run["id"]].approval_state == "PENDING_HUMAN_APPROVAL"


def test_human_decision_requires_backend_to_confirm_same_run():
    class WrongDecisionRunBackend(MemoryBackend):
        def record_human_decision(self, run_id: int, approved: bool) -> dict:
            result = super().record_human_decision(run_id, approved)
            result["id"] = run_id + 1
            return result

    backend = WrongDecisionRunBackend()
    run = prepare_application_run_safely(backend, 1)

    with pytest.raises(ValueError, match="Decision run mismatch"):
        record_human_decision_safely(backend, run["id"], True)


def test_human_decision_never_reports_external_submission():
    backend = MemoryBackend()
    run = prepare_application_run_safely(backend, 1)

    result = record_human_decision_safely(backend, run["id"], True)

    assert result["id"] == run["id"]
    assert result["approval_state"] == "APPROVED_DEMO_STATE"
    assert result["external_submission_performed"] is False
