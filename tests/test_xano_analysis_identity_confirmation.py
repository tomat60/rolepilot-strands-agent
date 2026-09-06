import pytest

from rolepilot_agent.backend import XanoBackend


def test_xano_analyze_requires_explicit_opportunity_id(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "readiness": 99,
            "state": "READY",
            "can_prepare": True,
        },
    )

    with pytest.raises(RuntimeError, match="malformed opportunity id"):
        backend.analyze(1)
