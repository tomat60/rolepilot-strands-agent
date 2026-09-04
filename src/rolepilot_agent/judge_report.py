from __future__ import annotations

from html import escape
from pathlib import Path

from .backend import Backend
from .tools import process_queue_safely


def _reason_text(reasons: list[str]) -> str:
    if not reasons:
        return "No additional action required."
    return ", ".join(str(reason).replace("_", " ") for reason in reasons)


def render_judge_report(backend: Backend) -> str:
    """Render a self-contained, credential-free product view for judges.

    The report uses the same deterministic queue/safety path exposed to Strands tools.
    It demonstrates preparation, persisted run state, decision points and the explicit
    human approval boundary without invoking a model or any external submission path.
    """
    result = process_queue_safely(backend)

    prepared_cards = []
    for item in result["prepared"]:
        run = item["run"]
        audit = "".join(f"<li>{escape(event)}</li>" for event in run["audit_events"])
        prepared_cards.append(
            f"""
            <article class="card ready">
              <div class="eyebrow">READY · PREPARED</div>
              <h3>{escape(str(item['title']))}</h3>
              <p>Application run <strong>#{run['id']}</strong> is prepared and persisted.</p>
              <div class="gate">Human approval: <strong>{escape(run['approval_state'])}</strong></div>
              <details><summary>Audit trace</summary><ol>{audit}</ol></details>
            </article>
            """
        )

    decision_cards = []
    for item in result["decision_points"]:
        state = escape(str(item["state"]))
        decision_cards.append(
            f"""
            <article class="card decision">
              <div class="eyebrow">{state}</div>
              <h3>{escape(str(item['title']))}</h3>
              <p>{escape(_reason_text(item.get('reasons', [])))}</p>
              <div class="gate">Agent stopped here for a real human decision.</div>
            </article>
            """
        )

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>RolePilot Agent · Safe Delegation Demo</title>
<style>
:root {{ color-scheme: dark; font-family: Inter, ui-sans-serif, system-ui, sans-serif; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: #0b0d12; color: #f5f7fb; }}
main {{ max-width: 980px; margin: 0 auto; padding: 40px 20px 64px; }}
.hero {{ padding: 28px; border: 1px solid #2b3240; border-radius: 24px; background: #11151d; }}
h1 {{ font-size: clamp(2rem, 7vw, 4.5rem); line-height: .95; margin: 8px 0 18px; max-width: 760px; }}
.lede {{ color: #b9c1cf; max-width: 720px; font-size: 1.08rem; line-height: 1.6; }}
.badge, .eyebrow {{ font-size: .75rem; letter-spacing: .12em; text-transform: uppercase; font-weight: 800; }}
.badge {{ display: inline-block; padding: 8px 11px; border: 1px solid #3d4658; border-radius: 999px; }}
.stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 18px 0 34px; }}
.stat {{ padding: 18px; border: 1px solid #2b3240; border-radius: 18px; background: #11151d; }}
.stat strong {{ display: block; font-size: 1.65rem; }}
section {{ margin-top: 34px; }}
.grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }}
.card {{ padding: 20px; border: 1px solid #2b3240; border-radius: 18px; background: #11151d; min-width: 0; }}
.card h3 {{ margin: 8px 0 10px; }}
.card p, li {{ color: #c2cad7; line-height: 1.5; }}
.ready {{ border-color: #38644f; }}
.decision {{ border-color: #665839; }}
.gate {{ margin-top: 16px; padding: 12px; border-radius: 12px; background: #171c26; }}
details {{ margin-top: 14px; }}
.safety {{ margin-top: 34px; padding: 20px; border-radius: 18px; background: #15131a; border: 1px solid #463a56; }}
@media (max-width: 640px) {{ .grid, .stats {{ grid-template-columns: 1fr; }} main {{ padding: 20px 14px 40px; }} .hero {{ padding: 20px; }} }}
</style>
</head>
<body>
<main>
  <div class="hero">
    <span class="badge">AWS Agents for Humans · Professional Agent</span>
    <h1>Delegate the queue.<br>Keep the decisions.</h1>
    <p class="lede">RolePilot Agent processes casting work up to the consequential boundary: it prepares safe opportunities, persists an audit trail and surfaces only the cases that need a person.</p>
  </div>
  <div class="stats">
    <div class="stat"><strong>{len(result['prepared'])}</strong>prepared safely</div>
    <div class="stat"><strong>{len(result['decision_points'])}</strong>human decisions</div>
    <div class="stat"><strong>0</strong>external submissions</div>
  </div>
  <section>
    <h2>Prepared work</h2>
    <div class="grid">{''.join(prepared_cards) or '<p>No safe opportunities were prepared.</p>'}</div>
  </section>
  <section>
    <h2>Decision inbox</h2>
    <div class="grid">{''.join(decision_cards) or '<p>No human decisions are waiting.</p>'}</div>
  </section>
  <div class="safety"><strong>Safety invariant</strong><p>Human approval changes internal demo state only. Competition/demo flows contain no real casting submission path.</p></div>
</main>
</body>
</html>"""


def write_judge_report(backend: Backend, path: str | Path) -> Path:
    output = Path(path)
    output.write_text(render_judge_report(backend), encoding="utf-8")
    return output
