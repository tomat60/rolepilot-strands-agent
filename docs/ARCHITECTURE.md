# Architecture

## Goal
RolePilot Agent automates casting application preparation while keeping consequential external action behind an explicit human boundary.

```mermaid
flowchart LR
    U[User goal] --> A[Strands Agent]
    A --> T1[List opportunities tool]
    A --> T2[Analyze readiness tool]
    A --> T3[Prepare run tool]
    A --> T4[Record human decision tool]
    T1 --> B[Backend adapter]
    T2 --> B
    T3 --> S[Deterministic safety gate]
    S --> B
    T4 --> B
    B --> M[Memory backend for tests]
    B --> X[Xano RolePilot backend]
    X --> R[Persisted opportunity/run/audit state]
    R --> H[Human approval boundary]
    H --> N[No real external submission in demo]
```

## Why two control layers
The Strands agent decides which product tools to call and in what order. The deterministic safety layer separately decides whether preparation is allowed. This keeps autonomous orchestration useful without making model output the source of authority for consequential state transitions.

## Current tool contract
- `list_casting_opportunities`: load the queue.
- `analyze_casting_opportunity`: classify readiness.
- `prepare_application_run`: persist preparation only if the safety gate allows it.
- `record_human_decision`: persist an internal demo decision without external submission.

## Backends
### MemoryBackend
Synthetic, deterministic, credential-free backend for tests and offline smoke runs. It contains three competition-safe scenarios: READY, NEEDS_RECORDING, and REVIEW.

### XanoBackend
Adapter for the RolePilot Xano prototype created on 2026-09-03. It uses the prototype REST APIs for opportunities, analysis, application runs, and approval state.

## Security and privacy
- No final casting submission tool exists in this repository.
- No AWS credentials or Xano secrets are committed.
- Tests require no paid model calls.
- Public demo data must remain synthetic.
