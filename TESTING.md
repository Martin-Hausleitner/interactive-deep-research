# Testing

The repository has two test tiers:

- CI-safe tests that never call NotebookLM or Antigravity.
- Opt-in live E2E tests that run the real `nlm` fast+deep path and spend quota.

## CI-Safe Checks

```bash
./scripts/verify.sh
```

The verifier runs syntax checks, `PYTHONDONTWRITEBYTECODE=1 pytest -p
no:cacheprovider -m "not live"`, deterministic proof-site rendering with a fixed
`SITE_BUILD_TS`, `git diff --check`, layout dedupe checks, local/tracked bytecode
checks, private machine marker scans, and common token-shape checks. Default CI
calls the same script.

Coverage:

- `IDR_MOCK=1` plan -> question -> resume -> report.
- `IDR_MOCK=1 idr run` through the `askq` bridge with an isolated answer stub.
- `nlm query` JSON answer parsing.
- Notebook ID extraction.
- Required-live fail-closed behavior for missing NotebookLM notebook IDs, query
  failures, deep-pass failures, and deep-pass `--force` startup.
- `askq` non-interactive JSON mode, `ASKQ_ANSWER`, choices, custom logs, and
  no-question usage errors.
- `scorecard` Markdown, HTML, stdin, malformed JSON, and schema errors.
- `install.sh` smoke test with isolated skill/bin directories.
- `idr report <run_id>` regeneration from existing run content.
- Proof-site rebuild from tracked repo artifacts.
- README/Skill documentation contract: Mermaid pipeline + skill invocation,
  privacy/failure-mode sections, install coverage, layout dedupe, and no private
  machine markers or common token-shaped secrets in public artifacts, including
  scorecard data and install/verification scripts.
- CI workflow contract: GitHub-owned actions must use Node-24-ready major
  versions so default CI stays ahead of hosted-runner deprecations.

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
- `state.json` has `phase: "done"`, `mock: false`, `deep.ok: true`, and the
  same real `notebook_id` returned by `idr plan`.
- Record the exact git branch and SHA used for the live run.
- Record that `IDR_REQUIRE_LIVE=1` was set and `IDR_MOCK` was unset.
- Record the live `run_id`, `notebook_id`, artifact list, content sizes, and
  report proof in `VERIFICATION.md`.

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

Exact Pages artifact:

```bash
./scripts/build_pages_artifact.sh _site
python3 -m http.server 5181 --directory _site
```

Then open:

```text
http://127.0.0.1:5181/
```

Expected: HTTP 200, the same proof-site title, both worked examples, the
Pipeline-Flow section, `reports/voice/report.html`,
`reports/messaging/report.html`, `audio/`, and `openaudio-calculator/`.

After GitHub Pages deploys, verify the published URL:

```text
https://martin-hausleitner.github.io/interactive-deep-research/
```

Expected: HTTP 200, title `Interaktives Deep Research — Verlauf, Output &
Beweis`, both worked examples, and the Pipeline-Flow section.
