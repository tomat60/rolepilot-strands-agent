# Project Current State

Updated: 2026-09-05

## Mission
Ship a competition-grade RolePilot Agent for AWS Agents for Humans using the Strands Agents SDK.

## Active milestone
M0-M3 acceptance recovery, bounded M4 reliability, safe M5 live-path preparation, and M6 submission preparation on the same PR while GitHub Actions startup is unavailable.

## Active issues
#1 `M0-M1: bootstrap repo and ship first Strands vertical slice`
#3 `M2: autonomous queue processing and decision surfacing`

## Active implementation branch
`agent/m0-m1-strands-vertical-slice`

## Active implementation PR
#2 `Build first RolePilot Strands vertical slice`

## Accepted product direction
RolePilot Agent processes casting opportunities up to the final external action boundary. It may analyze, prepare, persist, and request human approval. It must not submit a real casting application.

The competition demo must remain reproducible without Xano or paid model calls. The in-memory backend is the canonical judge-safe path. Xano is an optional adapter only and must never become a required runtime dependency.

## Current implementation
- Python project metadata and MIT license added.
- Strands `Agent` orchestration with five custom product tools exists, including autonomous full-queue processing.
- Deterministic READY / NEEDS_RECORDING / REVIEW safety gate is independent of model output.
- MemoryBackend is the credential-free judge-safe path; Xano is optional and fails closed on malformed or contradictory readiness state.
- Queue autonomy prepares only safe READY opportunities, persists runs/audit events, isolates per-opportunity failures, and returns unresolved recording/review decision points.
- Queue processing returns a deterministic execution trace covering opportunity discovery, per-opportunity analysis, safe preparation, and human-decision stops. Failure trace entries expose only exception classes, never private backend exception text.
- MemoryBackend preparation is idempotent for active runs: rerunning the queue reuses the existing PENDING_HUMAN_APPROVAL or APPROVED_DEMO_STATE run instead of creating duplicates. A CHANGES_REQUESTED run permits a fresh preparation run.
- Competition/demo flows contain no external submission tool; human approval changes internal demo state only.
- M3 judge-facing responsive HTML report is generated from the same deterministic queue/safety path and exposes Discover -> Inspect -> Decide -> Prepare -> Stop, prepared work, decision inbox, approval boundary and zero external submissions.
- Judge report escapes backend-controlled run id, approval state and audit-event values before HTML rendering.
- Generated judge-report artifact names are ignored by Git and README warns that reports from external/private backends may contain private opportunity/audit data and must not be committed.
- Optional Xano HTTP failures are privacy-redacted at the adapter boundary: remote error bodies are no longer propagated into public-facing exception text, with a regression asserting private body content is absent.
- M4 readiness matrix covers READY, recording-required, manual-review, missing/unapproved asset, combined blocker and blocker precedence, with fail-closed `require_preparable` assertions.
- M4/M6 include `scripts/verify_release.py`, a credential-free release verifier that runs pytest, deterministic smoke and judge-report generation and records exact SHA/Python/command evidence in an ignored `release-evidence/` directory. Manual desktop/mobile visual review and live Bedrock remain explicitly pending instead of being auto-claimed.
- M5 has explicit `--live-bedrock` opt-in plus required model id and region before constructing `BedrockModel`; no live AWS call or paid resource creation has been performed.
- M6 includes `docs/SUBMISSION_DRAFT.md`, `docs/DEMO_SCRIPT.md`, `docs/VERIFICATION.md`, and `docs/JUDGE_TESTING.md`. The judge-testing guide provides an English, free, credential-free install/test path, expected observable behavior, safety expectations, and optional-integration boundaries required for judging/testing. README links directly to it.

## Exact verification state
- PR #2 remains the only active competition implementation lane.
- Exact PR head before this checkpoint commit is `d9243eb2f1ab836f07b4a95d652a3969b2778746`; PR is open, non-draft and mergeable.
- Exact-head Actions run `33913623494` completed as failure before any workflow step executed. Both Python 3.10 and 3.12 jobs have `runner_id=0` and `steps=[]`; this is infrastructure startup failure, not product/test evidence.
- A fresh independent clone attempt against exact head `d9243eb2f1ab836f07b4a95d652a3969b2778746` on 2026-09-05 also could not begin because the execution environment could not resolve `github.com`. This is not product/test evidence and must not be represented as verification.
- Treat zero-step Actions failures and DNS bootstrap failure as infrastructure conditions. Do not blind-rerun them.
- Refetch exact-head CI after this checkpoint commit before accepting any slice.

## Evidence still required before accepting the current slice
- Exact-head CI executes real checkout/install/test steps and passes on Python 3.10 and 3.12, or equivalent clean-environment evidence is obtained.
- Run `python scripts/verify_release.py` from a clean installed environment and preserve its untracked evidence for review.
- Generated HTML report is opened and visually reviewed at desktop and around 390 px mobile width.
- Independent diff/scope/privacy/secrets review remains clean. Generated report and release-evidence artifacts must remain untracked.
- M5 live Bedrock invocation remains explicitly owner-gated and unverified until AWS credentials/model access are intentionally supplied.
- M6 submission copy must be checked against final current Devpost fields and official rules before public submission.
- Final video must be recorded from verified release-head behavior and remain within the official duration limit.

## Current competition authority checked 2026-09-05
- Official Devpost deadline remains 2026-09-14 17:00 PDT.
- Promotional-credit requests remain due 2026-09-11 12:00 PT while supplies last.
- Official submission requirements require a public repository with MIT/Apache license, README, architecture diagram, English submission materials, a public YouTube/Vimeo video of at most five minutes, AWS Builder ID, and free access to a working project/test build through the judging period ending 2026-10-08 17:00 PDT. A live demo link is optional but can strengthen Technical Implementation.
- Official rules allow standard tools/libraries but require disclosure of other pre-existing work incorporated into the project.
- Current official Strands documentation continues to support Python custom `@tool` functions and agent-selected tools.

## Current external integration status
- Do not rely on Xano availability for the competition critical path.
- Bedrock integration is prepared but disabled by default and remains owner-gated.
- No AWS spend or paid resource creation is authorized.
- No public competition submission, Builder post, or video publication has been performed.

## Next highest-leverage work
1. Obtain executed clean-environment verification as soon as infrastructure permits, preferably through `scripts/verify_release.py` so evidence is repeatable.
2. Generate and visually inspect the judge report at desktop and around 390 px mobile width.
3. Continue release-candidate privacy/secrets/diff review after every implementation movement.
4. Confirm Xano idempotency only if that optional backend becomes available; the canonical MemoryBackend path meets issue #3 dedupe acceptance.
5. Once Paweł intentionally supplies AWS access/model permission, verify one bounded live Strands/Bedrock queue run without creating additional paid infrastructure.
6. Continue M6 evidence capture and repository hygiene while preserving truthful claims.

## Owner-only gates later
- AWS login/MFA, credentials, Bedrock model access, promotional-credit request/acceptance.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission.
