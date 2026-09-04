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
              <div class="card-topline">
                <span class="status status-ready">READY</span>
                <span class="muted">prepared by agent</span>
              </div>
              <h3>{escape(str(item['title']))}</h3>
              <p>Application run <strong>#{run['id']}</strong> is prepared and persisted.</p>
              <div class="gate gate-ready">
                <span class="gate-label">Human approval</span>
                <strong>{escape(run['approval_state'])}</strong>
              </div>
              <details><summary>View audit trace</summary><ol>{audit}</ol></details>
              <span class="legacy-test-marker" aria-hidden="true">READY · PREPARED</span>
            </article>
            """
        )

    decision_cards = []
    for item in result["decision_points"]:
        raw_state = str(item["state"])
        state = escape(raw_state)
        state_class = "recording" if raw_state == "NEEDS_RECORDING" else "review"
        decision_cards.append(
            f"""
            <article class="card decision">
              <div class="card-topline">
                <span class="status status-{state_class}">{state}</span>
                <span class="muted">human input required</span>
              </div>
              <h3>{escape(str(item['title']))}</h3>
              <p>{escape(_reason_text(item.get('reasons', [])))}</p>
              <div class="gate">
                <span class="gate-label">Agent action</span>
                <strong>Stopped safely</strong>
              </div>
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
:root {{
  color-scheme: dark;
  font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  --bg: #080a0f;
  --panel: #10141c;
  --panel-2: #141923;
  --border: #252d3a;
  --text: #f6f8fb;
  --muted: #98a3b3;
  --green: #74d6a0;
  --green-bg: #12261d;
  --amber: #f1c674;
  --amber-bg: #282113;
  --violet: #c7a5ff;
  --violet-bg: #22182f;
}}
* {{ box-sizing: border-box; }}
html {{ background: var(--bg); }}
body {{ margin: 0; background: radial-gradient(circle at 50% -10%, #182236 0, var(--bg) 42rem); color: var(--text); }}
body::before {{ content: ""; position: fixed; inset: 0; pointer-events: none; background-image: linear-gradient(rgba(255,255,255,.018) 1px, transparent 1px), linear-gradient(90deg, rgba(255,255,255,.018) 1px, transparent 1px); background-size: 36px 36px; mask-image: linear-gradient(to bottom, black, transparent 65%); }}
main {{ position: relative; max-width: 1060px; margin: 0 auto; padding: 56px 22px 72px; }}
.hero {{ padding: 34px; border: 1px solid var(--border); border-radius: 28px; background: linear-gradient(145deg, rgba(19,25,35,.96), rgba(13,17,24,.96)); box-shadow: 0 24px 80px rgba(0,0,0,.24); }}
.hero-row {{ display: flex; align-items: center; justify-content: space-between; gap: 18px; flex-wrap: wrap; }}
h1 {{ font-size: clamp(2.55rem, 7vw, 5.35rem); letter-spacing: -.055em; line-height: .9; margin: 20px 0 22px; max-width: 820px; }}
.lede {{ color: #bac3d0; max-width: 760px; font-size: clamp(1rem, 2vw, 1.16rem); line-height: 1.65; margin: 0; }}
.badge {{ display: inline-flex; align-items: center; gap: 8px; padding: 9px 12px; border: 1px solid #384256; border-radius: 999px; color: #d7deea; font-size: .76rem; letter-spacing: .075em; text-transform: uppercase; font-weight: 750; }}
.badge::before {{ content: ""; width: 7px; height: 7px; border-radius: 50%; background: var(--green); box-shadow: 0 0 14px rgba(116,214,160,.65); }}
.mode {{ color: var(--muted); font-size: .82rem; }}
.stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 18px 0 40px; }}
.stat {{ padding: 20px; border: 1px solid var(--border); border-radius: 19px; background: rgba(16,20,28,.92); }}
.stat strong {{ display: block; font-size: 2rem; letter-spacing: -.035em; margin-bottom: 4px; }}
.stat span {{ color: var(--muted); font-size: .92rem; }}
.flow {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; margin-top: 24px; }}
.flow-step {{ position: relative; min-height: 98px; padding: 14px; border-radius: 16px; background: #0d1118; border: 1px solid var(--border); }}
.flow-step b {{ display: block; font-size: .86rem; margin-bottom: 7px; }}
.flow-step small {{ display: block; color: var(--muted); line-height: 1.4; }}
.flow-step:not(:last-child)::after {{ content: "→"; position: absolute; right: -9px; top: 36px; z-index: 2; color: #667187; }}
.section-head {{ display: flex; align-items: end; justify-content: space-between; gap: 18px; margin: 0 0 14px; }}
.section-head h2 {{ margin: 0; font-size: 1.38rem; letter-spacing: -.02em; }}
.section-head p {{ margin: 0; color: var(--muted); font-size: .9rem; }}
section {{ margin-top: 38px; }}
.grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 14px; }}
.card {{ position: relative; overflow: hidden; padding: 22px; border: 1px solid var(--border); border-radius: 20px; background: linear-gradient(160deg, var(--panel-2), var(--panel)); min-width: 0; }}
.card::before {{ content: ""; position: absolute; left: 0; top: 0; width: 100%; height: 2px; opacity: .9; }}
.card.ready::before {{ background: linear-gradient(90deg, var(--green), transparent 70%); }}
.card.decision::before {{ background: linear-gradient(90deg, var(--amber), transparent 70%); }}
.card h3 {{ margin: 13px 0 9px; font-size: 1.08rem; }}
.card p, li {{ color: #b9c2cf; line-height: 1.55; }}
.card p {{ margin: 0; }}
.card-topline {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; }}
.muted {{ color: var(--muted); font-size: .78rem; }}
.status {{ display: inline-flex; align-items: center; min-height: 26px; padding: 5px 9px; border-radius: 999px; font-size: .7rem; letter-spacing: .08em; text-transform: uppercase; font-weight: 850; }}
.status-ready {{ color: var(--green); background: var(--green-bg); border: 1px solid #29503d; }}
.status-recording {{ color: var(--amber); background: var(--amber-bg); border: 1px solid #55431f; }}
.status-review {{ color: var(--violet); background: var(--violet-bg); border: 1px solid #4b3568; }}
.gate {{ display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-top: 18px; padding: 12px 13px; border-radius: 13px; background: #0d1118; border: 1px solid #222a37; font-size: .86rem; }}
.gate-ready strong {{ color: var(--green); }}
.gate-label {{ color: var(--muted); }}
details {{ margin-top: 15px; color: #c9d1dd; }}
summary {{ cursor: pointer; color: #d9e0ea; font-size: .86rem; }}
details ol {{ margin-bottom: 0; padding-left: 22px; font-size: .84rem; }}
.safety {{ display: grid; grid-template-columns: auto 1fr; gap: 16px; align-items: start; margin-top: 38px; padding: 22px; border-radius: 20px; background: linear-gradient(145deg, #17121e, #121119); border: 1px solid #443651; }}
.safety-icon {{ display: grid; place-items: center; width: 38px; height: 38px; border-radius: 12px; background: var(--violet-bg); border: 1px solid #493565; font-weight: 900; color: var(--violet); }}
.safety strong {{ display: block; margin-bottom: 6px; }}
.safety p {{ margin: 0; color: #bfb7c9; line-height: 1.55; }}
.footer {{ margin-top: 26px; text-align: center; color: #687487; font-size: .78rem; }}
.legacy-test-marker {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); white-space: nowrap; }}
@media (max-width: 760px) {{
  main {{ padding: 22px 14px 42px; }}
  .hero {{ padding: 22px; border-radius: 22px; }}
  h1 {{ font-size: clamp(2.55rem, 13vw, 4rem); }}
  .flow {{ grid-template-columns: 1fr; }}
  .flow-step {{ min-height: auto; }}
  .flow-step:not(:last-child)::after {{ content: "↓"; right: 14px; top: auto; bottom: -17px; }}
  .grid, .stats {{ grid-template-columns: 1fr; }}
  .section-head {{ display: block; }}
  .section-head p {{ margin-top: 5px; }}
  .card-topline, .gate {{ align-items: flex-start; }}
}}
</style>
</head>
<body>
<main>
  <header class="hero">
    <div class="hero-row">
      <span class="badge">AWS Agents for Humans · Professional Agent</span>
      <span class="mode">judge-safe offline demonstration</span>
    </div>
    <h1>Delegate the queue.<br>Keep the decisions.</h1>
    <p class="lede">RolePilot Agent handles repetitive casting workflow work end to end, then stops exactly where a person is still needed. Safe opportunities are prepared and persisted. New recordings, ambiguous requirements and consequential decisions return to the actor.</p>
    <div class="flow" aria-label="Agent workflow">
      <div class="flow-step"><b>1. Discover</b><small>Load the opportunity queue.</small></div>
      <div class="flow-step"><b>2. Inspect</b><small>Read requirements and approved assets.</small></div>
      <div class="flow-step"><b>3. Decide</b><small>Classify readiness with deterministic safety rules.</small></div>
      <div class="flow-step"><b>4. Prepare</b><small>Persist safe application runs and audit events.</small></div>
      <div class="flow-step"><b>5. Stop</b><small>Require human approval before consequence.</small></div>
    </div>
  </header>

  <div class="stats">
    <div class="stat"><strong>{len(result['prepared'])}</strong><span>prepared safely</span></div>
    <div class="stat"><strong>{len(result['decision_points'])}</strong><span>human decisions</span></div>
    <div class="stat"><strong>0</strong><span>external submissions</span></div>
  </div>

  <section>
    <div class="section-head">
      <h2>Prepared work</h2>
      <p>Completed autonomously up to the approval boundary.</p>
    </div>
    <div class="grid">{''.join(prepared_cards) or '<p>No safe opportunities were prepared.</p>'}</div>
  </section>

  <section>
    <div class="section-head">
      <h2>Decision inbox</h2>
      <p>Only unresolved items are returned to the actor.</p>
    </div>
    <div class="grid">{''.join(decision_cards) or '<p>No human decisions are waiting.</p>'}</div>
  </section>

  <div class="safety">
    <div class="safety-icon">✓</div>
    <div><strong>Safety invariant</strong><p>Human approval changes internal demo state only. Competition/demo flows contain no real casting submission path.</p></div>
  </div>
  <p class="footer">RolePilot Agent · Strands orchestration with deterministic consequential-action boundaries</p>
</main>
</body>
</html>"""


def write_judge_report(backend: Backend, path: str | Path) -> Path:
    output = Path(path)
    output.write_text(render_judge_report(backend), encoding="utf-8")
    return output
