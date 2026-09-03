from __future__ import annotations

from strands import tool

from .backend import Backend


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
        record_human_decision,
    ]
