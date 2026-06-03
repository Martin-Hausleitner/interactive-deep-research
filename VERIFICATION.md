# Verification Ledger

Last updated: 2026-06-03.

## Current Evidence

CI-safe suite:

```bash
./scripts/verify.sh
```

Observed result:

```text
27 passed, 1 deselected
verify: ok
```

GitHub Actions CI:

```text
Run: 26856120643
SHA: 0e5af03f1738ab506b1da488f918379dba0c1a8f
Conclusion: success
Log evidence: 27 passed, 1 deselected; verify: ok
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
./scripts/build_pages_artifact.sh _site
```

Observed result:

```text
SITE .../site/goal_site.html 76580 bytes
pages artifact: _site
```

Browser validation:

```bash
python3 -m http.server 5191 --directory _site
Google Chrome --headless --screenshot=/tmp/idr-pages-artifact.png http://127.0.0.1:5191/
```

Observed result:

```text
title='Interaktives Deep Research — Verlauf, Output & Beweis'
h1='Verlauf, Output & Beweis'
hasPipeline=True hasVoice=True hasMessaging=True bodyLength=39189
```

GitHub Pages remote deployment:

```text
Run: 26856120640
SHA: 0e5af03f1738ab506b1da488f918379dba0c1a8f
URL: https://martin-hausleitner.github.io/interactive-deep-research/
Conclusion: success
Artifact: index.html, goal_site.html, reports/, audio/, openaudio-calculator/
```

Remote validation:

```text
HTTP 200
title='Interaktives Deep Research — Verlauf, Output & Beweis'
hasPipeline=True hasVoice=True hasMessaging=True
reports/voice/report.html HTTP 200
screenshot=/tmp/idr-pages-remote.png
```

Repository hygiene:

```bash
git ls-files | rg '(^|/)__pycache__/|\.pyc$|^(PROGRESS|audio_demos|build_audios|build_goal_site|site_config)\.' || true
find . -path '*/__pycache__/*' -o -name '*.pyc'
```

Observed result: no tracked bytecode, no local bytecode, and no root-level proof-site duplicates.

Public hygiene:

Observed result: no private host/IP, local-path, account, or local-file URL hits
and no common token-shaped secret hits in README, docs, skills, tests, reports,
proof-site files, scorecard data, scripts, or CI config.

GitHub repository:

```bash
gh repo view Martin-Hausleitner/interactive-deep-research --json defaultBranchRef,nameWithOwner,isPrivate,visibility,homepageUrl
```

Observed result:

```json
{"defaultBranchRef":{"name":"main"},"homepageUrl":"https://martin-hausleitner.github.io/interactive-deep-research/","isPrivate":false,"nameWithOwner":"Martin-Hausleitner/interactive-deep-research","visibility":"PUBLIC"}
```

## Notes

- The live E2E is opt-in and intentionally excluded from default CI.
- `IDR_REQUIRE_LIVE=1` makes live verification fail closed instead of falling
  back to mock text.
- Proof-site HTML uses repository-relative report paths as text, not local-file
  URL links.
