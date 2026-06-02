import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_proof_site_builds_from_repo_artifacts():
    result = subprocess.run(
        [sys.executable, "site/build_goal_site.py"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    assert "SITE" in result.stdout
    page = ROOT / "site" / "goal_site.html"
    html = page.read_text(encoding="utf-8")
    assert "<title>Interaktives Deep Research" in html
    assert "Voice Cloning" in html
    assert "Cross-Channel Messaging" in html
    assert "Pipeline-Flow" in html
