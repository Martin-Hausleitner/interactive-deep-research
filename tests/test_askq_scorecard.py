import json
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


def test_askq_non_interactive_json_stdout_only():
    result = run_cmd([ASKQ, "Constraint?", "--answer", "self-hosted", "--no-log"])
    payload = json.loads(result.stdout)
    assert payload["question"] == "Constraint?"
    assert payload["answer"] == "self-hosted"
    assert payload["mode"] == "non-interactive"
    assert result.stderr == ""


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
