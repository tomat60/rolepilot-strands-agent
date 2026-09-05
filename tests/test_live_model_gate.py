import pytest

from rolepilot_agent.live_model import (
    LiveModelConfigurationError,
    bedrock_settings_from_env,
)


def _clear_bedrock_env(monkeypatch):
    for key in (
        "ROLEPILOT_BEDROCK_MODEL_ID",
        "ROLEPILOT_BEDROCK_REGION",
        "AWS_REGION",
        "AWS_DEFAULT_REGION",
    ):
        monkeypatch.delenv(key, raising=False)


def test_live_bedrock_requires_explicit_model_and_region(monkeypatch):
    _clear_bedrock_env(monkeypatch)

    with pytest.raises(LiveModelConfigurationError) as exc:
        bedrock_settings_from_env()

    message = str(exc.value)
    assert "ROLEPILOT_BEDROCK_MODEL_ID" in message
    assert "ROLEPILOT_BEDROCK_REGION" in message


def test_live_bedrock_settings_are_loaded_without_network_call(monkeypatch):
    _clear_bedrock_env(monkeypatch)
    monkeypatch.setenv("ROLEPILOT_BEDROCK_MODEL_ID", "example.model-id")
    monkeypatch.setenv("AWS_REGION", "eu-central-1")

    settings = bedrock_settings_from_env()

    assert settings.model_id == "example.model-id"
    assert settings.region_name == "eu-central-1"
