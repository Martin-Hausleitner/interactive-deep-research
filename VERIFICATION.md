# Verification Ledger

Last updated: 2026-06-03.

## Current Evidence

CI-safe suite:

```bash
PYTHONDONTWRITEBYTECODE=1 pytest -p no:cacheprovider -m "not live" -q
```

Observed result:

```text
17 passed, 1 deselected
```

Live NotebookLM E2E:

```bash
PYTHONDONTWRITEBYTECODE=1 \
IDR_LIVE_E2E=1 \
IDR_REQUIRE_LIVE=1 \
IDR_LIVE_TOPIC="Compact OSS documentation and E2E test strategy for a deterministic NotebookLM-backed CLI pipeline" \
IDR_LIVE_ANSWER="Prioritize CI-safe mock tests, one opt-in live NotebookLM test, clear verification docs, and no personal data." \
pytest -m live tests/test_live_idr_e2e.py -q
```

Observed result:

```text
1 passed in 672.33s (0:11:12)
```

Proof-site render:

```bash
PYTHONDONTWRITEBYTECODE=1 SITE_BUILD_TS="2026-06-03 00:00" python3 site/build_goal_site.py
cp site/goal_site.html site/index.html
```

Observed result:

```text
SITE .../site/goal_site.html 76580 bytes
```

Browser validation:

```bash
python3 -m http.server 5181 --directory site
playwright screenshot --viewport-size=1440,1200 \
  http://127.0.0.1:5181/goal_site.html /tmp/idr-proof-site.png
```

Observed result:

```text
title='Interaktives Deep Research — Verlauf, Output & Beweis'
h1='Verlauf, Output & Beweis'
hasPipeline=True hasVoice=True hasMessaging=True bodyLength=39189
```

Repository hygiene:

```bash
git ls-files | rg '(^|/)__pycache__/|\.pyc$|^(PROGRESS|audio_demos|build_audios|build_goal_site|site_config)\.' || true
find . -path '*/__pycache__/*' -o -name '*.pyc'
```

Observed result: no tracked bytecode, no local bytecode, and no root-level proof-site duplicates.

Public hygiene:

Observed result: no private host/IP, local-path, account, or local-file URL hits
in README, docs, skills, tests, reports, proof-site files, or CI config.

GitHub branch:

```bash
gh repo view Martin-Hausleitner/interactive-deep-research --json defaultBranchRef,nameWithOwner,isPrivate
```

Observed result:

```json
{"defaultBranchRef":{"name":"main"},"isPrivate":true,"nameWithOwner":"Martin-Hausleitner/interactive-deep-research"}
```

## Notes

- The live E2E is opt-in and intentionally excluded from default CI.
- `IDR_REQUIRE_LIVE=1` makes live verification fail closed instead of falling
  back to mock text.
- Proof-site HTML uses repository-relative report paths as text, not local-file
  URL links.
