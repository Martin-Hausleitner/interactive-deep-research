import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
IDR = ROOT / "skills" / "integrative-deep-research" / "scripts" / "idr.py"


pytestmark = pytest.mark.live


@pytest.mark.skipif(os.environ.get("IDR_LIVE_E2E") != "1", reason="set IDR_LIVE_E2E=1 to spend live NotebookLM quota")
@pytest.mark.skipif(shutil.which("nlm") is None, reason="nlm CLI is not on PATH")
def test_live_notebooklm_plan_resume_report(tmp_path):
    """Real fast+deep NotebookLM E2E. Opt-in only because it uses auth, network, and quota."""
    env = os.environ.copy()
    env.pop("IDR_MOCK", None)
    env["IDR_REQUIRE_LIVE"] = "1"
    env["IDR_RUNS_DIR"] = str(tmp_path / "runs")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    assert "IDR_MOCK" not in env
    assert env["IDR_REQUIRE_LIVE"] == "1"
    topic = os.environ.get(
        "IDR_LIVE_TOPIC",
        "Compact OSS documentation and E2E test strategy for a deterministic NotebookLM-backed CLI pipeline",
    )
    answer = os.environ.get(
        "IDR_LIVE_ANSWER",
        "Prioritize CI-safe tests, one opt-in live NotebookLM test, and concise contributor documentation.",
    )

    plan = subprocess.run(
        [sys.executable, str(IDR), "plan", topic],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=900,
        check=True,
    )
    plan_payload = json.loads(plan.stdout)
    assert plan_payload["notebook_id"]
    assert plan_payload["question"].strip().endswith("?")
    run_dir = Path(plan_payload["rundir"])
    assert run_dir.is_dir()

    resume = subprocess.run(
        [sys.executable, str(IDR), "resume", plan_payload["run_id"], "--answer", answer],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        timeout=2400,
        check=True,
    )
    resume_payload = json.loads(resume.stdout)
    assert resume_payload["notebook_id"] == plan_payload["notebook_id"]

    report = Path(resume_payload["report"])
    assert report.exists()
    assert report.parent == run_dir

    state = json.loads((run_dir / "state.json").read_text(encoding="utf-8"))
    assert state["phase"] == "done"
    assert state["mock"] is False
    assert state["notebook_id"] == plan_payload["notebook_id"]
    assert state["deep"]["ok"] is True
    assert state["report"] == str(report)
    assert state["answer"] == answer
    assert state["question"] == plan_payload["question"]
    for key in ("overview", "comparison", "recommendation"):
        content_path = run_dir / "content" / f"{key}.md"
        assert content_path.exists()
        content = content_path.read_text(encoding="utf-8").strip()
        assert content
        assert "nlm query failed" not in content
        assert "Traceback" not in content
        assert "mock fallback" not in content
        assert "##" in content or "|" in content
        assert state["content"][key] == str(content_path)

    html = report.read_text(encoding="utf-8")
    assert topic in html
    assert "Overview" in html
    assert "Recommendation" in html
    assert "nlm query failed" not in html
    assert "mock fallback" not in html
