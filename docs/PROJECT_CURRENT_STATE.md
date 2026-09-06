# Project Current State

Updated: 2026-09-06

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
- Analysis identity is treated as untrusted at both the shared tool/queue boundary and the Xano adapter boundary: `/analyze` must explicitly return a non-boolean numeric `opportunity_id` matching the requested opportunity. Missing, malformed, boolean-aliased, or mismatched analysis identity fails closed and cannot reach preparation.
- Queue persistence requires the returned run to explicitly contain a valid run id and the same opportunity id before preparation is reported. Missing, malformed, boolean-aliased, or mismatched persisted identity fails that lane closed to REVIEW while later opportunities continue.
- Xano `/runs` persistence requires the backend response itself to explicitly contain the expected `opportunity_id`; the adapter does not synthesize persistence identity.
- Queue discovery fails closed when the backend raises or returns a non-list response; remote/private exception text is never echoed and no preparation is attempted.
- Queue processing normalizes non-canonical backend analysis `state` to fail-closed `REVIEW`; malformed state text is not echoed into decision output or execution trace.
- Malformed queue items and opportunity identifiers, including Python boolean/int aliasing, fail closed without echoing raw backend values.
- MemoryBackend preparation is idempotent for active runs; CHANGES_REQUESTED permits a fresh preparation run.
- Competition/demo flows contain no external submission tool; approval updates internal demo state only.
- Responsive judge HTML report is generated from the same deterministic queue/safety path and escapes backend-controlled HTML values.
- Xano `/opportunities`, `/analyze`, `/runs`, and `/approval` are treated as untrusted boundaries. Arbitrary/private fields are discarded, remote error bodies are redacted, contradictory readiness signals fail closed, and analysis/run/approval identity must be explicitly confirmed.
- Regression coverage includes private-like backend fields, incomplete readiness signals, malformed/boolean IDs, queue discovery failure, analysis identity mismatch/missing identity, persisted-run identity mismatch/missing identity, explicit Xano `/analyze` identity confirmation, and Xano run/approval confirmation failures.
- `scripts/verify_release.py` provides credential-free pytest + deterministic smoke + judge-report evidence capture under ignored `release-evidence/`.
- Live Bedrock is explicit opt-in and requires model id + region before model construction. No AWS spend or live model invocation has been performed.
- M6 docs include architecture, judge testing, verification, submission draft and sub-five-minute demo script.

## Exact verification state
- Latest Xano analysis-identity hardening commits are `8924bd6618270637b60d875b535fe9e386144371` and regression commit `c269983c734c7e7d3c715da0c7e5314c1ffc4fb6`; refetch the final PR head after this documentation commit.
- Exact-head CI run `34009981696` on prior head `040659f23f25d13e456641916ca9699ab1ef9e95` failed before runner execution: both Python jobs had `runner_id=0` and `steps=[]`. Do not treat it as product verification.
- A fresh clean-clone workaround was attempted again on 2026-09-06, but local execution could not reach GitHub because DNS resolution for `github.com` failed before checkout. This is infrastructure evidence only, not product verification.
- The latest Xano analysis-identity hardening and its regression are source-reviewed but have no successful clean-environment execution evidence yet. Do not infer success from source review or mergeability.
- Do not blind-rerun zero-step Actions failures.

## Evidence still required before merge
1. Exact-head CI executes real checkout/install/test steps and passes on Python 3.10 and 3.12, or equivalent clean-environment evidence is obtained.
2. Run `python scripts/verify_release.py` from a clean installed environment and preserve the ignored evidence for review.
3. Open the generated judge report and visually review desktop plus approximately 390 px mobile width.
4. Keep independent diff/scope/privacy/secrets review clean; generated report/release evidence must remain untracked.
5. Live Bedrock remains explicitly owner-gated and unverified until one intentionally authorized run succeeds.
6. Check final submission copy against current official Devpost fields/rules.
7. Record the final video from verified release-head behavior and keep it within the official duration limit.

## Competition authority checked 2026-09-06
- Official Devpost submission deadline remains 2026-09-14 17:00 PDT.
- Promotional-credit requests remain due 2026-09-11 12:00 PT while supplies last.
- Project work must be newly created during the submission period except standard tools/libraries and disclosed incorporated work. The Sep 3 Xano RolePilot foundation remains explicitly disclosed.
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
