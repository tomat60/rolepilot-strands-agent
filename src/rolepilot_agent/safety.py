from __future__ import annotations

from .domain import Asset, Opportunity, ReadinessResult, ReadinessState


class SafetyGateError(RuntimeError):
    """Raised when a consequential preparation transition is not allowed."""


def evaluate_readiness(
    opportunity: Opportunity,
    assets: list[Asset],
) -> ReadinessResult:
    approved_kinds = {asset.kind for asset in assets if asset.approved}
    missing = tuple(
        kind for kind in opportunity.required_assets if kind not in approved_kinds
    )

    if opportunity.manual_review_required:
        return ReadinessResult(
            opportunity_id=opportunity.id,
            state=ReadinessState.REVIEW,
            can_prepare=False,
            missing_assets=missing,
            reasons=("Manual review is required before preparation.",),
        )

    if opportunity.requires_new_recording:
        return ReadinessResult(
            opportunity_id=opportunity.id,
            state=ReadinessState.NEEDS_RECORDING,
            can_prepare=False,
            missing_assets=missing,
            reasons=("A new recording is required.",),
        )

    if missing:
        return ReadinessResult(
            opportunity_id=opportunity.id,
            state=ReadinessState.REVIEW,
            can_prepare=False,
            missing_assets=missing,
            reasons=("One or more required approved assets are missing.",),
        )

    return ReadinessResult(
        opportunity_id=opportunity.id,
        state=ReadinessState.READY,
        can_prepare=True,
        reasons=("All required approved assets are available.",),
    )


def require_preparable(result: ReadinessResult) -> None:
    if not result.can_prepare or result.state is not ReadinessState.READY:
        raise SafetyGateError(
            f"Opportunity {result.opportunity_id} cannot be prepared: {result.state.value}"
        )
