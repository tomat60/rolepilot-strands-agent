from __future__ import annotations

import os
from dataclasses import dataclass


class LiveModelConfigurationError(RuntimeError):
    """Raised before any model call when explicit live Bedrock config is missing."""


@dataclass(frozen=True)
class BedrockSettings:
    model_id: str
    region_name: str


def bedrock_settings_from_env() -> BedrockSettings:
    """Load explicit Bedrock settings without making an AWS network call.

    We intentionally require both values instead of silently accepting the Strands
    default provider/model. A live model invocation can incur AWS cost, so the
    competition-safe CLI must make that transition deliberate and inspectable.
    """

    model_id = os.getenv("ROLEPILOT_BEDROCK_MODEL_ID", "").strip()
    region_name = (
        os.getenv("ROLEPILOT_BEDROCK_REGION", "").strip()
        or os.getenv("AWS_REGION", "").strip()
        or os.getenv("AWS_DEFAULT_REGION", "").strip()
    )

    missing: list[str] = []
    if not model_id:
        missing.append("ROLEPILOT_BEDROCK_MODEL_ID")
    if not region_name:
        missing.append("ROLEPILOT_BEDROCK_REGION (or AWS_REGION/AWS_DEFAULT_REGION)")

    if missing:
        raise LiveModelConfigurationError(
            "Live Bedrock execution is disabled until explicit configuration is set: "
            + ", ".join(missing)
        )

    return BedrockSettings(model_id=model_id, region_name=region_name)


def build_bedrock_model(settings: BedrockSettings):
    """Construct the Strands Bedrock provider after the explicit owner gate."""

    from strands.models import BedrockModel

    return BedrockModel(
        model_id=settings.model_id,
        region_name=settings.region_name,
        temperature=0.0,
    )
