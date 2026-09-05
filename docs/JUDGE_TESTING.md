# Judge Testing

RolePilot Agent provides a free, credential-free testing path that does not require AWS, Xano, private casting data, or paid model calls.

## Supported judge path

Use Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/verify_release.py
```

The release verifier runs the deterministic test suite, the synthetic queue smoke path, and judge-report generation. It records exact local execution evidence under the ignored `release-evidence/` directory.

For a shorter manual check:

```bash
pytest
rolepilot-agent --deterministic-smoke
rolepilot-agent --judge-report rolepilot-report.html
```

Open `rolepilot-report.html` in a browser to inspect the judge-facing product flow.

## What judges should observe

The synthetic queue contains representative opportunities that exercise the core end-to-end behavior:

1. discover opportunities;
2. inspect requirements and approved materials;
3. classify each opportunity as READY, NEEDS_RECORDING, or REVIEW;
4. prepare and persist an application run only when deterministic safety rules allow it;
5. surface unresolved human decisions;
6. preserve an audit/execution trace;
7. stop before any real external submission.

Rerunning the same queue must not create duplicate active runs for an already prepared opportunity. A run that has been sent back for changes may be prepared again.

## Safety expectations

The competition/demo code intentionally contains no external casting-submission tool. Demo approval changes internal state only. Model output cannot bypass the deterministic preparation validator or authorize a real submission.

No private casting data, credentials, screenshots, generated reports, or release evidence should be committed to the public repository. The canonical in-memory test data is synthetic and public-safe.

## Optional integrations

Xano is optional and is not required for judging. If used, it is the disclosed RolePilot prototype foundation created on 2026-09-03 during the competition submission period.

Amazon Bedrock is also optional for the free judge path. The live Strands/Bedrock path requires explicit opt-in, an approved model id, region, and valid AWS credentials. It must not be treated as verified until an intentionally authorized live run succeeds.

## Current verification caveat

Repository documentation may describe implementation that has not yet been accepted as release evidence. Before final submission, the release candidate still requires executed clean-environment verification, desktop and approximately 390 px mobile visual review of the generated report, privacy/secrets review, and one live Bedrock path when owner-authorized AWS access is available.
