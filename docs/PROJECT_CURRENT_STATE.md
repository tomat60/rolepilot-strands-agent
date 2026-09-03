# Project Current State

Updated: 2026-09-04

## Mission
Ship a competition-grade RolePilot Agent for AWS Agents for Humans using the Strands Agents SDK.

## Active milestone
M0-M1: repository bootstrap plus first Strands vertical slice.

## Active issue
#1 `M0-M1: bootstrap repo and ship first Strands vertical slice`

## Active implementation branch
`agent/m0-m1-strands-vertical-slice`

## Active implementation PR
#2 `Build first RolePilot Strands vertical slice`

## Accepted product direction
RolePilot Agent processes casting opportunities up to the final external action boundary. It may analyze, prepare, persist, and request human approval. It must not submit a real casting application.

The competition demo must remain reproducible without Xano. The in-memory backend is the canonical judge-safe path. Xano is an optional adapter only and must never become a required runtime dependency.

## Current implementation
- Python project metadata added.
- MIT license added.
- Strands `Agent` orchestration added.
- Four custom product tools added.
- Deterministic safety gate added.
- Memory backend added for credential-free tests and demos.
- Optional Xano adapter added for the Sep 3 RolePilot prototype.
- Xano readiness normalization fails closed on malformed `can_prepare` values and contradictory READY/non-READY state.
- Regression tests cover malformed string booleans and inconsistent remote readiness state.
- Safety invariant and Xano adapter tests added.
- CI added for Python 3.10 and 3.12 plus deterministic smoke.
- Architecture documented.
- README now makes the offline MemoryBackend the canonical judge-safe path and explicitly treats Xano as optional.

## Exact verification state
- PR #2 remains the only active competition implementation lane.
- Before this current-state update, the exact head was `c8e0d456e6b220c9a0547ee56e889355e925037f`, 23 commits ahead / 0 behind `main`.
- Exact-head CI run `33815188406` instantiated two job records but neither job executed a single workflow step. Python 3.10 concluded failure with `steps=[]`, `runner_id=0`; Python 3.12 concluded cancelled with `steps=[]`, `runner_id=0`.
- This is classified as GitHub-hosted Actions startup/infrastructure failure, not a demonstrated product/test failure.
- A clean-environment clone/test attempt from the steward runtime was also unavailable because that runtime could not resolve github.com, so it does not provide equivalent independent verification.
- The fail-closed Xano regressions remain committed but are not yet accepted as CI-verified.

## Evidence still required before accepting M0-M1
- Exact-head CI executes real checkout/install/test steps and passes on both Python versions, or equivalent clean-environment evidence is obtained.
- Deterministic smoke passes in CI or equivalent clean-environment evidence is obtained.
- New Xano fail-closed regression tests execute successfully.
- Independent diff/scope review remains clean.
- No private data or secrets are present.

## Current external integration status
- Do not rely on Xano availability for the competition critical path.
- AWS/Bedrock live-model verification remains a later owner-gated M5 step.
- No AWS spend or paid resource creation is authorized.

## Next milestone after M0-M1
M2: queue autonomy. The Strands agent should process multiple opportunities in one request, prepare all safe READY items, and surface only recording/review/human-decision blockers with persisted evidence.

## Owner-only gates later
- AWS login/MFA and Bedrock access.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission.
