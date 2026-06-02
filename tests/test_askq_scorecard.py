import json
import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASKQ = ROOT / "skills" / "askq" / "scripts" / "askq.py"
SCORECARD = ROOT / "skills" / "deep-research-scorecard" / "scripts" / "scorecard.py"


def run_cmd(args, **kwargs):
    return subprocess.run(
        [sys.executable, *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
        **kwargs,
    )


def run_cmd_no_check(args, **kwargs):
    return subprocess.run(
        [sys.executable, *map(str, args)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
        **kwargs,
    )


def test_askq_non_interactive_json_stdout_only():
    result = run_cmd([ASKQ, "Constraint?", "--answer", "self-hosted", "--no-log"])
    payload = json.loads(result.stdout)
    assert payload["question"] == "Constraint?"
    assert payload["answer"] == "self-hosted"
    assert payload["mode"] == "non-interactive"
    assert result.stderr == ""


def test_askq_env_answer_choices_and_custom_log(tmp_path):
    log = tmp_path / "askq.jsonl"
    env = {**os.environ, "ASKQ_ANSWER": "deep"}
    result = run_cmd(
        [ASKQ, "Pick a depth?", "--choices", "fast|deep", "--log", log],
        env=env,
    )
    payload = json.loads(result.stdout)
    assert payload["answer"] == "deep"
    assert payload["choices"] == ["fast", "deep"]
    assert payload["mode"] == "non-interactive"

    lines = log.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["question"] == "Pick a depth?"


def test_askq_missing_question_exits_usage_without_log(tmp_path):
    log = tmp_path / "askq.jsonl"
    result = run_cmd_no_check([ASKQ, "--log", log], input="")
    assert result.returncode == 64
    assert result.stdout == ""
    assert "askq: no question provided" in result.stderr
    assert not log.exists()


def test_scorecard_crowns_expected_voice_winner():
    result = run_cmd([SCORECARD, ROOT / "data" / "voice_scorecard.json"])
    assert "Sieger: CosyVoice 3.0" in result.stdout
    assert "| 1 | **[CosyVoice 3.0]" in result.stdout
    assert "Σ/100" in result.stdout


def test_scorecard_html_fragment_contains_expected_classes():
    result = run_cmd([SCORECARD, ROOT / "data" / "voice_scorecard.json", "--html"])
    assert '<table class="scorecard">' in result.stdout
    assert '<div class="winner">' in result.stdout
    assert "CosyVoice 3.0" in result.stdout


def test_scorecard_accepts_stdin_spec():
    spec = (ROOT / "data" / "voice_scorecard.json").read_text(encoding="utf-8")
    result = run_cmd([SCORECARD, "-"], input=spec)
    assert "Sieger: CosyVoice 3.0" in result.stdout
    assert "Scorecard" in result.stdout


def test_scorecard_invalid_spec_exits_cleanly(tmp_path):
    spec = tmp_path / "bad.json"
    spec.write_text(
        json.dumps(
            {
                "criteria": [{"key": "quality", "label": "Quality", "weight": 1}],
                "candidates": [{"name": "Broken", "scores": {"quality": 11}}],
            }
        ),
        encoding="utf-8",
    )
    result = run_cmd_no_check([SCORECARD, spec])
    assert result.returncode == 1
    assert result.stdout == ""
    assert "scorecard: error:" in result.stderr
    assert "within 0..10" in result.stderr


def test_scorecard_malformed_json_exits_cleanly():
    result = run_cmd_no_check([SCORECARD, "-"], input="{bad json")
    assert result.returncode == 1
    assert result.stdout == ""
    assert "scorecard: error:" in result.stderr


def test_scorecard_requires_candidates(tmp_path):
    spec = tmp_path / "empty.json"
    spec.write_text(
        json.dumps(
            {
                "criteria": [{"key": "quality", "label": "Quality", "weight": 1}],
                "candidates": [],
            }
        ),
        encoding="utf-8",
    )
    result = run_cmd_no_check([SCORECARD, spec])
    assert result.returncode == 1
    assert result.stdout == ""
    assert "candidates must be a non-empty list" in result.stderr
