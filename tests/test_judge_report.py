from rolepilot_agent.backend import MemoryBackend
from rolepilot_agent.judge_report import render_judge_report


def test_judge_report_shows_prepared_work_decisions_and_zero_submission():
    html = render_judge_report(MemoryBackend())

    assert "Delegate the queue" in html
    assert "1</strong><span>prepared safely" in html
    assert "2</strong><span>human decisions" in html
    assert "0</strong><span>external submissions" in html
    assert "READY · PREPARED" in html
    assert "NEEDS_RECORDING" in html
    assert "REVIEW" in html
    assert "Human approval" in html
    assert "PENDING_HUMAN_APPROVAL" in html
    assert "no real casting submission path" in html


def test_judge_report_explains_the_agent_workflow_and_human_boundary():
    html = render_judge_report(MemoryBackend())

    assert "1. Discover" in html
    assert "2. Inspect" in html
    assert "3. Decide" in html
    assert "4. Prepare" in html
    assert "5. Stop" in html
    assert "Only unresolved items are returned to the actor." in html
    assert "judge-safe offline demonstration" in html
