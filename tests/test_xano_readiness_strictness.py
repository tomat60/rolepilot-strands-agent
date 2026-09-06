import pytest

from rolepilot_agent.backend import XanoBackend


@pytest.mark.parametrize("readiness", ["94", 94.7, True, None])
def test_xano_analyze_rejects_non_integer_readiness(monkeypatch, readiness):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": readiness,
            "state": "READY",
            "can_prepare": True,
        },
    )

    result = backend.analyze(1)

    assert result["readiness"] == 0
    assert result["can_prepare"] is False
    assert result["state"] == "REVIEW"
    assert result["safety_warning"] == "malformed_readiness"


def test_xano_analyze_accepts_real_integer_readiness(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": 94,
            "state": "READY",
            "can_prepare": True,
        },
    )

    result = backend.analyze(1)

    assert result["readiness"] == 94
    assert result["can_prepare"] is True
    assert result["state"] == "READY"
