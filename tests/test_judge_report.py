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


def test_judge_report_escapes_backend_controlled_run_fields():
    class MaliciousRunBackend(MemoryBackend):
        def create_run(self, opportunity_id: int) -> dict:
            run = super().create_run(opportunity_id)
            run["id"] = '<img src=x onerror="alert(1)">'
            run["approval_state"] = '<script>alert("approval")</script>'
            run["audit_events"] = ['<svg onload="alert(2)"></svg>']
            return run

    html = render_judge_report(MaliciousRunBackend())

    assert '<img src=x onerror="alert(1)">' not in html
    assert '<script>alert("approval")</script>' not in html
    assert '<svg onload="alert(2)"></svg>' not in html
    assert "&lt;img src=x onerror=&quot;alert(1)&quot;&gt;" in html
    assert "&lt;script&gt;alert(&quot;approval&quot;)&lt;/script&gt;" in html
    assert "&lt;svg onload=&quot;alert(2)&quot;&gt;&lt;/svg&gt;" in html
