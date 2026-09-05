# Project Current State

Updated: 2026-09-05

## Mission
Ship a competition-grade RolePilot Agent for AWS Agents for Humans using the Strands Agents SDK.

## Active milestone
M0-M3 acceptance recovery, bounded M4 reliability, safe M5 live-path preparation, and M6 submission preparation on the same PR while GitHub Actions startup is unavailable.

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
- Queue processing now also normalizes any non-canonical backend analysis `state` to fail-closed `REVIEW`; malformed state text is not echoed into decision output or execution trace. Regression coverage uses a private-like malformed value and requires it not to escape.
- Malformed opportunity identifiers fail closed without echoing raw backend values.
- MemoryBackend preparation is idempotent for active runs; CHANGES_REQUESTED permits a fresh preparation run.
- Competition/demo flows contain no external submission tool; approval updates internal demo state only.
- Responsive judge HTML report is generated from the same deterministic queue/safety path and escapes backend-controlled HTML values.
- Optional Xano errors and malformed readiness/can-prepare combinations fail closed and redact remote error bodies.
- `scripts/verify_release.py` provides credential-free pytest + deterministic smoke + judge-report evidence capture under ignored `release-evidence/`.
- Live Bedrock is explicit opt-in and requires model id + region before model construction. No AWS spend or live model invocation has been performed.
- M6 docs include architecture, judge testing, verification, submission draft and sub-five-minute demo script.

## Exact verification state
- Before the latest reliability hardening, PR #2 exact head was `e57e07ac053074e9fcf72d20064241edf4915051`, open, non-draft and mergeable.
- Latest reliability commits add fail-closed queue analysis-state normalization and its regression; exact implementation head immediately before this checkpoint commit is `6ae7a94b1e71f46f10e5a11c26c98d1de3ecb146`.
- Exact-head CI run `33959067040` on `6ae7a94b1e71f46f10e5a11c26c98d1de3ecb146` completed before any executable step: Python 3.12 failed and Python 3.10 was cancelled with no job steps. This is infrastructure startup failure, not product/test evidence.
- A fresh independent clean clone on 2026-09-05 again failed before checkout because the execution environment could not resolve `github.com`. This is not product/test evidence.
- No successful clean-environment execution evidence exists yet for the latest reliability commits. Do not infer success from mergeability or source review.
- Refetch exact PR head, mergeability and exact-head CI after this checkpoint commit.
- Do not blind-rerun zero-step Actions failures.

## Evidence still required before merge
1. Exact-head CI executes real checkout/install/test steps and passes on Python 3.10 and 3.12, or equivalent clean-environment evidence is obtained.
2. Run `python scripts/verify_release.py` from a clean installed environment and preserve the ignored evidence for review.
3. Open the generated judge report and visually review desktop plus approximately 390 px mobile width.
4. Keep independent diff/scope/privacy/secrets review clean; generated report/release evidence must remain untracked.
5. Live Bedrock remains explicitly owner-gated and unverified until one intentionally authorized run succeeds.
6. Check final submission copy against current official Devpost fields/rules.
7. Record the final video from verified release-head behavior and keep it within the official duration limit.

## Competition authority checked 2026-09-05
- Official Devpost submission deadline remains 2026-09-14 17:00 PDT.
- Promotional-credit requests remain due 2026-09-11 12:00 PT while supplies last.
- Project work must be newly created during the submission period except standard tools/libraries and disclosed pre-existing incorporated work. The Sep 3 Xano RolePilot foundation remains explicitly disclosed.
- AgentCore is encouraged but not required.
- Current Strands documentation continues to support Python custom `@tool` functions and agent tool use.

## Current external integration status
- Do not rely on Xano availability for the competition critical path.
- Bedrock integration is prepared but disabled by default and remains owner-gated.
- No AWS spend or paid resource creation is authorized.
- No public competition submission, Builder post or video publication has been performed.

## Next highest-leverage work
1. Obtain executed clean-environment verification as soon as infrastructure permits, preferably through `scripts/verify_release.py`.
2. Generate and visually inspect the judge report at desktop and around 390 px mobile width.
3. Continue release-candidate privacy/secrets/diff review after every implementation movement.
4. Once Paweł intentionally supplies AWS access/model permission, verify one bounded live Strands/Bedrock queue run without creating additional paid infrastructure.
5. Continue M6 evidence capture and repository hygiene while preserving truthful claims.

## Owner-only gates
- AWS login/MFA, credentials, Bedrock model access, promotional-credit request/acceptance.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission and final hackathon submission.
