import pytest

from rolepilot_agent.backend import XanoBackend
from rolepilot_agent.safety import SafetyGateError


def test_xano_prepare_refuses_non_ready_before_post(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "analyze",
        lambda opportunity_id: {
            "opportunity_id": opportunity_id,
            "state": "REVIEW",
            "can_prepare": False,
        },
    )

    called = False

    def fail_if_called(*args, **kwargs):
        nonlocal called
        called = True
        raise AssertionError("POST /runs must not be reached")

    monkeypatch.setattr(backend, "_request", fail_if_called)

    with pytest.raises(SafetyGateError):
        backend.create_run(3)

    assert called is False


def test_xano_prepare_posts_only_after_ready_gate(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "analyze",
        lambda opportunity_id: {
            "opportunity_id": opportunity_id,
            "state": "READY",
            "can_prepare": True,
        },
    )

    requests = []

    def fake_request(method, path, payload=None):
        requests.append((method, path, payload))
        return {"run": {"id": 7, "opportunity_id": payload["opportunity_id"]}}

    monkeypatch.setattr(backend, "_request", fake_request)

    result = backend.create_run(1)

    assert result["run"]["id"] == 7
    assert requests == [("POST", "/runs", {"opportunity_id": 1})]


def test_xano_demo_approval_is_explicitly_non_external(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "id": 7,
            "approval_state": "APPROVED_DEMO_STATE",
        },
    )

    result = backend.record_human_decision(7, True)

    assert result["external_submission_performed"] is False
