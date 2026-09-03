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

    def create_run(self, opportunity_id: int) -> dict:
        result = self._analysis(opportunity_id)
        require_preparable(result)
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
            body = exc.read().decode("utf-8", errors="replace")
            raise RuntimeError(f"Xano returned HTTP {exc.code}: {body}") from exc

    def list_opportunities(self) -> list[dict]:
        return self._request("GET", "/opportunities")

    def analyze(self, opportunity_id: int) -> dict:
        result = self._request("POST", "/analyze", {"opportunity_id": opportunity_id})
        readiness = int(result.get("readiness", 0))
        can_prepare = bool(result.get("can_prepare", readiness >= 90))
        if not can_prepare:
            state = result.get("state", "REVIEW")
            if state not in {item.value for item in ReadinessState}:
                state = "REVIEW"
            result["state"] = state
        else:
            result["state"] = "READY"
        result["can_prepare"] = can_prepare
        return result

    def create_run(self, opportunity_id: int) -> dict:
        analysis = self.analyze(opportunity_id)
        if not analysis.get("can_prepare") or analysis.get("state") != "READY":
            raise SafetyGateError(
                f"Opportunity {opportunity_id} cannot be prepared: {analysis.get('state')}"
            )
        return self._request("POST", "/runs", {"opportunity_id": opportunity_id})

    def record_human_decision(self, run_id: int, approved: bool) -> dict:
        result = self._request(
            "POST", f"/runs/{run_id}/approval", {"approved": approved}
        )
        result["external_submission_performed"] = False
        return result
