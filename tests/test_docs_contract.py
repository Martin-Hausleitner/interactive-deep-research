import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILLS = (
    "interactive-deep-research",
    "integrative-deep-research",
    "askq",
    "deep-research-scorecard",
)
PRIVATE_MARKERS = (
    "100" + ".120",
    "510" + "7",
    "510" + "5",
    "518" + "2",
    "file" + "://",
    "/Users/" + "mh",
    "Account" + ":",
    "mart" + "iking",
    "vc" + "vm",
    "tail" + "net",
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_readme_documents_pipeline_and_skill_invocation_with_mermaid():
    text = read("README.md")
    mermaid_blocks = re.findall(r"```mermaid\n(.*?)\n```", text, flags=re.DOTALL)
    assert len(mermaid_blocks) >= 2
    assert any("NotebookLM FAST pass" in block and "report.html" in block for block in mermaid_blocks)
    assert any(
        "interactive-deep-research" in block
        and "integrative-deep-research" in block
        and "deep-research-scorecard" in block
        for block in mermaid_blocks
    )
    for phrase in (
        "Quickstart",
        "proof site",
        "Verification",
        "Privacy",
        "Failure Modes",
        "IDR_REQUIRE_LIVE=1",
        "IDR_MOCK=1",
    ):
        assert phrase in text


def test_packaged_skills_have_oss_documentation_contract():
    for skill in SKILLS:
        text = read(f"skills/{skill}/SKILL.md")
        assert f"name: {skill}" in text
        assert "description:" in text
        assert "version:" in text
        assert "license: MIT" in text
        assert "## Privacy / No PII" in text
        assert "Failure" in text or "Exit Behavior" in text
        assert "```bash" in text or "```mermaid" in text


def test_install_and_ci_cover_all_packaged_skills():
    install = read("install.sh")
    ci = read(".github/workflows/ci.yml")
    for skill in SKILLS:
        assert skill in install
        assert (ROOT / "skills" / skill / "SKILL.md").exists()
    for driver in ("idr.py", "askq.py", "scorecard.py"):
        assert driver in install
        assert driver in ci
    assert "pytest" in ci
    assert '-m "not live"' in ci


def test_layout_has_no_tracked_root_site_duplicates_or_bytecode():
    tracked = subprocess_git_ls_files()
    forbidden_roots = {
        "PROGRESS.md",
        "audio_demos.json",
        "build_audios.py",
        "build_goal_site.py",
        "site_config.json",
    }
    assert forbidden_roots.isdisjoint(tracked)
    assert not any("__pycache__/" in path or path.endswith(".pyc") for path in tracked)


def test_proof_site_is_rendered_repo_relative_and_public_safe():
    html = read("site/goal_site.html")
    index = read("site/index.html")
    assert "<title>Interaktives Deep Research — Verlauf, Output & Beweis</title>" in html
    assert "Pipeline-Flow" in html
    assert "reports/voice/report.html" in html
    assert "reports/messaging/report.html" in html
    assert html == index


def test_public_artifacts_do_not_contain_private_machine_markers():
    paths = [
        "README.md",
        "TESTING.md",
        "VERIFICATION.md",
        "CONTRIBUTING.md",
        "GOAL.md",
        "CHANGELOG.md",
        ".github/workflows/ci.yml",
        "openaudio-calculator/index.html",
    ]
    paths.extend(f"skills/{skill}/SKILL.md" for skill in SKILLS)
    paths.extend(str(path.relative_to(ROOT)) for path in (ROOT / "tests").glob("*.py"))
    paths.extend(str(path.relative_to(ROOT)) for path in (ROOT / "reports").rglob("*.html"))
    paths.extend(str(path.relative_to(ROOT)) for path in (ROOT / "site").glob("*.html"))

    hits = []
    for path in paths:
        text = read(path)
        if any(marker in text for marker in PRIVATE_MARKERS):
            hits.append(path)
    assert hits == []


def subprocess_git_ls_files() -> set[str]:
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return set(result.stdout.splitlines())
