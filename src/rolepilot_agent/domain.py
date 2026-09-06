from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any


class ReadinessState(str, Enum):
    READY = "READY"
    NEEDS_RECORDING = "NEEDS_RECORDING"
    REVIEW = "REVIEW"


@dataclass(frozen=True)
class Opportunity:
    id: int
    title: str
    brand: str
    required_assets: tuple[str, ...] = ()
    requires_new_recording: bool = False
    manual_review_required: bool = False
    raw_text: str = ""


@dataclass(frozen=True)
class Asset:
    id: int
    kind: str
    label: str
    approved: bool = True


@dataclass(frozen=True)
class ReadinessResult:
    opportunity_id: int
    state: ReadinessState
    can_prepare: bool
    missing_assets: tuple[str, ...] = ()
    reasons: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["state"] = self.state.value
        return data


@dataclass
class ApplicationRun:
    id: int
    opportunity_id: int
    readiness: int
    approval_state: str = "PENDING_HUMAN_APPROVAL"
    audit_events: list[str] = field(default_factory=list)
    external_submission_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
