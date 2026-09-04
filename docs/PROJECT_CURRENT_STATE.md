# Project Current State

Updated: 2026-09-04

## Mission
Ship a competition-grade RolePilot Agent for AWS Agents for Humans using the Strands Agents SDK.

## Active milestone
M0-M3 acceptance recovery, bounded M4 reliability, safe M5 live-path preparation, and M6 submission preparation on the same PR while GitHub Actions startup is unavailable.

## Active issue
#1 `M0-M1: bootstrap repo and ship first Strands vertical slice`

## Active implementation branch
`agent/m0-m1-strands-vertical-slice`

## Active implementation PR
#2 `Build first RolePilot Strands vertical slice`

## Accepted product direction
RolePilot Agent processes casting opportunities up to the final external action boundary. It may analyze, prepare, persist, and request human approval. It must not submit a real casting application.

The competition demo must remain reproducible without Xano or paid model calls. The in-memory backend is the canonical judge-safe path. Xano is an optional adapter only and must never become a required runtime dependency.

## Current implementation
- Python project metadata and MIT license added.
- Strands `Agent` orchestration added.
- Five custom product tools exist, including autonomous full-queue processing.
- Deterministic READY / NEEDS_RECORDING / REVIEW safety gate added.
- Memory backend added for credential-free tests and demos.
- Queue autonomy prepares every safe READY opportunity, persists the run, and returns only unresolved recording/review decision points; it has no external submission path.
- Queue-autonomy regression coverage proves only READY is prepared, human approval remains pending, blockers remain surfaced, and external submission remains false.
- Queue processing isolates per-opportunity backend/normalization/persistence failures: the affected lane fails closed to `REVIEW`, only the exception class is surfaced, and the remaining queue continues.
- Regression coverage exercises both analysis failure and prepare/persistence failure, proves no private exception message leaks, and preserves zero external submissions.
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
- M4 deterministic readiness matrix coverage exercises READY, new-recording, manual-review, missing/unapproved asset, combined blocker, and blocker-precedence scenarios. Every non-READY path is asserted fail-closed through `require_preparable`.
- M5 preparation includes an explicit Bedrock live-model cost/configuration gate. The normal CLI will not invoke a model unless `--live-bedrock` is supplied.
- Live Bedrock mode additionally requires an explicit `ROLEPILOT_BEDROCK_MODEL_ID` and region (`ROLEPILOT_BEDROCK_REGION`, `AWS_REGION`, or `AWS_DEFAULT_REGION`) before constructing the Strands `BedrockModel`.
- Bedrock configuration parsing is network-free and has deterministic regression coverage for missing and valid configuration.
- No AWS resource creation, model-access enablement, quota change, credential storage, or live model call was performed by this slice.
- M6 preparation now includes `docs/SUBMISSION_DRAFT.md` with the project story, technical implementation, safety invariants, impact, reuse disclosure, judge run path, truthful verification boundaries, and final submission checklist.
- M6 preparation now includes `docs/DEMO_SCRIPT.md`, a target 4:15-4:40 end-to-end video plan focused on product behavior first, Strands depth second, safety evidence, mobile/desktop product UX, and a strict rule not to present Bedrock as live unless an exact live run has actually been verified.

## Exact verification state
- PR #2 remains the only active competition implementation lane.
- Exact head `b9ddd90a07f8aa589dd02f99302ae98db8fca326` produced CI run `33838342064`; both matrix jobs had `runner_id=0`, `steps=[]`, and ended before checkout, so this remains an infrastructure startup failure rather than executed product/test evidence.
- Submission-draft commit `e4b14c7486ac22183be73643810517371acc9fde` produced exact-head CI run `33842045281`, which also completed as failure before usable verification could be obtained.
- After adding the demo script the branch remained 46 commits ahead and 0 behind `main`. A transient PR mergeability read returned false immediately after the content update even though the compare endpoint showed the branch strictly ahead of the unchanged merge base; refetch is required before treating this as a conflict.
- A fresh container clean-check on 2026-09-04 previously failed before clone because the runtime could not resolve `github.com`; this does not satisfy acceptance and is not product failure evidence.
- GitHub-hosted Actions startup remains unverified until a job acquires a runner and executes workflow steps.
- Do not blind-rerun zero-step failures.

## Evidence still required before accepting the current slice
- Exact-head CI executes real checkout/install/test steps and passes on both Python versions, or equivalent clean-environment evidence is obtained.
- Deterministic smoke passes in CI or equivalent clean-environment evidence is obtained.
- Queue-autonomy, failure-isolation, Xano fail-closed, judge-report, approval-state, readiness-matrix, and Bedrock-gate regression tests execute successfully.
- Generated HTML report is opened and visually reviewed at desktop and mobile width.
- Independent diff/scope review remains clean.
- No private data or secrets are present.
- M5 live Bedrock invocation remains explicitly owner-gated and unverified until AWS credentials/model access are intentionally supplied.
- M6 submission copy must be checked against the final current Devpost fields and official rules before public submission.
- Final video must be recorded from verified release-head behavior and remain within the current official duration limit.

## Current external integration status
- Do not rely on Xano availability for the competition critical path.
- Bedrock integration is prepared but live invocation is disabled by default and remains owner-gated.
- No AWS spend or paid resource creation is authorized.
- No public competition submission, Builder post, or video publication has been performed.

## Next highest-leverage work
1. Obtain executed clean-environment verification as soon as infrastructure permits.
2. Generate and visually inspect the judge report at desktop and around 390 px mobile width; tighten hierarchy if needed.
3. Once Paweł intentionally supplies AWS access/model permission, verify one bounded live Strands/Bedrock queue run without creating additional paid infrastructure.
4. Continue M6 evidence capture and final repository hygiene while preserving truthful submission claims.

## Owner-only gates later
- AWS login/MFA, credentials, and Bedrock model access.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission.
