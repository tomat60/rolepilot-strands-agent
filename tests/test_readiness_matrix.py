import pytest

from rolepilot_agent.domain import Asset, Opportunity, ReadinessState
from rolepilot_agent.safety import SafetyGateError, evaluate_readiness, require_preparable


APPROVED_HEADSHOT = Asset(id=1, kind="headshot", label="Approved headshot", approved=True)
UNAPPROVED_SHOWREEL = Asset(id=2, kind="showreel", label="Old showreel", approved=False)


@pytest.mark.parametrize(
    ("opportunity", "assets", "expected_state", "can_prepare", "missing_assets"),
    [
        (
            Opportunity(id=1, title="Existing materials", brand="Demo", required_assets=("headshot",)),
            [APPROVED_HEADSHOT],
            ReadinessState.READY,
            True,
            (),
        ),
        (
            Opportunity(id=2, title="Needs self tape", brand="Demo", requires_new_recording=True),
            [APPROVED_HEADSHOT],
            ReadinessState.NEEDS_RECORDING,
            False,
            (),
        ),
        (
            Opportunity(id=3, title="Rights review", brand="Demo", manual_review_required=True),
            [APPROVED_HEADSHOT],
            ReadinessState.REVIEW,
            False,
            (),
        ),
        (
            Opportunity(id=4, title="Missing approved reel", brand="Demo", required_assets=("showreel",)),
            [UNAPPROVED_SHOWREEL],
            ReadinessState.REVIEW,
            False,
            ("showreel",),
        ),
        (
            Opportunity(
                id=5,
                title="Recording plus missing asset",
                brand="Demo",
                required_assets=("showreel",),
                requires_new_recording=True,
            ),
            [UNAPPROVED_SHOWREEL],
            ReadinessState.NEEDS_RECORDING,
            False,
            ("showreel",),
        ),
        (
            Opportunity(
                id=6,
                title="Manual review wins",
                brand="Demo",
                required_assets=("showreel",),
                requires_new_recording=True,
                manual_review_required=True,
            ),
            [UNAPPROVED_SHOWREEL],
            ReadinessState.REVIEW,
            False,
            ("showreel",),
        ),
    ],
)
def test_readiness_matrix_is_fail_closed(
    opportunity,
    assets,
    expected_state,
    can_prepare,
    missing_assets,
):
    result = evaluate_readiness(opportunity, assets)

    assert result.state is expected_state
    assert result.can_prepare is can_prepare
    assert result.missing_assets == missing_assets

    if can_prepare:
        require_preparable(result)
    else:
        with pytest.raises(SafetyGateError):
            require_preparable(result)
