from __future__ import annotations

import json
from dataclasses import asdict
from typing import Protocol
from urllib import error, request

from .domain import ApplicationRun, Asset, Opportunity, ReadinessResult, ReadinessState
from .safety import SafetyGateError, evaluate_readiness, require_preparable


class Backend(Protocol):
    def list_opportunities(self) -> list[dict]: ...
    def analyze(self, opportunity_id: int) -> dict: ...
    def create_run(self, opportunity_id: int) -> dict: ...
    def record_human_decision(self, run_id: int, approved: bool) -> dict: ...


class MemoryBackend:
    """Competition-safe deterministic backend used by tests and offline demos."""

    def __init__(self) -> None:
        self.opportunities = {
            1: Opportunity(
                id=1,
                title="Lifestyle Campaign - Urban Commuter",
                brand="Northline Studio",
                required_assets=("portrait", "full_body", "english_intro", "showreel"),
                raw_text="Male talent 28-38. Warsaw. Existing approved materials accepted.",
            ),
            2: Opportunity(
                id=2,
                title="Fintech Product Film - Office Role",
                brand="Orbit Casting",
                required_assets=("portrait", "slate", "self_tape"),
                requires_new_recording=True,
                raw_text="New slate and improvised self-tape required.",
            ),
            3: Opportunity(
                id=3,
                title="Travel App - Presenter",
                brand="Frame & Form",
                required_assets=("portrait", "showreel"),
                manual_review_required=True,
                raw_text="Usage details require manual review before consent.",
            ),
        }
        self.assets = [
            Asset(1, "portrait", "Portrait 01"),
            Asset(2, "full_body", "Full body"),
            Asset(3, "english_intro", "English intro"),
            Asset(4, "showreel", "Showreel"),
        ]
        self.runs: dict[int, ApplicationRun] = {}
        self._next_run_id = 1

    def list_opportunities(self) -> list[dict]:
        return [asdict(item) for item in self.opportunities.values()]

    def _analysis(self, opportunity_id: int) -> ReadinessResult:
        try:
            opportunity = self.opportunities[opportunity_id]
        except KeyError as exc:
            raise KeyError(f"Unknown opportunity: {opportunity_id}") from exc
        return evaluate_readiness(opportunity, self.assets)

    def analyze(self, opportunity_id: int) -> dict:
        return self._analysis(opportunity_id).to_dict()

    def _find_active_run(self, opportunity_id: int) -> ApplicationRun | None:
        active_states = {"PENDING_HUMAN_APPROVAL", "APPROVED_DEMO_STATE"}
        for run in self.runs.values():
            if run.opportunity_id == opportunity_id and run.approval_state in active_states:
                return run
        return None

    def create_run(self, opportunity_id: int) -> dict:
        result = self._analysis(opportunity_id)
        require_preparable(result)

        existing = self._find_active_run(opportunity_id)
        if existing is not None:
            return existing.to_dict()

        run = ApplicationRun(
            id=self._next_run_id,
            opportunity_id=opportunity_id,
            readiness=94,
            audit_events=[
                "Opportunity requirements normalized",
                "Approved materials matched",
                "Deterministic safety gate passed",
                "Preparation state persisted",
                "Human approval required before external action",
            ],
        )
        self.runs[run.id] = run
        self._next_run_id += 1
        return run.to_dict()

    def record_human_decision(self, run_id: int, approved: bool) -> dict:
        try:
            run = self.runs[run_id]
        except KeyError as exc:
            raise KeyError(f"Unknown run: {run_id}") from exc
        run.approval_state = "APPROVED_DEMO_STATE" if approved else "CHANGES_REQUESTED"
        run.audit_events.append(
            "Human approval recorded" if approved else "Human changes requested"
        )
        run.external_submission_performed = False
        return run.to_dict()


class XanoBackend:
    """Adapter for the Sep 3 RolePilot Xano prototype APIs."""

    def __init__(self, base_url: str, timeout_seconds: float = 10.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    def _request(self, method: str, path: str, payload: dict | None = None):
        data = None if payload is None else json.dumps(payload).encode("utf-8")
        req = request.Request(
            f"{self.base_url}{path}",
            data=data,
            method=method,
            headers={"Content-Type": "application/json"},
        )
        try:
            with request.urlopen(req, timeout=self.timeout_seconds) as response:
                return json.loads(response.read().decode("utf-8"))
        except error.HTTPError as exc:
            # Remote error bodies may contain casting/profile/private backend data.
            # Preserve only the status code at this public adapter boundary.
            raise RuntimeError(f"Xano returned HTTP {exc.code}") from exc

    @staticmethod
    def _safe_int(value, field_name: str) -> int:
        if isinstance(value, bool):
            raise RuntimeError(f"Xano returned malformed {field_name}")
        try:
            return int(value)
        except (TypeError, ValueError) as exc:
            raise RuntimeError(f"Xano returned malformed {field_name}") from exc

    @staticmethod
    def _safe_display_text(value, field_name: str) -> str:
        if not isinstance(value, str):
            raise RuntimeError(f"Xano returned malformed {field_name}")
        text = value.strip()
        if not text or len(text) > 200:
            raise RuntimeError(f"Xano returned malformed {field_name}")
        return text

    @classmethod
    def _normalize_run_response(
        cls,
        response,
        *,
        expected_opportunity_id: int | None = None,
        expected_run_id: int | None = None,
        approved: bool | None = None,
    ) -> dict:
        """Return only canonical, public-safe run fields from an untrusted backend response."""
        if not isinstance(response, dict):
            raise RuntimeError("Xano returned malformed run response")

        raw_run = response.get("run", response)
        if not isinstance(raw_run, dict):
            raise RuntimeError("Xano returned malformed run response")

        # A response must explicitly prove persisted identity. Never synthesize
        # success from the requested run/opportunity identifiers when omitted.
        if expected_run_id is not None and "id" not in raw_run:
            raise RuntimeError("Xano returned malformed run id")
        run_id = cls._safe_int(raw_run.get("id"), "run id")
        if expected_run_id is not None and run_id != expected_run_id:
            raise RuntimeError("Xano returned inconsistent run id")

        if expected_opportunity_id is not None:
            if "opportunity_id" not in raw_run:
                raise RuntimeError("Xano returned malformed opportunity id")
            raw_opportunity_id = raw_run.get("opportunity_id")
            opportunity_id = cls._safe_int(raw_opportunity_id, "opportunity id")
            if opportunity_id != expected_opportunity_id:
                raise RuntimeError("Xano returned inconsistent opportunity id")
        else:
            raw_opportunity_id = raw_run.get("opportunity_id")
            opportunity_id = (
                cls._safe_int(raw_opportunity_id, "opportunity id")
                if raw_opportunity_id is not None
                else None
            )

        if approved is None:
            approval_state = "PENDING_HUMAN_APPROVAL"
            audit_events = [
                "Deterministic safety gate passed",
                "Xano preparation state persisted",
                "Human approval required before external action",
            ]
        else:
            approval_state = "APPROVED_DEMO_STATE" if approved else "CHANGES_REQUESTED"
            audit_events = [
                "Human approval recorded" if approved else "Human changes requested",
                "External submission remains disabled",
            ]

        return {
            "id": run_id,
            "opportunity_id": opportunity_id,
            "readiness": 0,
            "approval_state": approval_state,
            "audit_events": audit_events,
            "external_submission_performed": False,
        }

    def list_opportunities(self) -> list[dict]:
        response = self._request("GET", "/opportunities")
        if not isinstance(response, list):
            raise RuntimeError("Xano returned malformed opportunities response")

        normalized: list[dict] = []
        for item in response:
            if not isinstance(item, dict):
                raise RuntimeError("Xano returned malformed opportunity")
            normalized.append(
                {
                    "id": self._safe_int(item.get("id"), "opportunity id"),
                    "title": self._safe_display_text(item.get("title"), "opportunity title"),
                    "brand": self._safe_display_text(item.get("brand"), "opportunity brand"),
                }
            )
        return normalized

    def analyze(self, opportunity_id: int) -> dict:
        result = self._request("POST", "/analyze", {"opportunity_id": opportunity_id})
        if not isinstance(result, dict):
            raise RuntimeError("Xano returned malformed analysis response")

        remote_opportunity_id = self._safe_int(
            result.get("opportunity_id", opportunity_id), "opportunity id"
        )
        if remote_opportunity_id != opportunity_id:
            raise RuntimeError("Xano returned inconsistent opportunity id")

        safety_warning: str | None = None
        raw_readiness = result.get("readiness", 0)
        if isinstance(raw_readiness, bool):
            readiness = 0
            safety_warning = "malformed_readiness"
        else:
            try:
                readiness = int(raw_readiness)
            except (TypeError, ValueError):
                readiness = 0
                safety_warning = "malformed_readiness"
        if readiness < 0 or readiness > 100:
            readiness = 0
            safety_warning = "malformed_readiness"

        raw_can_prepare = result.get("can_prepare")
        if raw_can_prepare is None:
            can_prepare = False
            if safety_warning is None:
                safety_warning = "missing_can_prepare"
        elif isinstance(raw_can_prepare, bool):
            can_prepare = raw_can_prepare
        else:
            can_prepare = False
            safety_warning = "malformed_can_prepare"

        raw_state = result.get("state")
        valid_states = {item.value for item in ReadinessState}

        if raw_state is None:
            can_prepare = False
            if safety_warning is None:
                safety_warning = "missing_state"
        elif raw_state not in valid_states:
            can_prepare = False
            if safety_warning is None:
                safety_warning = "malformed_state"

        if safety_warning == "malformed_readiness":
            can_prepare = False

        if can_prepare and raw_state != "READY":
            can_prepare = False
            safety_warning = "inconsistent_ready_state"

        if can_prepare and readiness < 90:
            can_prepare = False
            safety_warning = "insufficient_readiness"

        if can_prepare:
            state = "READY"
        elif raw_state in valid_states and raw_state != "READY":
            state = raw_state
        else:
            state = "REVIEW"

        if safety_warning is not None:
            reasons = [safety_warning]
        elif state == "NEEDS_RECORDING":
            reasons = ["new_recording_required"]
        elif state == "REVIEW":
            reasons = ["manual_review_required"]
        else:
            reasons = ["ready_for_preparation"]

        normalized = {
            "opportunity_id": opportunity_id,
            "readiness": readiness,
            "state": state,
            "can_prepare": can_prepare,
            "reasons": reasons,
        }
        if safety_warning is not None:
            normalized["safety_warning"] = safety_warning
        return normalized

    def create_run(self, opportunity_id: int) -> dict:
        analysis = self.analyze(opportunity_id)
        if not analysis.get("can_prepare") or analysis.get("state") != "READY":
            raise SafetyGateError(
                f"Opportunity {opportunity_id} cannot be prepared: {analysis.get('state')}"
            )
        response = self._request("POST", "/runs", {"opportunity_id": opportunity_id})
        return self._normalize_run_response(
            response,
            expected_opportunity_id=opportunity_id,
        )

    def record_human_decision(self, run_id: int, approved: bool) -> dict:
        response = self._request(
            "POST", f"/runs/{run_id}/approval", {"approved": approved}
        )
        return self._normalize_run_response(
            response,
            expected_run_id=run_id,
            approved=approved,
        )
