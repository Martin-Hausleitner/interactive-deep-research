# Changelog

## Unreleased

- Removed duplicated proof-site inputs from the repository root; `site/` is the
  canonical source for proof-site build data.
- Removed tracked Python bytecode artifacts from the Git index.
- Reworked the README with Mermaid diagrams for the IDR pipeline and skill/CLI
  invocation flow.
- Documented all packaged skills: `interactive-deep-research`,
  `integrative-deep-research`, `askq`, and `deep-research-scorecard`.
- Added `scorecard` installation support in `install.sh`.
- Made the proof-site builder render from repository artifacts when local IDR
  run state is unavailable.
- Added pytest coverage for mock IDR E2E, parser helpers, `askq`, `scorecard`,
  proof-site rendering, and an opt-in live NotebookLM E2E test.
- Added `IDR_RUNS_DIR`, `ASKQ_SCRIPT`, and `IDR_REQUIRE_LIVE` contracts so tests
  can isolate artifacts and live verification fails closed.
- Added contributor, testing, CI, and verification docs for the mock/live E2E
  matrix and proof-site evidence.
