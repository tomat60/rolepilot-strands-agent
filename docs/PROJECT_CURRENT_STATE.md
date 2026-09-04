# Project Current State

Updated: 2026-09-04

## Mission
Ship a competition-grade RolePilot Agent for AWS Agents for Humans using the Strands Agents SDK.

## Active milestone
M0-M1 acceptance recovery plus bounded M2/M3 progress on the same PR while GitHub Actions startup is unavailable.

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
- Python project metadata and MIT license added.
- Strands `Agent` orchestration added.
- Five custom product tools exist, including autonomous full-queue processing.
- Deterministic READY / NEEDS_RECORDING / REVIEW safety gate added.
- Memory backend added for credential-free tests and demos.
- Queue autonomy prepares every safe READY opportunity, persists the run, and returns only unresolved recording/review decision points; it has no external submission path.
- Queue-autonomy regression coverage proves only READY is prepared, human approval remains pending, blockers remain surfaced, and external submission remains false.
- Optional Xano adapter added for the Sep 3 RolePilot prototype.
- Xano readiness normalization fails closed on malformed `can_prepare` values and contradictory READY/non-READY state.
- Safety invariant and Xano adapter regression tests added.
- CI added for Python 3.10 and 3.12 plus deterministic smoke.
- Architecture documented.
- README makes the offline MemoryBackend the canonical judge-safe path and explicitly treats Xano as optional.
- M3 judge-facing product report added: a self-contained responsive HTML view generated from the same deterministic queue/safety path. It shows prepared work, persisted run/audit state, NEEDS_RECORDING/REVIEW decision points, the human approval gate and zero external submissions.
- CLI supports `--judge-report PATH` so judges can generate the product view without credentials, AWS, Xano or paid model calls.
- Regression coverage asserts the judge report exposes the correct 1 prepared / 2 decision / 0 submission state and preserves the human gate.
- Independent contract review found a TEST_BUG: M2 and judge-report tests expected `PENDING`, while the domain/backend contract intentionally persists the explicit `PENDING_HUMAN_APPROVAL` state. Tests were corrected to the product contract; the product state was not weakened or renamed to satisfy tests.

## Exact verification state
- PR #2 remains the only active competition implementation lane.
- Exact head `d0b5e3de4d2af3da448daa49fbbc6abd42b9efe5` produced CI run `33823405767`, which completed failure before test execution; prior runs repeatedly showed `runner_id=0` and `steps=[]` before checkout.
- GitHub-hosted Actions startup remains classified as infrastructure failure until a job actually acquires a runner and executes workflow steps.
- A container clean-check attempt could not clone GitHub because that runtime has no DNS/network access; this is not product evidence and does not satisfy acceptance.
- M3 judge-report and approval-state test-correction commits were added after the last executed head; final exact-head CI state must be refetched.
- Do not blind-rerun zero-step failures.

## Evidence still required before accepting M0-M3 slice
- Exact-head CI executes real checkout/install/test steps and passes on both Python versions, or equivalent clean-environment evidence is obtained.
- Deterministic smoke passes in CI or equivalent clean-environment evidence is obtained.
- Queue-autonomy, Xano fail-closed and judge-report regression tests execute successfully.
- Generated HTML report is opened and visually reviewed at desktop and mobile width.
- Independent diff/scope review remains clean.
- No private data or secrets are present.

## Current external integration status
- Do not rely on Xano availability for the competition critical path.
- AWS/Bedrock live-model verification remains a later owner-gated M5 step.
- No AWS spend or paid resource creation is authorized.

## Next highest-leverage work
1. Obtain executed clean-environment verification for M0-M3 as soon as infrastructure permits.
2. Visually inspect the generated judge report and tighten mobile hierarchy if needed.
3. Then move to M4 reliability/evaluation or M5 Bedrock live path depending on owner AWS readiness.

## Owner-only gates later
- AWS login/MFA and Bedrock access.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission.
