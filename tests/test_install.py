import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_install_links_skills_and_cli_drivers(tmp_path):
    skills_dir = tmp_path / "skills"
    bin_dir = tmp_path / "bin"
    env = {
        **os.environ,
        "CLAUDE_SKILLS_DIR": str(skills_dir),
        "BIN_DIR": str(bin_dir),
        "PYTHONDONTWRITEBYTECODE": "1",
    }

    subprocess.run(
        ["bash", "install.sh"],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=True,
    )

    for skill in (
        "integrative-deep-research",
        "askq",
        "interactive-deep-research",
        "deep-research-scorecard",
    ):
        assert (skills_dir / skill / "SKILL.md").exists()

    for command in ("idr", "askq", "scorecard"):
        driver = bin_dir / command
        assert driver.is_symlink()
        help_result = subprocess.run(
            [str(driver), "--help"],
            cwd=ROOT,
            env=env,
            text=True,
            capture_output=True,
            check=True,
        )
        assert f"usage: {command}" in help_result.stdout
