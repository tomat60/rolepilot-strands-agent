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
- Strands `Agent` orchestration with five custom product tools exists, including autonomous full-queue processing.
- Deterministic READY / NEEDS_RECORDING / REVIEW safety gate is independent of model output.
- MemoryBackend is the credential-free judge-safe path; Xano is optional and fails closed on malformed or contradictory readiness state.
- Queue autonomy prepares only safe READY opportunities, persists runs/audit events, isolates per-opportunity failures, and returns unresolved recording/review decision points.
- Competition/demo flows contain no external submission tool; human approval changes internal demo state only.
- M3 judge-facing responsive HTML report is generated from the same deterministic queue/safety path and exposes Discover -> Inspect -> Decide -> Prepare -> Stop, prepared work, decision inbox, approval boundary and zero external submissions.
- Judge report now escapes backend-controlled run id, approval state and audit-event values before HTML rendering. A regression injects HTML/script payloads and asserts they are encoded rather than executable.
- M4 readiness matrix covers READY, recording-required, manual-review, missing/unapproved asset, combined blocker and blocker precedence, with fail-closed `require_preparable` assertions.
- M5 has explicit `--live-bedrock` opt-in plus required model id and region before constructing `BedrockModel`; no live AWS call or paid resource creation has been performed.
- M6 includes `docs/SUBMISSION_DRAFT.md` and `docs/DEMO_SCRIPT.md`; the video plan stays under five minutes and must not claim live Bedrock until verified.

## Exact verification state
- PR #2 remains the only active competition implementation lane.
- Current branch head after the judge-report security hardening is `c69e8e5f86c0787657dcb9f8b8f8eba9995d0211` before this state-only checkpoint commit.
- At inspection time GitHub had created no Actions run yet for that exact head.
- Earlier exact-head runs repeatedly failed before runner assignment with `runner_id=0` and `steps=[]`; this remains infrastructure startup failure evidence, not executed product/test evidence.
- Do not blind-rerun zero-step failures.

## Evidence still required before accepting the current slice
- Exact-head CI executes real checkout/install/test steps and passes on Python 3.10 and 3.12, or equivalent clean-environment evidence is obtained.
- Deterministic smoke and all regressions, including judge-report escaping, execute successfully.
- Generated HTML report is opened and visually reviewed at desktop and around 390 px mobile width.
- Independent diff/scope/privacy/secrets review remains clean.
- M5 live Bedrock invocation remains explicitly owner-gated and unverified until AWS credentials/model access are intentionally supplied.
- M6 submission copy must be checked against final current Devpost fields and official rules before public submission.
- Final video must be recorded from verified release-head behavior and remain within the official duration limit.

## Current competition authority checked 2026-09-04
- Official Devpost deadline remains 2026-09-14 17:00 PDT.
- Promotional-credit requests remain due 2026-09-11 12:00 PT while supplies last.
- Official rules allow standard tools/libraries but require disclosure of other pre-existing work incorporated into the project.
- Current official Strands documentation continues to support Python custom `@tool` functions and BedrockModel.

## Current external integration status
- Do not rely on Xano availability for the competition critical path.
- Bedrock integration is prepared but disabled by default and remains owner-gated.
- No AWS spend or paid resource creation is authorized.
- No public competition submission, Builder post, or video publication has been performed.

## Next highest-leverage work
1. Obtain executed clean-environment verification as soon as infrastructure permits.
2. Generate and visually inspect the judge report at desktop and around 390 px mobile width.
3. Complete independent privacy/secrets/diff review on the release candidate.
4. Once Paweł intentionally supplies AWS access/model permission, verify one bounded live Strands/Bedrock queue run without creating additional paid infrastructure.
5. Continue M6 evidence capture and repository hygiene while preserving truthful claims.

## Owner-only gates later
- AWS login/MFA, credentials, Bedrock model access, promotional-credit request/acceptance.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission.
