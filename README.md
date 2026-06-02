# Interactive Deep Research — Verlauf, Output & Beweis

Supervised, multi-round, cross-engine deep research with proof, scored feature-matrices,
and a chronological reasoning trace. Two worked examples + the reusable skills.

**Live site:** http://100.120.120.120:5181/ (served from `site/index.html`)

## Examples
- **A · Open-Source Voice Cloning (DE+EN):** 7 rounds (agy waypoint → NotebookLM Fast → Rückfrage → NotebookLM Deep + Web engines → emotion → license-agnostic re-score). Winner depends on constraint:
  - License irrelevant (just OSS): **OpenAudio S1/S2 (Fish-Speech)** — #1 TTS-Arena, richest emotion tags, native DE.
  - Permissive/commercial wanted: **CosyVoice 3.0 (Apache)** — only published German head-to-head; **Chatterbox Multilingual (MIT)**.
  - IndexTTS-2 = SOTA emotion but no German → disqualified.
- **B · Cross-Channel Messaging-Automation:** NotebookLM Deep (111 sources). Best self-build: **Matrix + Mautrix bridges + GoLogin + Claude Computer Use** (~$30–60/mo).

## Reusable skills (`skills/`)
- **deep-research-scorecard** — points-scored, weighted feature-matrix that crowns a winner with justification (`scorecard spec.json [--html]`).
- **integrative-deep-research** — deterministic, token-frugal pipeline: agy → NotebookLM fast/deep → askq HITL → HTML report (`idr`).
- **askq** — human-in-the-loop question bridge.

## Layout
- `site/index.html` — the polished presentation site (exec summary, scorecards, comparison tables w/ benchmarks + GitHub links, Gedankenverlauf timeline, Q&A).
- `reports/{voice,messaging}/` — per-example report.html + source content.
- `data/*.json` — scorecard specs (criteria, weights, scores).
- `build_goal_site.py` — data-driven site generator.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
