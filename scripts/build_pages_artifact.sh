#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONDONTWRITEBYTECODE=1

out="${1:-_site}"
rm -rf "$out"
mkdir -p "$out"

python3 site/build_goal_site.py

cp site/index.html "$out/index.html"
cp site/goal_site.html "$out/goal_site.html"
cp -R reports "$out/reports"
cp -R openaudio-calculator "$out/openaudio-calculator"
cp -R site/audio "$out/audio"

python3 - "$out" <<'PY'
import sys
from pathlib import Path

out = Path(sys.argv[1])
required = [
    out / "index.html",
    out / "goal_site.html",
    out / "reports" / "voice" / "report.html",
    out / "reports" / "messaging" / "report.html",
    out / "openaudio-calculator" / "index.html",
]
missing = [str(path) for path in required if not path.is_file() or path.stat().st_size == 0]
if missing:
    raise SystemExit(f"pages artifact missing files: {missing}")
if (out / "index.html").read_text(encoding="utf-8") != (
    out / "goal_site.html"
).read_text(encoding="utf-8"):
    raise SystemExit("pages artifact index.html and goal_site.html differ")
print(f"pages artifact: {out}")
PY
