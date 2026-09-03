# RolePilot Agent

**Safe delegation for casting applications, built with the Strands Agents SDK.**

RolePilot Agent is an autonomous professional-workflow agent for actors and talent teams. It processes casting opportunities, checks whether approved materials are sufficient, prepares safe application state when possible, surfaces only the decisions that need a person, and stops before any real external submission.

This repository is the competition-specific Strands implementation for the AWS **Agents for Humans** hackathon.

## Product principle

Automate preparation. Keep authority human.

The agent may inspect opportunities, analyze readiness, select approved materials, prepare an application run, and persist an audit trail. It must not submit a real casting application. Consequential external action remains behind an explicit human approval boundary.

## Current build status

Repository bootstrap started on 2026-09-03. The first vertical slice is being implemented now.

## Relationship to the Xano RolePilot prototype

A separate RolePilot/Xano prototype was created on 2026-09-03 during the competition period before this repository was opened. This project may use that prototype as a backend/service foundation. The Strands agent orchestration, agent tools, safety layer, tests, competition integration, and submission-specific product work are being built in this repository. Reused work will be disclosed rather than presented as newly created here.

## Planned architecture

`User goal -> Strands Agent -> product tools -> deterministic safety gate -> Xano/local backend -> persisted run -> human approval`

The Strands agent decides which tools to call. Deterministic product rules separately enforce that incomplete, recording-required, or manual-review opportunities cannot cross the preparation gate.

## Development

Python 3.10+ is required. Full setup and run instructions will be added with the first implementation slice.

Official Strands documentation: https://strandsagents.com/docs/user-guide/quickstart/python/

## License

MIT license will be included in the bootstrap milestone.
