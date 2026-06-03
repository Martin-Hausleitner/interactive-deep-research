#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export PYTHONDONTWRITEBYTECODE=1
export SITE_BUILD_TS="${SITE_BUILD_TS:-2026-06-03 00:00}"

tmp_pycache="$(mktemp -d)"
cleanup() {
  rm -rf "$tmp_pycache"
}
trap cleanup EXIT

PYTHONPYCACHEPREFIX="$tmp_pycache" python3 -B -m py_compile \
  skills/integrative-deep-research/scripts/idr.py \
  skills/askq/scripts/askq.py \
  skills/deep-research-scorecard/scripts/scorecard.py \
  site/build_goal_site.py \
  site/build_audios.py

pytest -p no:cacheprovider -m "not live"

python3 site/build_goal_site.py
test -s site/goal_site.html
test -s site/index.html

python3 - <<'PY'
from pathlib import Path

pages = {
    "site/goal_site.html": Path("site/goal_site.html").read_text(encoding="utf-8"),
    "site/index.html": Path("site/index.html").read_text(encoding="utf-8"),
}
required = (
    "<title>Interaktives Deep Research",
    "Verlauf, Output &amp; Beweis",
    "Pipeline-Flow",
    "Voice Cloning",
    "Cross-Channel Messaging",
    "reports/voice/report.html",
    "reports/messaging/report.html",
)
missing = [
    f"{path}: {marker}"
    for path, html in pages.items()
    for marker in required
    if marker not in html
]
if missing:
    raise SystemExit(f"verify: proof site missing markers: {missing}")
PY

git diff --check

if git ls-files | grep -E '(^|/)__pycache__/|\.pyc$|^(PROGRESS|audio_demos|build_audios|build_goal_site|site_config)\.'; then
  echo "verify: tracked bytecode or root-level proof-site duplicates found" >&2
  exit 1
fi

local_bytecode="$(
  find . -path './.git' -prune -o \
    \( -path '*/__pycache__/*' -o -name '*.pyc' -o -name '*.pyo' \) -print
)"
if [ -n "$local_bytecode" ]; then
  echo "$local_bytecode" >&2
  echo "verify: local Python bytecode artifacts found" >&2
  exit 1
fi

private_markers=(
  "100"".120"
  "510""7"
  "510""5"
  "518""2"
  "file""://"
  "/Users/""mh"
  "Account"":"
  "mart""iking"
  "vc""vm"
  "tail""net"
)

secret_patterns=(
  "sk-"'[A-Za-z0-9_-]{20,}'
  "ghp_"'[A-Za-z0-9_]{20,}'
  "AK""IA[0-9A-Z]{16}"
)

public_files() {
  find README.md TESTING.md VERIFICATION.md CONTRIBUTING.md GOAL.md CHANGELOG.md \
    install.sh .github skills tests data reports site openaudio-calculator scripts \
    \( -path 'site/audio/*' -o -name '*.wav' -o -name '*.flac' -o -name '*.mp3' -o -name '*.aac' \) -prune \
    -o -type f -print0
}

for marker in "${private_markers[@]}"; do
  while IFS= read -r -d '' file; do
    if grep -n -F "$marker" "$file"; then
      echo "verify: private machine marker found in public artifacts" >&2
      exit 1
    fi
  done < <(public_files)
done

for pattern in "${secret_patterns[@]}"; do
  while IFS= read -r -d '' file; do
    if grep -n -E "$pattern" "$file"; then
      echo "verify: possible secret token found in public artifacts" >&2
      exit 1
    fi
  done < <(public_files)
done

echo "verify: ok"
