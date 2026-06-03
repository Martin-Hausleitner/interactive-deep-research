# Feature Matrix

This matrix tracks the public surface of Interactive Deep Research from repo
evidence only. Status values are intentionally limited to `Done`, `Ready`,
`Blocked`, and `Planned`.

| Bereich | Feature / Rasterpunkt | Status | Aktivitaet / Reifegrad | Beleg / Dateien | Naechster Schritt |
| --- | --- | --- | --- | --- | --- |
| Pipeline | Phased IDR flow: `idr plan` -> one question -> `idr resume` -> `report.html` | Done | Active; release-ready core path | `skills/integrative-deep-research/scripts/idr.py`, `tests/test_idr_pipeline.py`, `README.md` | Keep output contract stable while adding new report sections. |
| Pipeline | Terminal-only loop through `idr run` and the `askq` bridge | Done | Active; useful for local operator runs | `tests/test_idr_pipeline.py`, `skills/askq/scripts/askq.py`, `skills/integrative-deep-research/SKILL.md` | Keep agent workflows on phased `plan/resume`; use `idr run` for terminal sessions. |
| Pipeline | Deterministic local report regeneration via `idr report` | Done | Active; mature recovery path | `tests/test_idr_pipeline.py`, `skills/integrative-deep-research/scripts/idr.py` | Preserve regeneration from existing `content/*.md` without live dependencies. |
| Research backend | NotebookLM fast pass, import/status wait, deep pass with `--force` | Done | Active; live-capable with external auth and quota | `skills/integrative-deep-research/scripts/idr.py`, `tests/test_live_idr_e2e.py`, `VERIFICATION.md` | Re-run opt-in live E2E before release claims or backend changes. |
| Research backend | Required-live fail-closed mode (`IDR_REQUIRE_LIVE=1`) | Done | Active; mature safety guard | `tests/test_idr_pipeline.py`, `tests/test_live_idr_e2e.py`, `TESTING.md` | Keep rejecting mock fallback, malformed query JSON, and deep-pass failures. |
| Research backend | Default live E2E in CI | Blocked | Guarded by design; external credentials, network, and quota required | `TESTING.md`, `scripts/verify.sh`, `.github/workflows/ci.yml` | Only enable in CI if credentials, quota limits, and non-sensitive synthetic topics are provisioned. |
| Mocking | `IDR_MOCK=1` offline smoke and CI path | Done | Active; mature contributor path | `tests/test_idr_pipeline.py`, `README.md`, `TESTING.md` | Use for all default verification and documentation examples. |
| Human bridge | `askq` JSON question/answer bridge with choices, logs, and `ASKQ_ANSWER` | Done | Active; stable CLI contract | `skills/askq/scripts/askq.py`, `tests/test_askq_scorecard.py`, `skills/askq/SKILL.md` | Keep default logs out of sensitive workflows via `--no-log` or isolated `--log`. |
| Scoring | Weighted scorecard CLI with Markdown and HTML output | Done | Active; mature comparison helper | `skills/deep-research-scorecard/scripts/scorecard.py`, `tests/test_askq_scorecard.py`, `data/voice_scorecard.json`, `data/messaging_scorecard.json` | Add new scorecard specs beside new worked examples. |
| Skills | Packaged skill bundle: umbrella, IDR, askq, scorecard | Done | Active; source release `v0.1.0` | `skills/interactive-deep-research/SKILL.md`, `skills/integrative-deep-research/SKILL.md`, `skills/askq/SKILL.md`, `skills/deep-research-scorecard/SKILL.md`, `install.sh` | Keep skill docs aligned with CLI flags and environment variables. |
| Install | Source installer for skills and CLI symlinks | Done | Active; source-installed distribution | `install.sh`, `tests/test_install.py`, `README.md` | Maintain isolated install smoke tests for `CLAUDE_SKILLS_DIR` and `BIN_DIR`. |
| Distribution | Package-manager release | Planned | Not active; explicitly not shipped for `v0.1.0` | `README.md`, `skills/interactive-deep-research/SKILL.md` | Decide whether a package is worth the maintenance cost after source release usage is proven. |
| Verification | `scripts/verify.sh` CI-safe gate | Done | Active; mature local and CI gate | `scripts/verify.sh`, `.github/workflows/ci.yml`, `TESTING.md`, `VERIFICATION.md` | Keep fast enough for default CI; leave live checks opt-in. |
| Verification | Public hygiene scan for private markers and token-shaped secrets | Done | Active; mature release hygiene | `scripts/verify.sh`, `tests/test_docs_contract.py`, `VERIFICATION.md` | Extend marker coverage when new artifact types are added. |
| Proof site | Local proof-site renderer from tracked examples | Done | Active; release proof path | `site/build_goal_site.py`, `site/site_config.json`, `site/index.html`, `site/goal_site.html`, `tests/test_site_build.py` | Rebuild with fixed `SITE_BUILD_TS` before publishing evidence. |
| Proof site | GitHub Pages artifact build | Ready | Active; deployable artifact path | `scripts/build_pages_artifact.sh`, `scripts/verify.sh`, `VERIFICATION.md` | Validate the rendered artifact locally before linking or publishing. |
| Worked examples | Voice cloning report and scorecard | Done | Active; proof artifact | `reports/voice/report.html`, `reports/voice/content/`, `data/voice_scorecard.json` | Refresh only with synthetic, publishable evidence. |
| Worked examples | Cross-channel messaging report and scorecard | Done | Active; proof artifact | `reports/messaging/report.html`, `reports/messaging/content/`, `data/messaging_scorecard.json` | Refresh only with synthetic, publishable evidence. |
| Side artifacts | OpenAudio calculator and audio demo assets | Ready | Supporting artifact; outside core IDR pipeline | `openaudio-calculator/index.html`, `openaudio-calculator/research/business_roi.md`, `site/audio_demos.json`, `site/audio/` | Keep linked from the Pages artifact; avoid coupling it to core `idr` tests. |
| Documentation | README as GitHub landing page | Done | Active; contract-tested overview | `README.md`, `tests/test_docs_contract.py` | Keep the top matrix link and the two Mermaid contract sections intact. |
| Documentation | Feature matrix with status, maturity, evidence, and next step | Done | Active; current release map | `docs/FEATURE_MATRIX.md` | Update whenever status changes, especially after new proof runs or distribution work. |
| Security / privacy | Public use guidance and vulnerability process | Done | Active; documented guardrails | `SECURITY.md`, `README.md`, `TESTING.md`, `VERIFICATION.md` | Keep sensitive topics, credentials, local paths, and private customer data out of committed artifacts. |

## Status Legend

| Status | Meaning in this repo |
| --- | --- |
| Done | Implemented, tested or documented, and represented by tracked files. |
| Ready | Usable now, but dependent on an operator action such as deploy, auth, or rebuild. |
| Blocked | Intentionally not enabled because an external dependency or operational policy is missing. |
| Planned | Not implemented in the current source release; tracked as a possible future extension. |

## Maturity Notes

- Default verification is intentionally mock-safe and CI-safe.
- Live NotebookLM verification exists and is documented, but remains opt-in.
- The proof site is built from tracked repository artifacts, not from private
  local run directories.
- The `v0.1.0` distribution model is source install via `./install.sh`; there
  is no package-manager release in this repository state.
