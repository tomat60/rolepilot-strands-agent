# Project Current State

Updated: 2026-09-06

## Mission
Ship a competition-grade RolePilot Agent for AWS Agents for Humans using the Strands Agents SDK.

## Active milestone
M6 release hardening and final submission preparation after the accepted M0-M5 vertical slice.

## Active lane
- Runtime baseline: `main`
- Accepted implementation PR: #2 `Build first RolePilot Strands vertical slice`
- PR #2 merged on 2026-09-06 as `770879c853fa0b8c90295ef837b454c3d7eb6b7a`.
- Keep further changes bounded to release evidence, live-path verification, or defects found during final submission QA.

## Accepted product direction
RolePilot Agent processes casting opportunities up to the final external action boundary. It may discover, analyze, prepare, persist, and request/record a human decision. It must not submit a real casting application.

The canonical competition demo remains reproducible without Xano or paid model calls. `MemoryBackend` is the credential-free judge-safe path. Xano is an optional adapter only.

## Current implementation
- Python 3.10+ project with MIT license and `strands-agents`.
- Strands `Agent` orchestration exposes five custom product tools, including autonomous full-queue processing.
- Deterministic READY / NEEDS_RECORDING / REVIEW safety logic remains separate from model output.
- Queue autonomy prepares only safe READY items, persists runs/audit events, isolates per-opportunity failures, and surfaces unresolved decision points.
- Analysis, persisted-run, queue-item, approval, and Xano adapter identities are treated as untrusted and must be explicit real integers; booleans, floats, strings, and other lossy aliases fail closed.
- Queue discovery and per-opportunity processing fail closed without echoing private backend exception text.
- Malformed queue items, readiness states, identifiers, and Python boolean/int aliases fail closed.
- Direct agent tool boundaries require strict integer identifiers and explicit boolean approval decisions, confirm persisted run identity after direct preparation, and confirm that decision persistence refers to the requested run.
- MemoryBackend preparation is idempotent for active runs; CHANGES_REQUESTED permits a fresh preparation run.
- Competition/demo flows contain no external submission tool; approval updates internal demo state only.
- Responsive judge HTML report is generated from the same deterministic queue/safety path and escapes backend-controlled HTML values that cross validated boundaries.
- Xano `/opportunities`, `/analyze`, `/runs`, and `/approval` are treated as untrusted boundaries. Arbitrary/private fields are discarded, remote error bodies are redacted, contradictory readiness signals fail closed, and identity/readiness must be explicitly validated with no lossy numeric coercion.
- `scripts/verify_release.py` provides credential-free pytest + deterministic smoke + judge-report evidence capture under ignored `release-evidence/` and is exercised by clean CI on Python 3.12.
- Live Bedrock is explicit opt-in and requires model id + region before model construction. No AWS spend or live model invocation has been performed.
- M6 docs include architecture, judge testing, verification, submission draft and sub-five-minute demo script.

## Accepted verification evidence
- PR #2 CI run `34040351401` validated implementation head `918cf77090d434da56314a0f4f6305f7c269d53e` through the pull-request merge ref.
- Python 3.10 and 3.12 both completed real checkout, editable dependency installation, full pytest and deterministic smoke successfully.
- Python 3.12 reported 75 passing tests and additionally executed `python scripts/verify_release.py` successfully.
- The verifier generated the judge-facing HTML report and retained it as workflow artifact `9991473987`.
- Deterministic smoke proves READY preparation stops at `PENDING_HUMAN_APPROVAL`, NEEDS_RECORDING remains unprepared, REVIEW remains unprepared, and `external_submission_performed` stays false.
- The exact CI-generated report was downloaded and directly reviewed at 1440 px desktop width and 390 px mobile width. Both layouts passed visual QA with no horizontal clipping or broken card layout; the flow, state hierarchy, human-approval boundary and zero-external-submission evidence remain legible.
- Full PR diff review found no committed credentials, tokens, private casting payloads or generated release evidence. Synthetic privacy/adversarial fixtures remain intentionally present in tests.
- Verification documentation was refreshed on `main` after merge in commit `8c7702a2a4f982f116be7f749294a0e5c56017d8`.

## Evidence still required before final submission
1. Keep final diff/scope/privacy/secrets review clean after the last release-evidence commit.
2. Live Bedrock remains explicitly owner-gated and unverified until one intentionally authorized run succeeds.
3. Check final submission copy against current official Devpost fields/rules.
4. Record the final video from verified release behavior and keep it within the official duration limit.
5. Complete AWS Builder ID and any other owner-only submission fields.

## Competition authority checked 2026-09-06
- Official Devpost submission deadline remains 2026-09-14 17:00 PDT.
- Promotional-credit requests remain due 2026-09-11 12:00 PT while supplies last.
- Project work must be newly created during the submission period except standard tools/libraries and disclosed incorporated work. The Sep 3 Xano RolePilot foundation remains explicitly disclosed.
- AgentCore is encouraged but not required.
- Current Strands documentation continues to require Python 3.10+ and support Python custom `@tool` functions; model providers remain provider-agnostic with Amazon Bedrock supported.

## Current external integration status
- Do not rely on Xano availability for the competition critical path.
- Bedrock integration is prepared but disabled by default and remains owner-gated.
- No AWS spend or paid resource creation is authorized.
- No public final competition submission, Builder post or final video publication has been performed from this repository lane.

## Next highest-leverage work
1. Verify one bounded live Strands + Bedrock queue run once Paweł intentionally supplies AWS access/model permission and approves the small model-call cost.
2. Run the final main-branch privacy/secrets/diff check after release-evidence updates settle.
3. Finalize Devpost copy and the short competition video against the verified product behavior.
4. Stop adding product scope unless final QA reveals a concrete blocker.

## Owner-only gates
- AWS login/MFA, credentials, Bedrock model access, promotional-credit request/acceptance.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission and final hackathon submission.
