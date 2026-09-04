# Release Verification Evidence

This document is the release-candidate evidence checklist for the Agents for Humans submission. It separates implemented behavior from behavior that has actually been executed and observed.

## Rule

Do not call an item verified because code exists, a workflow was created, or a check suite was scheduled. Verification requires executed evidence from the exact release head or a documented equivalent clean environment.

## Credential-free release gate

From a clean Python 3.10+ environment at the exact candidate commit:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
pytest
rolepilot-agent --deterministic-smoke
rolepilot-agent --judge-report rolepilot-report.html
```

Record:

- exact commit SHA;
- Python version;
- dependency install result;
- pytest result and test count;
- deterministic smoke result;
- judge report path;
- desktop visual review result;
- approximately 390 px mobile visual review result.

## Safety evidence required

The release candidate must demonstrate that:

- READY work may be prepared but stops at `PENDING_HUMAN_APPROVAL`;
- NEEDS_RECORDING cannot cross the preparation gate;
- REVIEW cannot cross the preparation gate;
- missing or unapproved assets fail closed;
- contradictory or malformed backend readiness fails closed;
- one opportunity failure does not abort the rest of the queue;
- rerunning an active prepared opportunity does not create a duplicate run;
- `CHANGES_REQUESTED` permits a fresh preparation run;
- judge-report backend values are HTML escaped;
- demo approval changes internal state only;
- external submission remains impossible because no submission tool exists.

## Public-repository hygiene gate

Before the final submission commit:

- inspect the complete changed-file list;
- inspect the final diff for credentials, tokens, URLs containing secrets, private casting data, private names or real application content;
- confirm generated `rolepilot-report*.html` artifacts are not tracked;
- confirm the MIT license, README, architecture documentation and Xano reuse disclosure are visible;
- confirm every public claim matches observed behavior.

## Live Bedrock gate

Live Bedrock is a separate owner-authorized verification step. It is not required to run the credential-free judge path and must not run automatically.

When AWS access, model access and cost approval are intentionally available, record:

- exact release candidate SHA;
- configured model ID and region, without recording credentials;
- bounded prompt used for the queue run;
- successful Strands agent invocation and meaningful custom-tool activity;
- confirmation that the deterministic safety gate still prevented external submission;
- approximate AWS usage/cost if available.

Until this succeeds, public copy must describe Bedrock as an implemented, explicitly gated live path rather than a verified live deployment.

## Current evidence status

As of 2026-09-04, implementation review confirms the release gates exist in source and tests, but the latest exact-head GitHub Actions attempt for PR #2 failed before runner assignment with zero executed steps. Therefore CI is not test evidence. Clean-environment execution, deterministic smoke, visual report review and live Bedrock verification remain outstanding.
