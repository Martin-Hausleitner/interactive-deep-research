# Changelog

## Unreleased

- Added CI-safe required-live fail-closed contracts for missing NotebookLM
  notebook IDs, query failures, deep-pass failures, and deep-pass `--force`
  startup behavior.

## v0.1.0 - 2026-06-03

Release readiness verified with:

- Public GitHub repository with default branch `main`.
- GitHub Pages proof site deployed from `main`.
- CI-safe verifier passing on `main`.
- Opt-in live NotebookLM E2E passing on `main` with `IDR_REQUIRE_LIVE=1`.
- No tracked or local Python bytecode, root proof-site duplicates, private
  machine markers, or common token-shaped secrets in public artifacts.

- Added `scripts/verify.sh` as the one-command local/CI verifier for syntax,
  non-live tests, deterministic proof-site rendering, layout/bytecode hygiene,
  whitespace checks, and public-artifact private-marker scans.
- Added a GitHub Pages deploy workflow and reusable Pages artifact builder for
  the proof site, reports, audio examples, and OpenAudio calculator.
- Extended `scripts/verify.sh` with common token-shape checks for public
  artifacts.
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
- Hardened README and skill docs with privacy guidance, command output
  contracts, environment contracts, failure-mode tables, and extra Mermaid
  diagrams for packaged-skill usage.
- Hardened `idr` fail-closed behavior for required-live mode and missing
  `askq` scripts.
- Added scorecard spec validation with clean stderr errors and tests.
- Expanded CI-safe CLI coverage for `askq` env/log behavior, `scorecard`
  stdin and malformed specs, IDR report regeneration, and `install.sh` smoke.
- Added CI-safe coverage for the successful `idr run` path through the `askq`
  bridge.
- Strengthened opt-in live E2E assertions for persisted state, deep-pass status,
  same-notebook continuity, and non-empty content artifacts.
- Added documentation and public-artifact contract tests for README Mermaid
  diagrams, packaged-skill docs, layout dedupe, proof-site rendering, and
  private machine marker hygiene.
- Updated GitHub Actions to Node-24-ready major versions and pinned that in the
  documentation contract test.
- Removed internal handoff/cache artifacts and private infrastructure references
  from tracked public docs and proof-site outputs.
- Expanded public-artifact hygiene checks to include scorecard data and
  install/verification scripts.
