import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[1]
IDR_PATH = ROOT / "skills" / "integrative-deep-research" / "scripts" / "idr.py"


def load_idr():
    spec = importlib.util.spec_from_file_location("idr_under_test", IDR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def run_idr(args, tmp_path, extra_env=None):
    env = os.environ.copy()
    env["IDR_MOCK"] = "1"
    env["IDR_RUNS_DIR"] = str(tmp_path / "runs")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(IDR_PATH), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )


def run_idr_no_check(args, tmp_path, extra_env=None):
    env = os.environ.copy()
    env["IDR_RUNS_DIR"] = str(tmp_path / "runs")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(IDR_PATH), *args],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )


def test_nlm_query_answer_extracts_value_answer():
    idr = load_idr()
    assert idr._query_answer('{"value":{"answer":"  useful answer  "}}') == "useful answer"
    assert idr._query_answer("{not json") == "{not json"


def test_extract_notebook_id_from_common_shapes():
    idr = load_idr()
    assert idr._extract_notebook_id("notebook_id: abcDEF123_456") == "abcDEF123_456"
    assert (
        idr._extract_notebook_id("created 123e4567-e89b-12d3-a456-426614174000")
        == "123e4567-e89b-12d3-a456-426614174000"
    )


def test_mock_plan_resume_report_e2e(tmp_path):
    plan = json.loads(run_idr(["plan", "Test deterministic IDR pipeline"], tmp_path).stdout)
    assert plan["run_id"]
    assert plan["question"].endswith("?")
    assert Path(plan["rundir"]).is_dir()

    resume = json.loads(
        run_idr(
            [
                "resume",
                plan["run_id"],
                "--answer",
                "Prioritize self-hostable OSS and deterministic artifacts.",
            ],
            tmp_path,
        ).stdout
    )
    report = Path(resume["report"])
    assert report.exists()
    html = report.read_text(encoding="utf-8")
    assert "Integrative Deep Research" in html
    assert "Test deterministic IDR pipeline" in html
    assert "mermaid" in html

    state = json.loads((Path(plan["rundir"]) / "state.json").read_text(encoding="utf-8"))
    assert state["phase"] == "done"
    assert state["mock"] is True
    for key in ("overview", "comparison", "recommendation"):
        assert (Path(plan["rundir"]) / "content" / f"{key}.md").exists()


def test_run_command_uses_askq_bridge_and_generates_report(tmp_path):
    askq_stub = tmp_path / "askq_stub.py"
    askq_stub.write_text(
        "import json\n"
        "import sys\n"
        "assert sys.argv[1].endswith('?')\n"
        "assert '--context' in sys.argv\n"
        "print(json.dumps({'answer': 'Prefer deterministic OSS evidence.'}))\n",
        encoding="utf-8",
    )
    askq_stub.chmod(0o755)

    result = json.loads(
        run_idr(
            ["run", "Full mock run through the askq bridge"],
            tmp_path,
            {"ASKQ_SCRIPT": str(askq_stub)},
        ).stdout
    )

    report = Path(result["report"])
    assert report.exists()
    state = json.loads((report.parent / "state.json").read_text(encoding="utf-8"))
    assert state["phase"] == "done"
    assert state["answer"] == "Prefer deterministic OSS evidence."
    html = report.read_text(encoding="utf-8")
    assert "Full mock run through the askq bridge" in html
    assert "Prefer deterministic OSS evidence." in html


def test_report_command_regenerates_existing_run(tmp_path):
    plan = json.loads(run_idr(["plan", "Regenerate report deterministically"], tmp_path).stdout)
    resume = json.loads(
        run_idr(
            [
                "resume",
                plan["run_id"],
                "--answer",
                "Keep the generated report deterministic and self-contained.",
            ],
            tmp_path,
        ).stdout
    )
    report = Path(resume["report"])
    report.unlink()

    regenerated = json.loads(run_idr(["report", plan["run_id"]], tmp_path).stdout)
    regenerated_report = Path(regenerated["report"])
    assert regenerated_report == report
    assert regenerated_report.exists()
    assert "Regenerate report deterministically" in regenerated_report.read_text(encoding="utf-8")


def test_required_live_rejects_mock_mode(tmp_path):
    result = run_idr_no_check(
        ["plan", "test topic"],
        tmp_path,
        {"IDR_MOCK": "1", "IDR_REQUIRE_LIVE": "1"},
    )
    assert result.returncode == 1
    assert "cannot be combined" in result.stderr


def test_required_live_rejects_missing_fast_notebook_id(tmp_path, monkeypatch):
    idr = load_idr()
    idr.RUNS_DIR = str(tmp_path / "runs")
    monkeypatch.delenv("IDR_MOCK", raising=False)
    monkeypatch.setenv("IDR_REQUIRE_LIVE", "1")
    monkeypatch.setattr(
        idr,
        "_seed_antigravity",
        lambda rundir, topic: {"brief": topic, "seed": str(Path(rundir) / "seed.md")},
    )
    monkeypatch.setattr(
        idr,
        "_nlm_fast_research",
        lambda topic, title: {"notebook_id": None, "raw": "auth failed"},
    )

    with pytest.raises(RuntimeError, match="did not return a notebook_id"):
        idr.cmd_plan("Required live missing notebook")


def test_required_live_query_failure_does_not_fallback(monkeypatch):
    idr = load_idr()
    monkeypatch.delenv("IDR_MOCK", raising=False)
    monkeypatch.setenv("IDR_REQUIRE_LIVE", "1")
    monkeypatch.setattr(idr, "_run", lambda cmd, timeout=300: (1, "", "query failed"))

    with pytest.raises(RuntimeError, match="nlm query failed in required-live mode"):
        idr._nlm_query("notebook-id", "prompt", "mock fallback")


def test_required_live_rejects_deep_failure(tmp_path, monkeypatch):
    idr = load_idr()
    idr.RUNS_DIR = str(tmp_path / "runs")
    monkeypatch.delenv("IDR_MOCK", raising=False)
    monkeypatch.setenv("IDR_REQUIRE_LIVE", "1")
    run_id = "required-live-deep-failure"
    idr._save_state(
        {
            "run_id": run_id,
            "topic": "Deep failure",
            "created": "2026-06-03T00:00:00+00:00",
            "mock": False,
            "seed": {},
            "notebook_id": "real-notebook-id",
            "question": "Question?",
            "answer": None,
            "phase": "awaiting_answer",
        }
    )
    monkeypatch.setattr(idr, "_agy", lambda prompt, timeout=300: None)
    monkeypatch.setattr(
        idr,
        "_nlm_deep_research",
        lambda query, notebook_id: {"ok": False, "raw": "deep timeout"},
    )

    with pytest.raises(RuntimeError, match="NotebookLM deep pass failed"):
        idr.cmd_resume(run_id, "answer")


def test_deep_research_imports_then_starts_with_force(monkeypatch):
    idr = load_idr()
    monkeypatch.delenv("IDR_MOCK", raising=False)
    calls = []

    def fake_run(cmd, timeout=600):
        calls.append(cmd)
        return 0, "started", ""

    monkeypatch.setattr(idr, "_run", fake_run)
    result = idr._nlm_deep_research("query", "notebook-id")

    assert result["ok"] is True
    assert calls[0] == ["nlm", "research", "import", "notebook-id"]
    start_cmd = calls[1]
    assert start_cmd[:4] == ["nlm", "research", "start", "query"]
    assert "--mode" in start_cmd and "deep" in start_cmd
    assert "--notebook-id" in start_cmd and "notebook-id" in start_cmd
    assert "--auto-import" in start_cmd
    assert "--force" in start_cmd


def test_run_fails_when_askq_script_missing(tmp_path):
    result = run_idr_no_check(
        ["run", "test topic"],
        tmp_path,
        {"IDR_MOCK": "1", "ASKQ_SCRIPT": str(tmp_path / "missing-askq.py")},
    )
    assert result.returncode == 1
    assert "askq failed" in result.stderr
