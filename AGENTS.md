# AGENTS.md

## Mission
Build a competition-grade Strands agent that automates casting application preparation while preserving explicit human authority over consequential external actions.

## Product invariants
- The agent may inspect, analyze, prepare, persist, and request a human decision.
- The agent must never submit a real casting application from this repository.
- Model output alone can never authorize a consequential state transition.
- READY, NEEDS_RECORDING, and REVIEW must remain truthful and explainable.
- Synthetic or competition-safe data only. Never commit private casting materials, credentials, or personal secrets.
- Reused work must be disclosed.

## Engineering rules
- Python 3.10+.
- Use the Strands Agents SDK for the actual agent orchestration.
- Prefer custom `@tool` functions for product actions.
- Keep deterministic safety checks separate from the LLM.
- Tests must run without AWS credentials or paid model calls.
- Use one bounded implementation PR at a time.
- Code committed is not done. Verify tests, CI, docs, behavior, and exact evidence.

## Competition priorities
1. Genuine Strands tool use and autonomous orchestration.
2. End-to-end useful workflow, not a chat toy.
3. Clear human approval boundary.
4. Judge-friendly product experience.
5. Reliable public setup and demo path.

## External action boundary
Do not add code that performs a final external casting submission. Demo approval may update internal state only.
