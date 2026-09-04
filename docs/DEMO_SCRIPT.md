# Competition Demo Script

Status: working production script. Keep the final recording under the current competition video limit and verify the limit again before publishing.

## Goal

Show one clear story: an actor delegates a noisy casting queue, RolePilot Agent does the safe work with Strands tools, and only the real decisions come back to the person.

Do not spend the video reading source code. Show the product behavior first, then briefly prove the Strands architecture and safety boundary.

## Recommended runtime

Target 4:15 to 4:40 so there is margin for transitions and platform encoding.

## 0:00-0:25 - Problem

Visual:
- inbox or synthetic queue with several different casting opportunities;
- labels showing short deadlines, new recording, rights review, and existing materials.

Narration points:
- Actors repeatedly receive fragmented opportunities from different sources.
- The hard part is deciding what can be completed immediately, what needs new creative work, and what is risky or duplicated.
- Existing assistants still make the user micromanage each item.

Core line:
"RolePilot lets the actor delegate the queue instead of delegating one click at a time."

## 0:25-0:50 - Product thesis

Visual:
- simple architecture diagram;
- highlight Strands Agent, custom tools, deterministic safety gate, human approval.

Narration points:
- Strands owns orchestration and decides which product tools to call.
- Deterministic rules own permission for consequential transitions.
- The model can decide what work to attempt, but it cannot grant itself authority.

## 0:50-2:10 - End-to-end queue run

Visual:
- start with the synthetic three-opportunity queue;
- trigger the deterministic judge-safe path or live Bedrock path if verified;
- open the generated judge report.

Show three outcomes:

1. READY
- required approved materials exist;
- agent prepares and persists an application run;
- state stops at `PENDING_HUMAN_APPROVAL`.

2. NEEDS_RECORDING
- new self-tape or recording is required;
- affected lane stops and becomes a real user decision.

3. REVIEW
- rights/consent or another ambiguity requires a person;
- no preparation promotion occurs.

Narration points:
- One delegated queue task produces prepared work plus only unresolved decisions.
- The agent does not force the user to inspect every opportunity manually.

## 2:10-2:50 - Safety proof

Visual:
- judge report section with zero external submissions;
- audit events;
- briefly show a relevant safety test or validator code.

Narration points:
- There is intentionally no final external-submission tool in the competition repository.
- Missing assets, duplicate evidence, rights ambiguity, malformed backend state, and per-opportunity failures all fail closed.
- One broken opportunity does not crash or contaminate the rest of the queue.

Core line:
"Flexible orchestration is separated from authority."

## 2:50-3:30 - Strands depth

Visual:
- `agent.py` and custom tools in `tools.py`;
- show the agent receiving multiple tools rather than a single hard-coded sequence;
- if a verified live trace is available, show tool calls from the Strands run.

Narration points:
- This is not a chat wrapper.
- The agent has product tools for discovery, inspection, readiness assessment, preparation, decision state, and full-queue processing.
- The deterministic backend and tests do not require paid model calls.

If live Bedrock is verified:
- show one bounded Strands plus Bedrock invocation;
- state the exact model used truthfully in the final recording.

If it is not verified:
- do not imply it is live;
- show the implemented opt-in path only as architecture and keep the demonstrated run deterministic.

## 3:30-4:05 - Product experience and impact

Visual:
- judge report at desktop width;
- judge report at mobile width;
- prepared vs needs recording vs review hierarchy.

Narration points:
- The interface is organized around decisions, not generic SaaS cards.
- The user sees what was handled, what needs recording, what needs review, and what is waiting for approval.
- The pattern can generalize to professional workflows where agents should do substantial work without silently crossing legal, financial, consent, or publication boundaries.

## 4:05-4:30 - Close

Visual:
- final architecture and project title;
- public repository.

Narration points:
- RolePilot Agent demonstrates safe delegation: autonomous work, explicit human authority.
- Built with the Strands Agents SDK for AWS Agents for Humans.

Closing line:
"Automate preparation. Keep authority human."

## Evidence capture checklist before recording

- [ ] Clean install succeeds from documented instructions.
- [ ] Full deterministic test suite passes.
- [ ] Deterministic smoke passes.
- [ ] Judge report is generated from the exact release head.
- [ ] Judge report is visually inspected at desktop width.
- [ ] Judge report is visually inspected around 390 px mobile width.
- [ ] No console or page errors are present in the chosen demo path.
- [ ] Audit and approval state shown in the video come from the actual run.
- [ ] Zero external submission is visible and true.
- [ ] If Bedrock is shown as live, one exact live run was actually verified beforehand.
- [ ] No private inbox data, email addresses, credentials, casting documents, or personal secrets appear on screen.
- [ ] Repository URL is public and accessible in a logged-out browser.
- [ ] Final video duration is below the current official competition limit.

## Recording rule

Use synthetic/public-safe casting data in the competition video. Real casting emails and private agency materials are not needed to prove the product and should not be exposed.
