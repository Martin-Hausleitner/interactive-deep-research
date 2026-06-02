# Interactive Deep Research

[![CI](https://github.com/Martin-Hausleitner/interactive-deep-research/actions/workflows/ci.yml/badge.svg)](https://github.com/Martin-Hausleitner/interactive-deep-research/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)

Deterministic, token-frugal deep research with one human clarification step.
NotebookLM does the heavy research and synthesis; this repository provides the
local orchestration, question bridge, scorecard utility, packaged skills, and
self-contained HTML report rendering.

The core idea is simple: keep the orchestrator rigid and cheap, delegate the
research reasoning to NotebookLM, then render the final report locally with
0 formatting tokens.

## Pipeline

```mermaid
flowchart TD
    A["agy seed<br/>local scoping brief"] --> B["NotebookLM FAST pass<br/>--auto-import source discovery"]
    B --> C["Poll status + import<br/>ensure sources landed"]
    C --> D["ONE clarifying question<br/>askq or chat relay"]
    D --> E["NotebookLM DEEP pass<br/>--force --auto-import<br/>same notebook, answer as context"]
    E --> F["Fixed query angles<br/>overview / comparison table / recommendation"]
    F --> G["Self-contained report.html<br/>local render, Mermaid, 0 LLM tokens"]
```

Why this shape:

- `agy` produces a short scoping waypoint before NotebookLM starts.
- The fast pass gets breadth and source discovery without committing to a full run.
- `askq` creates exactly one human-in-the-loop pause.
- The deep pass runs on the same notebook, with the human answer folded in.
- Fixed query angles make output reproducible across topics.
- HTML rendering is local and dependency-free.

## Skills And CLIs

```mermaid
flowchart LR
    U["interactive-deep-research<br/>umbrella playbook"] --> I["integrative-deep-research<br/>idr plan/resume/run/report"]
    U --> A["askq<br/>one-question JSON bridge"]
    U --> S["deep-research-scorecard<br/>weighted Σ/100 ranking"]
    I --> R["~/.local/share/idr/runs/&lt;run_id&gt;/report.html"]
    A --> H["~/.askq/history.jsonl"]
    S --> M["Markdown or HTML scorecard fragment"]
```

| Skill | CLI | Purpose |
| --- | --- | --- |
| `interactive-deep-research` | guide only | Umbrella orchestration playbook for the full system. |
| `integrative-deep-research` | `idr` | Driver for plan, resume, full run, and report regeneration. |
| `askq` | `askq` | Human-in-the-loop question bridge with JSON stdout. |
| `deep-research-scorecard` | `scorecard` | Weighted candidate ranking that crowns a winner. |

Install the packaged skills and CLI symlinks:

```bash
./install.sh
```

By default this copies skills to `~/.claude/skills` and links drivers into
`~/.local/bin`. Override with `CLAUDE_SKILLS_DIR` or `BIN_DIR` if needed.

## Quickstart

Preferred phased flow for agent environments:

```bash
idr plan "Best open-source DE+EN voice cloning stack 2026"
```

The command prints JSON containing `run_id`, `rundir`, `notebook_id`, and the one
clarifying `question`. Relay that question to the human, then continue:

```bash
idr resume <run_id> --answer "Prioritize self-hostable open-source; exclude SaaS."
```

The final artifact is written to:

```text
~/.local/share/idr/runs/<run_id>/report.html
```

Automation or terminal-only loop:

```bash
idr run "Best open-source DE+EN voice cloning stack 2026"
```

Offline smoke test, with no `agy`, NotebookLM, login, or network:

```bash
IDR_MOCK=1 idr plan "Test topic"
IDR_MOCK=1 idr resume <run_id> --answer "Self-hosted only."
```

Score a researched comparison:

```bash
scorecard data/voice_scorecard.json
scorecard data/voice_scorecard.json --html > /tmp/voice_scorecard.html
```

Ask one structured question directly:

```bash
askq "Which deployment constraint matters most?" --choices "self-hosted|SaaS|hybrid"
askq "Constraint?" --answer "self-hosted" --no-log
```

## Worked Examples

The repository includes two rendered proof examples:

- Voice cloning stack for German and English:
  `reports/voice/`, scorecard spec `data/voice_scorecard.json`.
- Cross-channel messaging stack:
  `reports/messaging/`, scorecard spec `data/messaging_scorecard.json`.

The proof site generator lives in `site/`:

```bash
python3 site/build_goal_site.py
open site/goal_site.html
```

Live proof site, when connected to the tailnet: <http://100.120.120.120:5181/>

## Verification

Mock and CI-safe verification:

```bash
pytest -m "not live"
```

Opt-in live NotebookLM E2E verification, which spends quota and requires an
authenticated `nlm` CLI:

```bash
IDR_LIVE_E2E=1 IDR_REQUIRE_LIVE=1 pytest -m live tests/test_live_idr_e2e.py
```

Proof-site render check:

```bash
python3 site/build_goal_site.py
python3 -m http.server 5181 --directory site
```

Expected artifacts:

- `~/.local/share/idr/runs/<run_id>/report.html` for live or mock `idr` runs.
- `site/goal_site.html` for the local proof site.
- `reports/voice/report.html` and `reports/messaging/report.html` as worked examples.

See [TESTING.md](TESTING.md) for the full test matrix and live-run safety notes,
and [VERIFICATION.md](VERIFICATION.md) for the latest evidence ledger.

Useful environment variables:

| Variable | Purpose |
| --- | --- |
| `IDR_MOCK=1` | Run without `agy`, NotebookLM, network, or auth. |
| `IDR_RUNS_DIR=/tmp/idr-runs` | Write run artifacts outside the default user data directory. |
| `ASKQ_SCRIPT=/path/to/askq.py` | Override the `askq` script used by `idr run`. |
| `IDR_REQUIRE_LIVE=1` | Fail closed if a live NotebookLM step falls back or fails. |
| `IDR_LIVE_E2E=1` | Enable the opt-in pytest live E2E test. |

## Repository Layout

```text
interactive-deep-research/
├── README.md
├── install.sh
├── skills/
│   ├── interactive-deep-research/
│   ├── integrative-deep-research/
│   ├── askq/
│   └── deep-research-scorecard/
├── site/
│   ├── build_goal_site.py
│   ├── build_audios.py
│   ├── audio_demos.json
│   ├── site_config.json
│   ├── PROGRESS.md
│   └── audio/
├── reports/
│   ├── voice/
│   └── messaging/
├── data/
│   ├── voice_scorecard.json
│   └── messaging_scorecard.json
└── openaudio-calculator/
```

`site/` is canonical for proof-site build inputs. Root-level duplicates of the
site builder inputs were intentionally removed.

`openaudio-calculator/` is an example side artifact, not part of the core `idr`
pipeline.

## Notes And Gotchas

- `nlm query` returns JSON. Parse `.value.answer`, not raw stdout.
- NotebookLM deep research needs `--force` for headless runs, otherwise it can
  stop on an interactive confirmation prompt.
- `fast --auto-import` can return before sources are imported. Poll status and
  explicitly import before asking the clarifying question.
- `agy` can prepend status noise; strip leading progress lines before using its
  output.
- Keep fixed query prompts topic-anchored with `Topic: <topic>` to avoid drift.
- NotebookLM quotas and transient 429s are real; use `IDR_MOCK=1` for CI and
  smoke tests.

## Preflight

```bash
nlm doctor
agy --version
IDR_MOCK=1 idr plan "smoke test"
```

Run `nlm login` if NotebookLM auth has expired. `agy` is optional; if missing,
the pipeline falls back to the original topic/brief.

## License

MIT. See [LICENSE](LICENSE).
