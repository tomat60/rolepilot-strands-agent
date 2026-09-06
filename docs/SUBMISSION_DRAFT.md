# Agents for Humans Submission Draft

Status: working draft. Do not submit or publish without owner approval.

## Project title

RolePilot Agent: Safe Delegation for Casting Applications

## Target track

Professional Agents

## One-line description

RolePilot Agent uses Strands to process an actor's casting queue, prepare every safe application, and surface only the decisions that still require a person, while a deterministic safety layer prevents autonomous external submission.

## The problem

Professional actors repeatedly receive fragmented casting opportunities with short deadlines, duplicated agency routes, different material requirements, new self-tape requests, rights questions, and manual application steps. The expensive part is not only filling a form. It is continuously deciding what can be handled now, what needs new work, what is risky, and what has already been handled.

Traditional automation is too rigid for this workflow, while an unconstrained AI assistant creates unacceptable risk around availability, rights, likeness, duplicate submissions, and external communication.

## The solution

RolePilot Agent is a safe delegation layer for casting applications.

The user delegates the queue, not each individual click. A Strands agent chooses product tools to inspect opportunities and approved materials, assess readiness, prepare safe application state, persist an audit trail, and request a human decision only when needed.

Every opportunity ends in one of three explainable states:

- READY: the required approved materials are available and a safe application run can be prepared.
- NEEDS_RECORDING: the opportunity requires new voice, video, or self-tape material.
- REVIEW: rights, consent, duplicate evidence, missing information, malformed backend data, or another ambiguity requires a person.

Prepared work still stops at a human approval boundary. The competition project intentionally contains no tool that can submit a real casting application.

## Why this is an agent, not a chatbot

The Strands agent is given multiple custom product tools and decides which ones to call based on the queue and current state. It can inspect opportunities, inspect approved assets, evaluate readiness, create persisted application runs, record human-decision state, and process the full queue in one delegated task.

The orchestration is separated from deterministic consequential-action rules. Model output can decide what tool to call, but model output alone cannot promote an unsafe opportunity through the preparation gate or authorize an external action.

## Strands implementation

The project uses the Python `strands-agents` SDK and custom `@tool` product functions. The current tool layer includes opportunity discovery and inspection, readiness analysis, application-run preparation, human-decision state, and autonomous queue processing.

A deterministic safety validator independently enforces READY, NEEDS_RECORDING, and REVIEW behavior. Tests run without paid model calls or AWS credentials.

The canonical judge-safe backend is an in-memory implementation with synthetic data. An adapter for the RolePilot Xano prototype exists only as an optional integration and is not required to run the agent or demo.

## Human control and safety

Key invariants:

1. The competition repository has no final external-submission tool.
2. Model output alone cannot authorize a consequential transition.
3. New recording requirements stop the affected lane.
4. Rights or consent ambiguity stops the affected lane.
5. Missing or unapproved assets fail closed.
6. Possible duplicate submission evidence fails closed.
7. Malformed or contradictory backend readiness data fails closed.
8. A failure in one opportunity is isolated so the rest of the queue can continue safely.
9. Audit state is persisted for prepared work and decisions.
10. Competition data is synthetic and public-safe.

## User experience

The deterministic demo can generate a self-contained judge report that shows:

- how many opportunities were prepared;
- which opportunities need a new recording;
- which opportunities require review;
- persisted application-run state;
- audit evidence;
- the human approval gate;
- zero external submissions.

This gives judges a product view of delegation behavior rather than requiring them to interpret terminal logs.

## Technical architecture

User goal -> Strands Agent -> custom product tools -> deterministic safety gate -> backend -> persisted run and audit -> human approval boundary

The agent owns orchestration. The deterministic layer owns safety authority.

See `docs/ARCHITECTURE.md` for the repository architecture diagram.

## AWS path

The project includes an explicit, owner-gated Amazon Bedrock live-model path. Normal local and judge-safe execution does not invoke a model. Live Bedrock execution requires deliberate CLI opt-in plus an explicitly configured model ID and region.

This design keeps deterministic development and judging reproducible while allowing a verified live Strands plus Bedrock path once AWS credentials and model access are intentionally supplied.

No AWS resources are created and no paid model call is made automatically.

## Potential impact

RolePilot targets a repeated professional workflow where attention is scarce and deadlines matter. The value is not simply faster form filling. The agent reduces queue-management overhead by completing safe preparation in batch and converting a noisy inbox into a small set of real human decisions.

The same safe-delegation pattern can generalize to other professional workflows where agents should do substantial work but must not silently cross consequential legal, financial, consent, or publication boundaries.

## Originality

The differentiated pattern is safe delegation rather than assistant chat. RolePilot combines agent-selected tool use with a separate deterministic authority layer. This lets the model be flexible about work orchestration without making the model the final source of permission.

## Reuse disclosure

A separate RolePilot/Xano prototype was created on September 3, 2026 during the competition period before this Strands repository was opened. It may be used as an optional backend/service foundation. It is not required for the canonical competition demo.

The Strands orchestration, custom tool layer, deterministic safety validator, tests, queue-autonomy behavior, judge-facing report, Bedrock integration path, competition documentation, and submission-specific work are built in this competition repository. Reused work is disclosed rather than represented as new work.

## Current verification status

Do not convert this section into a submission claim until the evidence exists.

Verified in repository structure and implementation review:

- public competition repository;
- MIT license;
- Strands agent and custom product tools;
- deterministic safety layer;
- synthetic memory backend;
- queue-processing implementation;
- judge-report implementation;
- tests covering safety and reliability scenarios;
- explicit Bedrock cost/configuration gate;
- disclosure of the September 3 Xano foundation.

Still required before final submission:

- exact-head tests executed successfully in a clean environment;
- deterministic smoke executed successfully;
- generated judge report opened and visually reviewed at desktop and mobile width;
- one bounded live Strands plus Bedrock run when owner credentials/model access are available;
- final public repository hygiene review for secrets/private casting data;
- final architecture check against actual implementation;
- final video recorded and kept within the competition limit;
- AWS Builder ID owner gate completed;
- final Devpost fields and terms reviewed and explicitly submitted by the owner.

## Judge run path

Credential-free deterministic path:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
rolepilot-agent --deterministic-smoke
rolepilot-agent --judge-report rolepilot-report.html
```

Optional live Bedrock path after intentional AWS configuration:

```bash
export ROLEPILOT_BEDROCK_MODEL_ID="YOUR_APPROVED_MODEL_ID"
export ROLEPILOT_BEDROCK_REGION="YOUR_APPROVED_REGION"
rolepilot-agent --live-bedrock "Process my casting opportunity queue."
```

## Final submission checklist

- [ ] Repository is public and final commit is visible.
- [ ] MIT license is visible.
- [ ] README install and demo commands work from a clean environment.
- [ ] Architecture diagram matches the shipped code.
- [ ] No secrets or private casting data are present.
- [ ] Exact-head test evidence is green.
- [ ] Judge report is visually accepted on desktop and mobile.
- [ ] Live Strands plus Bedrock path is verified or truthfully documented as unavailable.
- [ ] Video shows the real end-to-end behavior and is within the permitted duration.
- [ ] Reuse disclosure is retained.
- [ ] AWS Builder ID requirement is complete.
- [ ] Devpost copy is checked against current official fields and rules.
- [ ] Owner explicitly approves the final public submission.
