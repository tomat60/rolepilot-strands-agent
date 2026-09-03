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
Not opened yet.

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
- Safety invariant tests added.
- CI added for Python 3.10 and 3.12 plus deterministic smoke.
- Architecture documented.

## Evidence still required before accepting M0-M1
- Open PR and inspect exact changed scope.
- Exact-head CI passes on both Python versions.
- Deterministic smoke passes in CI.
- Review README/install instructions against actual implementation.
- Verify no private data or secrets are present.
- Merge only after independent scope review.

## Next milestone after M0-M1
M2: queue autonomy. The Strands agent should process multiple opportunities in one request, prepare all safe READY items, and surface only recording/review/human-decision blockers with persisted evidence.

## Owner-only gates later
- AWS login/MFA and Bedrock access.
- Any AWS spend or resource creation.
- AWS Builder ID.
- Public video/blog/Devpost submission.
