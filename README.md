# RolePilot Agent

**Safe delegation for casting applications, built with the Strands Agents SDK.**

RolePilot Agent is an autonomous professional-workflow agent for actors and talent teams. It processes casting opportunities, checks whether approved materials are sufficient, prepares safe application state when possible, surfaces only the decisions that need a person, and stops before any real external submission.

This repository is the competition-specific Strands implementation for the AWS **Agents for Humans** hackathon.

## Product principle

Automate preparation. Keep authority human.

The agent may inspect opportunities, analyze readiness, prepare an application run, persist an audit trail, and record a human decision. It must not submit a real casting application. Consequential external action remains outside the demo boundary.

## What is implemented

- Python 3.10+ project using `strands-agents`
- Strands `Agent` orchestration with four custom product tools
- deterministic safety gate independent of model output
- competition-safe in-memory backend for tests and offline smoke runs
- optional Xano adapter for the RolePilot prototype created on 2026-09-03
- READY, NEEDS_RECORDING, and REVIEW scenarios
- persisted demo application runs and audit events
- explicit human approval state with no external submission tool
- CI for Python 3.10 and 3.12

## Architecture

`User goal -> Strands Agent -> custom tools -> deterministic safety gate -> backend -> persisted run -> human approval`

The Strands agent decides which tools to call. Deterministic product rules separately enforce whether preparation is allowed. See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for the full diagram.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
```

Run all tests:

```bash
pytest
```

Run the deterministic competition-safe smoke test without AWS credentials, Xano, or model calls:

```bash
rolepilot-agent --deterministic-smoke
```

The in-memory backend is the canonical judge-safe path and requires no external service. This keeps the competition demo reproducible even when optional integrations are unavailable.

Run the real Strands agent with the default Strands model provider:

```bash
rolepilot-agent "Process my casting opportunity queue."
```

The Strands Python SDK uses Amazon Bedrock by default. A live invocation therefore requires suitable AWS credentials and model access. The deterministic test suite and smoke path do not.

## Optional Xano integration

The Sep 3 RolePilot Xano prototype is an optional integration, not a runtime dependency. If a compatible Xano API is available, set the API group base URL:

```bash
export ROLEPILOT_XANO_BASE_URL="https://YOUR_INSTANCE.xano.io/api:rolepilot"
rolepilot-agent --backend xano --deterministic-smoke
```

The adapter uses `/opportunities`, `/analyze`, `/runs`, and `/runs/{id}/approval`. Its normalization fails closed: malformed or contradictory readiness responses cannot be promoted to READY. If Xano is unavailable, use the default memory backend; the agent, safety gate, tests, and competition demo remain fully usable.

## Safety boundary

This repository intentionally contains **no tool that performs a final external casting submission**.

A demo approval can update internal run state only. Tests assert that external submission remains false even after approval.

## Relationship to the Xano RolePilot prototype

A separate RolePilot/Xano prototype was created on 2026-09-03 during the competition period before this repository was opened. This project may use that prototype as an optional backend/service foundation. The Strands agent orchestration, agent tools, deterministic safety layer, tests, competition integration, and submission-specific product work are being built in this repository. Reused work is disclosed rather than presented as newly created here.

## Official Strands references

- Python quickstart: https://strandsagents.com/docs/user-guide/quickstart/python/
- Custom tools: https://strandsagents.com/docs/user-guide/concepts/tools/custom-tools/

## License

MIT. See [`LICENSE`](LICENSE).
