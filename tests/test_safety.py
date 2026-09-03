import pytest

from rolepilot_agent.backend import MemoryBackend
from rolepilot_agent.safety import SafetyGateError


def test_ready_opportunity_can_be_prepared():
    backend = MemoryBackend()

    analysis = backend.analyze(1)
    run = backend.create_run(1)

    assert analysis["state"] == "READY"
    assert analysis["can_prepare"] is True
    assert run["approval_state"] == "PENDING_HUMAN_APPROVAL"
    assert run["external_submission_performed"] is False


def test_recording_required_opportunity_is_blocked():
    backend = MemoryBackend()

    analysis = backend.analyze(2)

    assert analysis["state"] == "NEEDS_RECORDING"
    assert analysis["can_prepare"] is False
    with pytest.raises(SafetyGateError):
        backend.create_run(2)


def test_manual_review_opportunity_is_blocked():
    backend = MemoryBackend()

    analysis = backend.analyze(3)

    assert analysis["state"] == "REVIEW"
    assert analysis["can_prepare"] is False
    with pytest.raises(SafetyGateError):
        backend.create_run(3)


def test_human_approval_never_performs_external_submission():
    backend = MemoryBackend()
    run = backend.create_run(1)

    approved = backend.record_human_decision(run["id"], True)

    assert approved["approval_state"] == "APPROVED_DEMO_STATE"
    assert approved["external_submission_performed"] is False
    assert "Human approval recorded" in approved["audit_events"]
