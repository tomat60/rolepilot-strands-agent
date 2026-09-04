from rolepilot_agent.backend import MemoryBackend
from rolepilot_agent.judge_report import render_judge_report


def test_judge_report_shows_prepared_work_decisions_and_zero_submission():
    html = render_judge_report(MemoryBackend())

    assert "Delegate the queue" in html
    assert "1</strong>prepared safely" in html
    assert "2</strong>human decisions" in html
    assert "0</strong>external submissions" in html
    assert "READY · PREPARED" in html
    assert "NEEDS_RECORDING" in html
    assert "REVIEW" in html
    assert "Human approval: <strong>PENDING</strong>" in html
    assert "no real casting submission path" in html
