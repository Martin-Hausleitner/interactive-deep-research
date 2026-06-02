# HANDOFF — interactive-deep-research → Codex

> **You are a fresh Codex session with ZERO prior context.** This file is your
> complete brief. Read it top to bottom. Repo: `~/code/interactive-deep-research`,
> GitHub `Martin-Hausleitner/interactive-deep-research` (private).
> Author of this handoff: the origin Claude session that built the system.

---

## 0. TL;DR — Your job

1. **Clean up the repo layout** (remove tracked `*.pyc`/`__pycache__`; resolve root↔`site/` duplicates).
2. **Write a modern README** with a Mermaid diagram covering *both* (a) how the pipeline works and (b) how to invoke the skills/CLI.
3. **Document/round out the skills** so each is clean and self-describing.
4. **Commit + push** to `Martin-Hausleitner/interactive-deep-research`, and **make `main` the default branch** (currently `master`).

There are **13 unpushed local commits** on `main`, including the unmerged-to-origin
merge `763f399`. Push them. Do **not** start a new research run — the system is
already proven working (see §4).

---

## 1. What "iterative / integrative deep research" IS (the `idr` pipeline)

A **deterministic, token-frugal** human-in-the-loop research pipeline. The key
idea: **NotebookLM does all the heavy LLM reasoning** (source discovery, analysis,
synthesis); our code only orchestrates and renders. The final HTML report is built
**locally with 0 LLM tokens**.

Pipeline (this is the canonical flow — keep it in the README Mermaid):

```
agy seed (scoping brief)
  → NotebookLM FAST research pass   (--auto-import; quick source discovery)
  → ONE clarifying question to a human   (via the askq CLI — exactly one, deferred)
  → NotebookLM DEEP research pass   (--force --auto-import, SAME notebook, answer as context)
  → fixed query-angles   (overview / comparison-table / recommendation)
  → self-contained HTML report   (local render, mermaid diagram, 0 LLM tokens)
```

Why each piece:
- **agy waypoint** = local Antigravity CLI seeds a scoping brief so the NotebookLM
  notebook starts focused.
- **fast pass** = cheap breadth; discovers sources.
- **one askq question** = the only human interruption; keeps it interactive but not chatty.
- **deep pass on the SAME notebook** = depth, conditioned on the human's answer.
- **fixed angles** = determinism (always the same 3 queries → reproducible reports).
- **local HTML render** = no tokens spent on formatting.

---

## 2. The skills in this repo

| Skill | CLI / path | Role |
| --- | --- | --- |
| `integrative-deep-research` | `idr` → `skills/integrative-deep-research/scripts/idr.py` | **Driver.** Implements the whole pipeline. |
| `askq` | `askq` → `skills/askq/scripts/askq.py` | Human-in-the-loop question bridge (JSON stdout + `~/.askq/history.jsonl` audit log). |
| `interactive-deep-research` | `skills/interactive-deep-research/SKILL.md` | **Umbrella** guide that ties the engines together (orchestration playbook, no code). |
| `deep-research-scorecard` | `scorecard` → `skills/deep-research-scorecard/scripts/scorecard.py` | Turns candidates into a weighted Σ/100 ranking, crowns a winner with justification; `--html` for embeddable fragment. |

CLI surface (all dependency-free Python 3):
- `idr plan "<topic>"` → runs agy seed + fast pass, returns `{run_id, rundir, notebook_id, question}` (the clarifying question).
- `idr resume <run_id> --answer "<text>"` → runs deep pass + angle queries + renders `report.html`, returns `{run_id, report, notebook_id}`.
- `idr run "<topic>" --answer "<text>"` → plan+resume in one shot (skips the human pause; for automation/tests).
- **`IDR_MOCK=1`** → fully offline mock (no agy, no NotebookLM); use for CI/e2e smoke tests. **Verified working** (see §4).

The on-PATH symlinks live at `~/.local/bin/{idr,askq}` → into `~/.claude/skills/...`.
NOTE: the **source of truth is `~/.claude/skills/`**; the copies in this repo's
`skills/` are the packaged/distributable versions. `install.sh` wires them up.

---

## 3. Exact repo state (read carefully before touching git)

**Branches:** local `main` is the working branch. `origin/HEAD → master` — i.e. the
GitHub **default branch is still `master`** and must become `main`.
`origin/main` exists but is **13 commits behind** local `main`.

**Unpushed:** local `main` is **+13 ahead** of `origin/main`. The most important
unpushed commit is the merge **`763f399`** ("unite session research output … with
packaged skills + agy README"). Everything is committed (clean working tree) — just unpushed.

**Tracked junk that must be removed from the index** (`.gitignore` already lists them,
but they were committed *before* the ignore rule, so they persist):
```
skills/askq/scripts/__pycache__/askq.cpython-314.pyc
skills/integrative-deep-research/scripts/__pycache__/idr.cpython-314.pyc
```
→ `git rm -r --cached` them (and any `__pycache__` dirs), then commit.

**Duplicate files — root vs `site/`** (same content, two locations; pick `site/` as
canonical and delete the root copies, OR vice-versa, but be consistent):
```
build_goal_site.py   ↔ site/build_goal_site.py
build_audios.py      ↔ site/build_audios.py
audio_demos.json     ↔ site/audio_demos.json
PROGRESS.md          ↔ site/PROGRESS.md
site_config.json     ↔ site/site_config.json
```
Recommendation: keep the **`site/`** copies (they are the proof-site build inputs)
and remove the root duplicates; update any path references.

**Full tracked layout:**
```
.gitignore  LICENSE  README.md  PROGRESS.md  install.sh
build_goal_site.py  build_audios.py  audio_demos.json  site_config.json   # ← root dupes
skills/
  integrative-deep-research/{SKILL.md, scripts/idr.py}      # driver
  askq/{SKILL.md, scripts/askq.py}                          # human bridge
  deep-research-scorecard/{SKILL.md, scripts/scorecard.py}  # winner-crowning
  interactive-deep-research/SKILL.md                        # umbrella (no code)
site/                          # the live proof-site (examples A + B); deployed to vcvm:5181
  build_goal_site.py  build_audios.py  audio_demos.json  site_config.json  PROGRESS.md  audio/
reports/
  voice/{report.html, content/}      # Example A: DE/EN voice cloning
  messaging/{report.html, content/}  # Example B: cross-channel messaging
data/
  voice_scorecard.json  messaging_scorecard.json   # scorecard specs for the two examples
openaudio-calculator/
  index.html  research/business_roi.md   # ⚠ SIDE-TANGENT — NOT part of the idr core; see note below
cache/
```
> ⚠ **`openaudio-calculator/` is a side-tangent** (an OpenAudio S2 Pro business/pricing
> calculator) that is *not* part of the iterative-deep-research core. It can stay in the
> repo as an example artifact, but the README and skill docs should be about the **idr
> pipeline**, not the calculator. Don't expand it.

**Two worked examples** (the proof that the pipeline produces real output):
- **A — Open-source DE/EN voice cloning** → `reports/voice/`, scorecard `data/voice_scorecard.json`. Winner: **CosyVoice 3.0** (German support is the binding criterion, not license).
- **B — Cross-channel messaging stack** → `reports/messaging/`, scorecard `data/messaging_scorecard.json`.

Both are rendered together into the proof site (`site/build_goal_site.py`) and are
**live at http://100.120.120.120:5181/** (vcvm tailnet; served from
`/home/coder/goal_deepresearch_site/index.html`). Title: *"Interaktives Deep Research — Verlauf, Output & Beweis"*.

---

## 4. Live learnings (hard-won — bake these into the code/docs, don't relearn them)

1. **`nlm query` returns JSON, not raw text.** Parse `.value.answer`. (Naive parsing
   returns a literal `{`.)
2. **The deep pass needs `--force`.** Without it NotebookLM shows an interactive
   `Continue? [y/N]` prompt that aborts a headless run.
3. **`fast --auto-import` returns BEFORE sources are actually imported.** You must
   poll `nlm research status --max-wait <s>` and then explicitly `nlm research import`,
   or the notebook has 0 sources and you get a canned fallback question.
4. **`agy` prepends a Gemini/Antigravity status line** ("🚀 Starting …"). Strip the
   first noise line(s) from its stdout before using the output.
5. **Keep query prompts topic-anchored** (prefix with `Topic: <topic>`) — otherwise the
   fixed angles drift and pull in unrelated context (this caused an early HITL-content bleed).
6. **`nlm`** = the NotebookLM CLI (v0.6.13). `agy` = headless Antigravity at
   `~/.local/bin/agy`, invoked `agy -p "<prompt>" --dangerously-skip-permissions`.
   Both require one-time browser login already done on this machine.
7. Quotas: NotebookLM ~50 queries/day, 429 backoff up to ~900s. `IDR_MOCK=1` avoids all of it.

**e2e verification just run (mock mode), all green:**
```
IDR_MOCK=1 idr plan "Best open-source DE+EN voice cloning stack 2026"
  → returns a real clarifying question (askq)
IDR_MOCK=1 idr resume <run_id> --answer "Prioritize self-hostable open-source; exclude SaaS."
  → writes content/{overview,comparison,recommendation}.md and a 5.9 KB report.html
    (self-contained, mermaid, 0 LLM tokens). state.json phase → done.
```

---

## 5. Your concrete task list (Codex)

- [ ] **a) Clean layout:**
  - `git rm -r --cached` the two tracked `*.pyc` + their `__pycache__` dirs; commit.
  - De-duplicate root vs `site/` (keep `site/`, remove root copies, fix references). Commit.
- [ ] **b) Modern README** (`README.md` — there's an agy-generated one already; modernize it):
  - A **Mermaid flowchart** of the pipeline (agy → fast → askq → deep → angles → HTML).
  - A second short section / diagram on **how to invoke** the skills & CLI (`idr plan/resume/run`, `IDR_MOCK=1`, `askq`, `scorecard`).
  - Quickstart, the two worked examples (link the live `:5181` site), and the §4 gotchas as a "Notes / gotchas" section.
- [ ] **c) Skill docs:** ensure each `SKILL.md` is accurate and self-contained; tighten the
  `interactive-deep-research` umbrella to describe orchestration; optionally add a tiny
  `IDR_MOCK=1` smoke-test note for contributors.
- [ ] **d) Ship it:**
  - Commit your changes.
  - `git push origin main` (pushes the 13 + your new commits).
  - On GitHub: set **default branch to `main`** (`gh api -X PATCH repos/Martin-Hausleitner/interactive-deep-research -f default_branch=main`), then optionally delete `master`.

Then **STOP** — the origin session hands off here.

---

## 6. Quick environment reference

- Python 3 (skills are dependency-free, stdlib only).
- `nlm` CLI on PATH (NotebookLM). `agy` at `~/.local/bin/agy` (Antigravity headless).
- `~/.local/bin/{idr,askq}` symlink into `~/.claude/skills/...` (source of truth).
- Run artifacts: `~/.local/share/idr/runs/<run_id>/{state.json, content/*.md, report.html}` (gitignored).
- Proof site host: vcvm, tailnet `100.120.120.120`, `ssh vcvm`; site root `/home/coder/goal_deepresearch_site/`, served by `python3 -m http.server 5181`.
- GitHub: `gh` CLI authenticated; repo `Martin-Hausleitner/interactive-deep-research` (private).
