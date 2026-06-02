# Testing

The repository has two test tiers:

- CI-safe tests that never call NotebookLM or Antigravity.
- Opt-in live E2E tests that run the real `nlm` fast+deep path and spend quota.

## CI-Safe Checks

```bash
python3 -m py_compile \
  skills/integrative-deep-research/scripts/idr.py \
  skills/askq/scripts/askq.py \
  skills/deep-research-scorecard/scripts/scorecard.py \
  site/build_goal_site.py \
  site/build_audios.py

pytest -m "not live"
```

Coverage:

- `IDR_MOCK=1` plan -> question -> resume -> report.
- `nlm query` JSON answer parsing.
- Notebook ID extraction.
- `askq` non-interactive JSON mode.
- `scorecard` Markdown and HTML output.
- Proof-site rebuild from tracked repo artifacts.

## Live NotebookLM E2E

Live E2E is intentionally opt-in because it requires browser-authenticated
NotebookLM and consumes quota.

```bash
nlm doctor
IDR_LIVE_E2E=1 pytest -m live tests/test_live_idr_e2e.py
```

Optional environment:

```bash
IDR_LIVE_TOPIC="Compact OSS test strategy for a deterministic NotebookLM CLI pipeline"
IDR_LIVE_ANSWER="Prioritize CI-safe tests plus one opt-in live E2E."
IDR_RUNS_DIR=/tmp/idr-live-runs
IDR_REQUIRE_LIVE=1
```

Expected evidence:

- Test output shows `tests/test_live_idr_e2e.py` passed.
- The test's temporary run directory contains `state.json`, three
  `content/*.md` files, and `report.html`.
- `state.json` has `phase: "done"` and a real `notebook_id`.

Do not enable live E2E in default CI unless credentials and quotas are explicitly
provisioned.

## Proof Site

```bash
python3 site/build_goal_site.py
python3 -m http.server 5181 --directory site
```

Then open:

```text
http://127.0.0.1:5181/goal_site.html
```

The title must be `Interaktives Deep Research — Verlauf, Output & Beweis`, and
the page should show both worked examples plus the Pipeline-Flow section.
