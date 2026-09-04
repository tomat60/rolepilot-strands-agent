from __future__ import annotations

import argparse
import json
import os

from .agent import build_agent
from .backend import MemoryBackend, XanoBackend
from .judge_report import write_judge_report
from .live_model import bedrock_settings_from_env, build_bedrock_model


def _backend_from_args(args):
    if args.backend == "xano":
        base_url = args.xano_base_url or os.getenv("ROLEPILOT_XANO_BASE_URL")
        if not base_url:
            raise SystemExit(
                "Set --xano-base-url or ROLEPILOT_XANO_BASE_URL for the Xano backend."
            )
        return XanoBackend(base_url)
    return MemoryBackend()


def main() -> None:
    parser = argparse.ArgumentParser(description="RolePilot Strands Agent")
    parser.add_argument("prompt", nargs="?", default="Process my casting opportunity queue.")
    parser.add_argument("--backend", choices=("memory", "xano"), default="memory")
    parser.add_argument("--xano-base-url")
    parser.add_argument(
        "--deterministic-smoke",
        action="store_true",
        help="Run the safety layer without invoking a model or AWS.",
    )
    parser.add_argument(
        "--judge-report",
        metavar="PATH",
        help="Write a self-contained HTML product report using the deterministic queue path.",
    )
    parser.add_argument(
        "--live-bedrock",
        action="store_true",
        help=(
            "Explicitly opt in to a live Amazon Bedrock model invocation. "
            "This may incur AWS usage cost and requires explicit model/region configuration."
        ),
    )
    args = parser.parse_args()
    backend = _backend_from_args(args)

    if args.judge_report:
        output = write_judge_report(backend, args.judge_report)
        print(f"Judge report written to {output}")
        return

    if args.deterministic_smoke:
        summary = []
        for opportunity in backend.list_opportunities():
            opportunity_id = int(opportunity["id"])
            analysis = backend.analyze(opportunity_id)
            item = {"opportunity_id": opportunity_id, "analysis": analysis}
            if analysis.get("can_prepare") and analysis.get("state") == "READY":
                item["prepared_run"] = backend.create_run(opportunity_id)
            summary.append(item)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return

    if not args.live_bedrock:
        raise SystemExit(
            "Live model execution is disabled by default. Use --deterministic-smoke or "
            "--judge-report for the free competition-safe path. Use --live-bedrock only "
            "after AWS access/cost approval and explicit Bedrock model configuration."
        )

    settings = bedrock_settings_from_env()
    model = build_bedrock_model(settings)
    agent = build_agent(backend, model=model)
    result = agent(args.prompt)
    print(result)


if __name__ == "__main__":
    main()
