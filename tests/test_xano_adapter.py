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

    assert result["id"] == 7
    assert result["opportunity_id"] == 1
    assert result["approval_state"] == "PENDING_HUMAN_APPROVAL"
    assert result["external_submission_performed"] is False
    assert requests == [("POST", "/runs", {"opportunity_id": 1})]


def test_xano_create_run_does_not_echo_private_backend_fields(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    private_value = "private@example.com secret casting payload"
    monkeypatch.setattr(
        backend,
        "analyze",
        lambda opportunity_id: {
            "opportunity_id": opportunity_id,
            "state": "READY",
            "can_prepare": True,
        },
    )
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "run": {
                "id": 7,
                "opportunity_id": payload["opportunity_id"],
                "private_profile": private_value,
                "audit_events": [private_value],
                "external_submission_performed": True,
            },
            "debug": private_value,
        },
    )

    result = backend.create_run(1)

    assert result == {
        "id": 7,
        "opportunity_id": 1,
        "readiness": 0,
        "approval_state": "PENDING_HUMAN_APPROVAL",
        "audit_events": [
            "Deterministic safety gate passed",
            "Xano preparation state persisted",
            "Human approval required before external action",
        ],
        "external_submission_performed": False,
    }
    assert private_value not in repr(result)


def test_xano_create_run_rejects_inconsistent_opportunity_id(monkeypatch):
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
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {"id": 7, "opportunity_id": 999},
    )

    with pytest.raises(RuntimeError, match="inconsistent opportunity id"):
        backend.create_run(1)


def test_xano_demo_approval_is_explicitly_non_external(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    private_value = "private@example.com secret casting payload"
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "id": 7,
            "approval_state": "APPROVED_DEMO_STATE",
            "external_submission_performed": True,
            "private_profile": private_value,
        },
    )

    result = backend.record_human_decision(7, True)

    assert result["id"] == 7
    assert result["approval_state"] == "APPROVED_DEMO_STATE"
    assert result["external_submission_performed"] is False
    assert private_value not in repr(result)


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


def test_xano_analyze_fails_closed_on_missing_can_prepare(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": 99,
            "state": "READY",
        },
    )

    result = backend.analyze(1)

    assert result["can_prepare"] is False
    assert result["state"] == "REVIEW"
    assert result["safety_warning"] == "missing_can_prepare"


def test_xano_analyze_fails_closed_on_missing_state(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": 99,
            "can_prepare": True,
        },
    )

    result = backend.analyze(1)

    assert result["can_prepare"] is False
    assert result["state"] == "REVIEW"
    assert result["safety_warning"] == "missing_state"


def test_xano_analyze_fails_closed_on_ready_below_threshold(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": 42,
            "state": "READY",
            "can_prepare": True,
        },
    )

    result = backend.analyze(1)

    assert result["can_prepare"] is False
    assert result["state"] == "REVIEW"
    assert result["safety_warning"] == "insufficient_readiness"


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
