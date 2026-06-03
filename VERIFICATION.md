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
Run: 26856251600
Branch: main
SHA: de264255019b2e69e14045611c8c60f4ab2ac74f
Conclusion: success
Log evidence: 27 passed, 1 deselected; verify: ok
```

Live NotebookLM E2E:

```bash
PYTHONDONTWRITEBYTECODE=1 \
IDR_LIVE_E2E=1 \
IDR_REQUIRE_LIVE=1 \
IDR_LIVE_TOPIC="Compact public OSS release checklist for a deterministic NotebookLM-backed CLI pipeline" \
IDR_LIVE_ANSWER="Prioritize public proof-site evidence, CI-safe mock tests, one live E2E proof, branch hygiene, and no personal data." \
pytest -q -s -m live tests/test_live_idr_e2e.py --basetemp /tmp/idr-live-current
```

Observed result:

```text
Date: 2026-06-03
Branch: main
SHA: de264255019b2e69e14045611c8c60f4ab2ac74f
Run id: 20260603-023238-bb7f
Notebook ID: bebfe750-5de9-41f5-a707-29a0ed73971d
State proof: mock=false, phase=done, deep.ok=true, same notebook_id from plan/resume
Artifacts: state.json, content/overview.md, content/comparison.md, content/recommendation.md, report.html
Content sizes: overview=3448 bytes, comparison=3745 bytes, recommendation=2751 bytes, report=15558 bytes
Test result: 1 passed in 651.95s (0:10:51)
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
Run: 26856251583
Branch: main
SHA: de264255019b2e69e14045611c8c60f4ab2ac74f
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
git ls-remote --heads origin
git branch -r --verbose
```

Observed result:

```json
{"defaultBranchRef":{"name":"main"},"homepageUrl":"https://martin-hausleitner.github.io/interactive-deep-research/","isPrivate":false,"nameWithOwner":"Martin-Hausleitner/interactive-deep-research","visibility":"PUBLIC"}
```

```text
Remote HEAD: refs/heads/main
Remote branches: main only
origin/HEAD -> origin/main
```

Release readiness:

```text
Target release: v0.1.0
Status: ready to tag after this ledger update lands on main and CI/Pages pass
Release basis: public repository, default branch main, live E2E pass, CI pass,
Pages pass, remote proof-site HTTP 200, and public-artifact hygiene pass
```

## Notes

- The live E2E is opt-in and intentionally excluded from default CI.
- `IDR_REQUIRE_LIVE=1` makes live verification fail closed instead of falling
  back to mock text.
- Proof-site HTML uses repository-relative report paths as text, not local-file
  URL links.
