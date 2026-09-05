from io import BytesIO
from urllib.error import HTTPError

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


def test_xano_analyze_fails_closed_on_string_false(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": 99,
            "state": "READY",
            "can_prepare": "false",
        },
    )

    result = backend.analyze(1)

    assert result["can_prepare"] is False
    assert result["state"] == "REVIEW"
    assert result["safety_warning"] == "malformed_can_prepare"


def test_xano_analyze_fails_closed_on_contradictory_state(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": 99,
            "state": "REVIEW",
            "can_prepare": True,
        },
    )

    result = backend.analyze(1)

    assert result["can_prepare"] is False
    assert result["state"] == "REVIEW"
    assert result["safety_warning"] == "inconsistent_ready_state"


def test_xano_analyze_fails_closed_on_malformed_readiness_without_echo(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    private_value = "private@example.com secret casting payload"
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": private_value,
            "state": "READY",
            "can_prepare": True,
        },
    )

    result = backend.analyze(1)

    assert result["readiness"] == 0
    assert result["can_prepare"] is False
    assert result["state"] == "REVIEW"
    assert result["safety_warning"] == "malformed_readiness"
    assert private_value not in repr(result)


def test_xano_analyze_treats_boolean_readiness_as_malformed(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": True,
            "state": "READY",
            "can_prepare": True,
        },
    )

    result = backend.analyze(1)

    assert result["readiness"] == 0
    assert result["can_prepare"] is False
    assert result["state"] == "REVIEW"
    assert result["safety_warning"] == "malformed_readiness"


def test_xano_http_error_does_not_expose_remote_body(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    private_body = b'{"email":"private@example.com","casting":"secret"}'

    def fail_urlopen(*args, **kwargs):
        raise HTTPError(
            url="https://example.invalid/api:rolepilot/opportunities",
            code=403,
            msg="Forbidden",
            hdrs=None,
            fp=BytesIO(private_body),
        )

    monkeypatch.setattr("rolepilot_agent.backend.request.urlopen", fail_urlopen)

    with pytest.raises(RuntimeError) as captured:
        backend.list_opportunities()

    message = str(captured.value)
    assert message == "Xano returned HTTP 403"
    assert "private@example.com" not in message
    assert "secret" not in message
