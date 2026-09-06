import pytest

from rolepilot_agent.backend import MemoryBackend
from rolepilot_agent.safety import SafetyGateError


@pytest.mark.parametrize("opportunity_id", [2, 3])
def test_direct_prepare_path_cannot_bypass_deterministic_safety_gate(opportunity_id: int):
    """Every preparation entry point must remain safe even if the agent calls it directly."""
    backend = MemoryBackend()

    with pytest.raises(SafetyGateError):
        backend.create_run(opportunity_id)

    assert backend.runs == {}


def test_direct_prepare_path_allows_only_ready_opportunity():
    backend = MemoryBackend()

    run = backend.create_run(1)

    assert run["opportunity_id"] == 1
    assert run["approval_state"] == "PENDING_HUMAN_APPROVAL"
    assert run["external_submission_performed"] is False
