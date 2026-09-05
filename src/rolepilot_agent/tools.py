from __future__ import annotations

from strands import tool

from .backend import Backend


CANONICAL_READINESS_STATES = {"READY", "NEEDS_RECORDING", "REVIEW"}


def process_queue_safely(backend: Backend) -> dict:
    """Process the full queue up to the human/external-action boundary.

    This deterministic orchestration is intentionally safe to run without a model:
    every opportunity is analyzed, READY items are prepared, and all other items
    are surfaced as decision points. A failure on one opportunity fails that lane
    closed to REVIEW without stopping the rest of the queue. The returned execution
    trace makes the work performed auditable without exposing private exception text
    or malformed backend identifiers. No external action is available here.
    """
    prepared: list[dict] = []
    decisions: list[dict] = []
    execution_trace: list[dict] = []

    opportunities = backend.list_opportunities()
    execution_trace.append(
        {
            "action": "list_opportunities",
            "outcome": "ok",
            "count": len(opportunities),
        }
    )

    for opportunity in opportunities:
        opportunity_id: int | None = None
        title = None
        try:
            if not isinstance(opportunity, dict):
                raise TypeError("Malformed opportunity item")
            title = opportunity.get("title")
            raw_opportunity_id = opportunity.get("id")
            if isinstance(raw_opportunity_id, bool):
                raise TypeError("Malformed opportunity id")
            opportunity_id = int(raw_opportunity_id)
            analysis = backend.analyze(opportunity_id)
            raw_state = analysis.get("state", "REVIEW")
            state = raw_state if raw_state in CANONICAL_READINESS_STATES else "REVIEW"
            malformed_state = state == "REVIEW" and raw_state not in CANONICAL_READINESS_STATES
            execution_trace.append(
                {
                    "action": "analyze_opportunity",
                    "opportunity_id": opportunity_id,
                    "outcome": state,
                    **({"reason": "malformed_analysis_state"} if malformed_state else {}),
                }
            )

            if state == "READY" and analysis.get("can_prepare") is True:
                run = backend.create_run(opportunity_id)
                prepared.append(
                    {
                        "opportunity_id": opportunity_id,
                        "title": title,
                        "run": run,
                    }
                )
                execution_trace.append(
                    {
                        "action": "prepare_application_run",
                        "opportunity_id": opportunity_id,
                        "outcome": "PENDING_HUMAN_APPROVAL",
                        "run_id": run.get("id"),
                    }
                )
                continue

            reasons = analysis.get("reasons", [])
            if malformed_state:
                reasons = ["malformed_analysis_state"]
            decisions.append(
                {
                    "opportunity_id": opportunity_id,
                    "title": title,
                    "state": state,
                    "reasons": reasons,
                }
            )
            execution_trace.append(
                {
                    "action": "stop_for_human_decision",
                    "opportunity_id": opportunity_id,
                    "outcome": state,
                    **({"reason": "malformed_analysis_state"} if malformed_state else {}),
                }
            )
        except Exception as exc:
            # One malformed or temporarily failing opportunity must not abort the
            # entire autonomous queue. Fail the affected lane closed and expose
            # only the exception class, never backend/private exception text. If
            # the identifier or item itself is malformed, do not echo raw values.
            safe_error = f"processing_error:{type(exc).__name__}"
            decisions.append(
                {
                    "opportunity_id": opportunity_id,
                    "title": title,
                    "state": "REVIEW",
                    "reasons": [safe_error],
                }
            )
            execution_trace.append(
                {
                    "action": "stop_for_human_decision",
                    "opportunity_id": opportunity_id,
                    "outcome": "REVIEW",
                    "reason": safe_error,
                }
            )

    return {
        "prepared": prepared,
        "decision_points": decisions,
        "execution_trace": execution_trace,
        "external_submission_performed": False,
    }


def build_tools(backend: Backend):
    @tool
    def list_casting_opportunities() -> list[dict]:
        """List casting opportunities available for the agent to process."""
        return backend.list_opportunities()

    @tool
    def analyze_casting_opportunity(opportunity_id: int) -> dict:
        """Analyze whether an opportunity is READY, NEEDS_RECORDING, or REVIEW.

        Args:
            opportunity_id: Numeric opportunity identifier.
        """
        return backend.analyze(opportunity_id)

    @tool
    def prepare_application_run(opportunity_id: int) -> dict:
        """Prepare and persist an application run only when the safety gate allows it.

        This tool never submits a real casting application.

        Args:
            opportunity_id: Numeric opportunity identifier.
        """
        return backend.create_run(opportunity_id)

    @tool
    def process_casting_queue() -> dict:
        """Process every available opportunity and return only prepared work and real decision points.

        READY opportunities are prepared and persisted. NEEDS_RECORDING, REVIEW,
        malformed backend analysis state, malformed queue items, and per-opportunity
        processing failures are surfaced without preparation. The result includes a
        deterministic execution trace for auditability. This tool cannot submit externally.
        """
        return process_queue_safely(backend)

    @tool
    def record_human_decision(run_id: int, approved: bool) -> dict:
        """Record the human decision for a prepared demo run.

        Approval updates internal demo state only. It never performs external submission.

        Args:
            run_id: Prepared application run identifier.
            approved: True to approve demo state, False to request changes.
        """
        return backend.record_human_decision(run_id, approved)

    return [
        list_casting_opportunities,
        analyze_casting_opportunity,
        prepare_application_run,
        process_casting_queue,
        record_human_decision,
    ]
