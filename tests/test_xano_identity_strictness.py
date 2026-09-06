import pytest

from rolepilot_agent.backend import XanoBackend


def test_xano_list_opportunities_rejects_lossy_identity_alias(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: [
            {"id": 1.7, "title": "Malformed id", "brand": "Example"}
        ],
    )

    with pytest.raises(RuntimeError, match="malformed opportunity id"):
        backend.list_opportunities()


def test_xano_analyze_rejects_string_identity_alias(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": "1",
            "readiness": 99,
            "state": "READY",
            "can_prepare": True,
        },
    )

    with pytest.raises(RuntimeError, match="malformed opportunity id"):
        backend.analyze(1)


def test_xano_run_response_rejects_lossy_run_identity_alias(monkeypatch):
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
        lambda method, path, payload=None: {
            "run": {"id": 7.9, "opportunity_id": payload["opportunity_id"]}
        },
    )

    with pytest.raises(RuntimeError, match="malformed run id"):
        backend.create_run(1)
