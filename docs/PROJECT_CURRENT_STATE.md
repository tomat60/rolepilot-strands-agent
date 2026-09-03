# Project Current State

Updated: 2026-09-03

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

## Current implementation
- Python project metadata added.
- MIT license added.
- Strands `Agent` orchestration added.
- Four custom product tools added.
- Deterministic safety gate added.
- Memory backend added for credential-free tests and demos.
- Xano adapter added for the Sep 3 RolePilot prototype.
- Xano readiness normalization now fails closed on malformed `can_prepare` values and contradictory READY/non-READY state.
- Regression tests cover malformed string booleans and inconsistent remote readiness state.
- Safety invariant and Xano adapter tests added.
- CI added for Python 3.10 and 3.12 plus deterministic smoke.
- Architecture documented.
- README includes install, smoke, Xano, safety, and reuse disclosure.

## Exact verification state
- Current PR head after the safety fix: `ca5653b46b15b7657911f5408472082b42c66e05`; branch is 21 commits ahead / 0 behind `main` and PR is mergeable.
- Previous exact-head CI run `33789000226` reached job records but failed before any workflow step executed: Python 3.10 concluded failure with zero steps and Python 3.12 was cancelled with zero steps.
- At the first post-fix inspection, GitHub had not instantiated a workflow run yet for `ca5653b46b15b7657911f5408472082b42c66e05`.
- This remains classified as an Actions runner/startup infrastructure failure until a job executes a real checkout/install/test step.
- The newly added fail-closed regressions are committed but not yet independently executed in CI because of that infrastructure blocker.
- Official current Strands documentation confirms Python 3.10+, `Agent`, custom `@tool` functions, and Bedrock as the default model provider, matching this implementation contract.

## Evidence still required before accepting M0-M1
- Exact-head CI executes real steps and passes on both Python versions.
- Deterministic smoke passes in CI or equivalent clean-environment evidence is obtained.
- New Xano fail-closed regression tests execute successfully.
- Independent diff/scope review remains clean.
- No private data or secrets are present.
- Merge only after the verification blocker is cleared or independently reproduced with equivalent evidence.

## Next milestone after M0-M1
M2: queue autonomy. The Strands agent should process multiple opportunities in one request, prepare all safe READY items, and surface only recording/review/human-decision blockers with persisted evidence.

## Owner-only gates later
- AWS login/MFA and Bedrock access.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission.
