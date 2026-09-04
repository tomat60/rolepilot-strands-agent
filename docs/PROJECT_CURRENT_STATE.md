# Project Current State

Updated: 2026-09-04

## Mission
Ship a competition-grade RolePilot Agent for AWS Agents for Humans using the Strands Agents SDK.

## Active milestone
M0-M1 acceptance recovery plus bounded M2 queue-autonomy slice on the same PR while GitHub Actions startup is unavailable.

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
- Five custom product tools now exist, including autonomous full-queue processing.
- Deterministic READY / NEEDS_RECORDING / REVIEW safety gate added.
- Memory backend added for credential-free tests and demos.
- Queue autonomy prepares every safe READY opportunity, persists the run, and returns only unresolved recording/review decision points; it has no external submission path.
- Queue-autonomy regression coverage proves only READY is prepared, human approval remains pending, blockers remain surfaced, and external submission remains false.
- Optional Xano adapter added for the Sep 3 RolePilot prototype.
- Xano readiness normalization fails closed on malformed `can_prepare` values and contradictory READY/non-READY state.
- Regression tests cover malformed string booleans and inconsistent remote readiness state.
- Safety invariant and Xano adapter tests added.
- CI added for Python 3.10 and 3.12 plus deterministic smoke.
- Architecture documented.
- README makes the offline MemoryBackend the canonical judge-safe path and explicitly treats Xano as optional.

## Exact verification state
- PR #2 remains the only active competition implementation lane and is mergeable.
- Previous exact head `4ecedd1c3478d01580499601282ad0694c42bd1d` produced CI run `33815222902`; both GitHub-hosted jobs had `runner_id=0` and `steps=[]`. Python 3.10 failed and Python 3.12 was cancelled before checkout.
- Queue-autonomy implementation commit `2379d5a19710ec68c8597c1492233d15dcab1aac` immediately created exact-head CI run `33823373967`, confirming Actions dispatch still occurs.
- Queue-autonomy test commit `0a2eb681a69989d0c716117b0293181c09b9811e` adds deterministic acceptance coverage for the new behavior.
- GitHub-hosted Actions startup remains classified as infrastructure failure until a job actually acquires a runner and executes workflow steps.
- Do not blind-rerun zero-step failures.

## Evidence still required before accepting M0-M1/M2 slice
- Exact-head CI executes real checkout/install/test steps and passes on both Python versions, or equivalent clean-environment evidence is obtained.
- Deterministic smoke passes in CI or equivalent clean-environment evidence is obtained.
- Queue-autonomy and Xano fail-closed regression tests execute successfully.
- Independent diff/scope review remains clean.
- No private data or secrets are present.

## Current external integration status
- Do not rely on Xano availability for the competition critical path.
- AWS/Bedrock live-model verification remains a later owner-gated M5 step.
- No AWS spend or paid resource creation is authorized.

## Next highest-leverage work after verification is available
M3 product integration: expose the real agent's queue result in a judge-friendly UX/API/CLI with visible tool trace, persisted run state, and an explicit human gate.

## Owner-only gates later
- AWS login/MFA and Bedrock access.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission.
