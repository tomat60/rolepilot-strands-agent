# Agents for Humans Submission Draft

Status: release-ready working copy. Do not submit or publish without owner approval.

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

The project uses the Python `strands-agents` SDK and custom `@tool` product functions. The tool layer includes opportunity discovery and inspection, readiness analysis, application-run preparation, human-decision state, and autonomous queue processing.

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

The deterministic demo generates a self-contained judge report that shows how many opportunities were prepared, which opportunities need a new recording, which require review, persisted application-run state, audit evidence, the human approval gate, and zero external submissions.

This gives judges a product view of delegation behavior rather than requiring them to interpret terminal logs. The exact CI-generated report from the accepted implementation was visually reviewed at 1440 px and 390 px widths.

## Technical architecture

User goal -> Strands Agent -> custom product tools -> deterministic safety gate -> backend -> persisted run and audit -> human approval boundary

The agent owns orchestration. The deterministic layer owns safety authority.

See `docs/ARCHITECTURE.md` for the repository architecture diagram.

## AWS path

The project includes an explicit, owner-gated Amazon Bedrock live-model path. Normal local and judge-safe execution does not invoke a model. Live Bedrock execution requires deliberate CLI opt-in plus an explicitly configured model ID and region.

No AWS resources are created and no paid model call is made automatically. Until a live Bedrock run is intentionally authorized and verified, the submission must not claim that live Bedrock execution has been demonstrated.

## Potential impact

RolePilot targets a repeated professional workflow where attention is scarce and deadlines matter. The value is not simply faster form filling. The agent reduces queue-management overhead by completing safe preparation in batch and converting a noisy inbox into a small set of real human decisions.

The same safe-delegation pattern can generalize to other professional workflows where agents should do substantial work but must not silently cross consequential legal, financial, consent, or publication boundaries.

## Originality

The differentiated pattern is safe delegation rather than assistant chat. RolePilot combines agent-selected tool use with a separate deterministic authority layer. This lets the model be flexible about work orchestration without making the model the final source of permission.

## Reuse disclosure

A separate RolePilot/Xano prototype was created on September 3, 2026 during the competition period before this Strands repository was opened. It may be used as an optional backend/service foundation. It is not required for the canonical competition demo.

The Strands orchestration, custom tool layer, deterministic safety validator, tests, queue-autonomy behavior, judge-facing report, Bedrock integration path, competition documentation, and submission-specific work were built in this competition repository. Reused work is disclosed rather than represented as new work.

## Verified release evidence

Verified on the accepted implementation and clean CI:

- public competition repository with MIT license, README and architecture documentation;
- Strands agent with multiple custom product tools;
- deterministic safety layer and synthetic memory backend;
- autonomous queue-processing implementation and judge-facing report;
- Python 3.10 and 3.12 clean CI checkout/install/test/smoke execution;
- 75 passing tests on the accepted Python 3.12 release verification run;
- credential-free release verifier completed successfully;
- deterministic smoke proves READY stops at `PENDING_HUMAN_APPROVAL`, NEEDS_RECORDING and REVIEW remain unprepared, and external submission remains false;
- exact CI-generated judge report visually reviewed at desktop 1440 px and mobile 390 px;
- accepted implementation diff reviewed with no committed credentials, tokens, private casting payloads or generated release evidence;
- explicit Bedrock cost/configuration gate;
- disclosure of the September 3 Xano foundation.

Still required before final public submission:

- final main-branch privacy/secrets/diff review after release-documentation changes settle;
- one bounded live Strands plus Bedrock run if the owner intentionally provides AWS credentials/model access and approves the model-call cost; otherwise document it truthfully as unverified;
- final video recorded from verified behavior, uploaded publicly to YouTube or Vimeo, and kept under five minutes;
- AWS Builder ID completed by the owner;
- final Devpost fields/terms reviewed and explicitly submitted by the owner.

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

- [x] Repository is public and accepted implementation is visible on `main`.
- [x] MIT license is visible.
- [x] README install and deterministic demo commands were exercised in clean CI.
- [x] Architecture documentation matches the shipped implementation.
- [x] Accepted implementation review found no secrets or private casting data.
- [x] Exact release-candidate test evidence is green.
- [x] Judge report was visually accepted on desktop and mobile.
- [ ] Run final main-branch privacy/secrets/diff review after release-documentation changes settle.
- [ ] Live Strands plus Bedrock path is verified or truthfully documented as unverified.
- [ ] Video shows the real end-to-end behavior, is below five minutes, and is public on YouTube or Vimeo.
- [x] Reuse disclosure is retained.
- [ ] AWS Builder ID requirement is complete.
- [x] Submission copy has been aligned with the current official requirements as of 2026-09-06.
- [ ] Owner explicitly approves the final public submission and competition terms.
