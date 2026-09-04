from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


def _run(command: list[str]) -> dict[str, object]:
    completed = subprocess.run(command, text=True, capture_output=True)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "passed": completed.returncode == 0,
    }


def _git_sha() -> str:
    completed = subprocess.run(
        ["git", "rev-parse", "HEAD"], text=True, capture_output=True
    )
    if completed.returncode != 0:
        return "UNKNOWN"
    return completed.stdout.strip()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run the credential-free RolePilot release gate and record evidence."
    )
    parser.add_argument(
        "--output-dir",
        default="release-evidence",
        help="Directory for the JSON evidence record and judge report.",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    report_path = output_dir / "rolepilot-report.html"

    commands = [
        [sys.executable, "-m", "pytest"],
        [sys.executable, "-m", "rolepilot_agent.cli", "--deterministic-smoke"],
        [
            sys.executable,
            "-m",
            "rolepilot_agent.cli",
            "--judge-report",
            str(report_path),
        ],
    ]

    results = [_run(command) for command in commands]
    evidence = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "commit_sha": _git_sha(),
        "python_version": sys.version,
        "credential_free": True,
        "external_submission_attempted": False,
        "report_path": str(report_path),
        "checks": results,
        "passed": all(bool(result["passed"]) for result in results),
        "manual_visual_review": {
            "desktop": "PENDING",
            "mobile_approx_390px": "PENDING",
        },
        "live_bedrock": "NOT_RUN_OWNER_GATED",
    }

    evidence_path = output_dir / "verification.json"
    evidence_path.write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Release evidence written to {evidence_path}")
    print(f"Judge report written to {report_path}")
    return 0 if evidence["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
