import pytest

from rolepilot_agent.backend import XanoBackend


def test_xano_list_opportunities_discards_untrusted_extra_fields(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    private_value = "private@example.com secret casting payload"
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: [
            {
                "id": 1,
                "title": "Commercial role",
                "brand": "Example Brand",
                "private_profile": private_value,
                "raw_casting_email": private_value,
            }
        ],
    )

    result = backend.list_opportunities()

    assert result == [
        {"id": 1, "title": "Commercial role", "brand": "Example Brand"}
    ]
    assert private_value not in repr(result)


def test_xano_analyze_discards_untrusted_extra_fields_and_remote_reasons(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    private_value = "private@example.com secret casting payload"
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": 95,
            "state": "READY",
            "can_prepare": True,
            "reasons": [private_value],
            "private_profile": private_value,
            "raw_casting_email": private_value,
        },
    )

    result = backend.analyze(1)

    assert result == {
        "opportunity_id": 1,
        "readiness": 95,
        "state": "READY",
        "can_prepare": True,
        "reasons": ["ready_for_preparation"],
    }
    assert private_value not in repr(result)


def test_xano_analyze_rejects_inconsistent_opportunity_id(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": 999,
            "readiness": 95,
            "state": "READY",
            "can_prepare": True,
        },
    )

    with pytest.raises(RuntimeError, match="inconsistent opportunity id"):
        backend.analyze(1)


def test_xano_analyze_fails_closed_on_out_of_range_readiness(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {
            "opportunity_id": payload["opportunity_id"],
            "readiness": 900,
            "state": "READY",
            "can_prepare": True,
        },
    )

    result = backend.analyze(1)

    assert result["readiness"] == 0
    assert result["state"] == "REVIEW"
    assert result["can_prepare"] is False
    assert result["safety_warning"] == "malformed_readiness"
    assert result["reasons"] == ["malformed_readiness"]
