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
SECRET_PATTERNS = (
    re.compile("sk-" + r"[A-Za-z0-9_-]{20,}"),
    re.compile("ghp_" + r"[A-Za-z0-9_]{20,}"),
    re.compile("AK" + "IA" + r"[0-9A-Z]{16}"),
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
    verify = read("scripts/verify.sh")
    for skill in SKILLS:
        assert skill in install
        assert (ROOT / "skills" / skill / "SKILL.md").exists()
    for driver in ("idr.py", "askq.py", "scorecard.py"):
        assert driver in install
        assert driver in verify
    assert "./scripts/verify.sh" in ci
    assert "pytest" in verify
    assert '-m "not live"' in verify


def test_verify_script_is_documented_and_used_by_ci():
    script = ROOT / "scripts" / "verify.sh"
    assert script.exists()
    assert script.stat().st_mode & 0o111

    script_text = script.read_text(encoding="utf-8")
    assert "pytest -p no:cacheprovider -m \"not live\"" in script_text
    assert "SITE_BUILD_TS" in script_text
    assert "git diff --check" in script_text
    assert "local Python bytecode artifacts" in script_text
    assert "private machine marker" in script_text
    assert "secret_patterns" in script_text
    assert "possible secret token" in script_text
    assert "grep -n -E" in script_text
    assert "sk-" in script_text
    assert "ghp_" in script_text
    assert '"AK""IA' in script_text
    assert "grep" in script_text
    assert " rg " not in script_text

    assert "./scripts/verify.sh" in read(".github/workflows/ci.yml")
    assert "./scripts/verify.sh" in read("README.md")
    assert "./scripts/verify.sh" in read("TESTING.md")
    assert "./scripts/verify.sh" in read("CONTRIBUTING.md")


def test_ci_uses_node24_ready_github_actions():
    ci = read(".github/workflows/ci.yml")
    for action in ("actions/checkout", "actions/setup-python"):
        match = re.search(rf"uses:\s*{re.escape(action)}@v(\d+)", ci)
        assert match is not None
        assert int(match.group(1)) >= 6


def test_pages_workflow_builds_and_deploys_proof_site_artifact():
    pages = read(".github/workflows/pages.yml")
    build_script = read("scripts/build_pages_artifact.sh")
    verify = read("scripts/verify.sh")

    assert "branches: [main]" in pages
    assert "contents: read" in pages
    assert "pages: write" in pages
    assert "id-token: write" in pages
    assert "name: github-pages" in pages
    assert "url: ${{ steps.deployment.outputs.page_url }}" in pages
    assert "./scripts/build_pages_artifact.sh _site" in pages
    assert "actions/configure-pages@v6" in pages
    assert "enablement: true" in pages
    assert "actions/upload-pages-artifact@v5" in pages
    assert "path: _site" in pages
    assert "actions/deploy-pages@v5" in pages
    assert "scripts/build_pages_artifact.sh" in verify
    assert "pages/reports/voice/report.html" in verify
    assert "pages/openaudio-calculator/index.html" in verify

    for public_path in (
        "site/index.html",
        "site/goal_site.html",
        "reports",
        "openaudio-calculator",
        "site/audio",
    ):
        assert public_path in build_script


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


def test_public_artifacts_do_not_contain_private_machine_markers_or_secret_shapes():
    paths = [
        "README.md",
        "TESTING.md",
        "VERIFICATION.md",
        "CONTRIBUTING.md",
        "GOAL.md",
        "CHANGELOG.md",
        "install.sh",
        ".github/workflows/ci.yml",
        "openaudio-calculator/index.html",
    ]
    paths.extend(f"skills/{skill}/SKILL.md" for skill in SKILLS)
    paths.extend(str(path.relative_to(ROOT)) for path in (ROOT / "data").glob("*.json"))
    paths.extend(str(path.relative_to(ROOT)) for path in (ROOT / "scripts").glob("*.sh"))
    paths.extend(str(path.relative_to(ROOT)) for path in (ROOT / "tests").glob("*.py"))
    paths.extend(str(path.relative_to(ROOT)) for path in (ROOT / "reports").rglob("*.html"))
    paths.extend(str(path.relative_to(ROOT)) for path in (ROOT / "site").glob("*.html"))

    hits = []
    for path in paths:
        text = read(path)
        if any(marker in text for marker in PRIVATE_MARKERS) or any(
            pattern.search(text) for pattern in SECRET_PATTERNS
        ):
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
