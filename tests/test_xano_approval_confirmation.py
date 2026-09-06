import pytest

from rolepilot_agent.backend import XanoBackend


def test_xano_approval_requires_explicit_run_id_confirmation(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(backend, "_request", lambda method, path, payload=None: {})

    with pytest.raises(RuntimeError, match="malformed run id"):
        backend.record_human_decision(7, True)


def test_xano_approval_rejects_mismatched_run_id(monkeypatch):
    backend = XanoBackend("https://example.invalid/api:rolepilot")
    monkeypatch.setattr(
        backend,
        "_request",
        lambda method, path, payload=None: {"id": 99},
    )

    with pytest.raises(RuntimeError, match="inconsistent run id"):
        backend.record_human_decision(7, True)
