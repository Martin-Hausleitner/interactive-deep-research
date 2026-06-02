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
- Hardened README and skill docs with privacy guidance, command output
  contracts, environment contracts, failure-mode tables, and extra Mermaid
  diagrams for packaged-skill usage.
- Hardened `idr` fail-closed behavior for required-live mode and missing
  `askq` scripts.
- Added scorecard spec validation with clean stderr errors and tests.
- Expanded CI-safe CLI coverage for `askq` env/log behavior, `scorecard`
  stdin and malformed specs, IDR report regeneration, and `install.sh` smoke.
- Added documentation and public-artifact contract tests for README Mermaid
  diagrams, packaged-skill docs, layout dedupe, proof-site rendering, and
  private machine marker hygiene.
- Updated GitHub Actions to Node-24-ready major versions and pinned that in the
  documentation contract test.
- Removed internal handoff/cache artifacts and private infrastructure references
  from tracked public docs and proof-site outputs.
