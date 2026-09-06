# Project Current State

Updated: 2026-09-06

## Mission
Ship a competition-grade RolePilot Agent for AWS Agents for Humans using the Strands Agents SDK.

## Active milestone
M0-M3 acceptance recovery, bounded M4 reliability, safe M5 live-path preparation, and M6 submission preparation on the same PR.

## Active lane
- Branch: `agent/m0-m1-strands-vertical-slice`
- PR: #2 `Build first RolePilot Strands vertical slice`
- Issues: #1 M0-M1 bootstrap/vertical slice, #3 M2 autonomous queue processing
- Keep this as the only competition implementation/recovery PR until accepted, rejected, or genuinely blocked.

## Accepted product direction
RolePilot Agent processes casting opportunities up to the final external action boundary. It may discover, analyze, prepare, persist, and request/record a human decision. It must not submit a real casting application.

The canonical competition demo must remain reproducible without Xano or paid model calls. `MemoryBackend` is the credential-free judge-safe path. Xano is an optional adapter only.

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
- `scripts/verify_release.py` provides credential-free pytest + deterministic smoke + judge-report evidence capture under ignored `release-evidence/` and is now exercised by clean CI on Python 3.12.
- Live Bedrock is explicit opt-in and requires model id + region before model construction. No AWS spend or live model invocation has been performed.
- M6 docs include architecture, judge testing, verification, submission draft and sub-five-minute demo script.

## Latest steward movement
- Commit `bf912b4c88e5119a4b58cd69916ff88dd364d316` set the CI matrix to `fail-fast: false`, so Python lanes remain independently diagnosable during recovery.
- The first real execution after infrastructure recovery exposed three stale contract tests: two expected pre-hardening exception/identity behavior and one attempted to inject an invalid string run id that the newer strict persistence gate correctly rejects.
- Commits `7c7ff365bf0320649a93e7c61c01947e93f91242` and `0ee27e07acb821d23e7e2a1fa6d6ea0a259514a8` aligned those tests without weakening the product contract.
- Commit `41b8df65986cbeae5a8fe3e0f69c72b2e5cd8a67` added the credential-free release verifier to the clean Python 3.12 CI lane.

## Exact verification state
- Exact release-candidate head before this documentation commit: `41b8df65986cbeae5a8fe3e0f69c72b2e5cd8a67`; refetch after this commit.
- GitHub Actions run `34034743018` executed real checkout, Python setup, editable install, full pytest and deterministic smoke successfully on Python 3.10 and 3.12.
- Python 3.12 additionally executed `python scripts/verify_release.py` successfully in the clean runner environment. The verifier re-ran pytest, deterministic smoke and judge-report generation and wrote `release-evidence/verification.json` plus `release-evidence/rolepilot-report.html` in the ephemeral runner.
- The direct Python 3.12 pytest stage reports 75 passed tests. The deterministic smoke proves READY preparation stops at `PENDING_HUMAN_APPROVAL`, NEEDS_RECORDING remains unprepared, REVIEW remains unprepared, and `external_submission_performed` stays false.
- Run `34034652461` also passed exact-head checkout/install/full pytest/deterministic smoke on Python 3.10 and 3.12 before the release-verifier CI addition.
- The prior zero-step/startup blocker is no longer authoritative for the competition repo; Actions is executing jobs normally again.

## Evidence still required before merge
1. Open the generated judge report and visually review desktop plus approximately 390 px mobile width. CI proves generation but does not itself prove visual quality.
2. Keep independent diff/scope/privacy/secrets review clean; generated report/release evidence must remain untracked.
3. Live Bedrock remains explicitly owner-gated and unverified until one intentionally authorized run succeeds.
4. Check final submission copy against current official Devpost fields/rules.
5. Record the final video from verified release-head behavior and keep it within the official duration limit.

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
- No public competition submission, Builder post or video publication has been performed.

## Next highest-leverage work
1. Obtain the generated judge report from a verified release candidate and visually inspect it at desktop and around 390 px mobile width.
2. Continue release-candidate privacy/secrets/diff review after every implementation movement.
3. Once Paweł intentionally supplies AWS access/model permission, verify one bounded live Strands/Bedrock queue run without creating additional paid infrastructure.
4. Continue M6 evidence capture and repository hygiene while preserving truthful claims.

## Owner-only gates
- AWS login/MFA, credentials, Bedrock model access, promotional-credit request/acceptance.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission and final hackathon submission.
