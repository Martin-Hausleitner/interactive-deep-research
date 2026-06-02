---
name: interactive-deep-research
description: Umbrella guide for the interactive deep-research system. Use when someone asks how the full system works, how to install it, how to run an end-to-end research with one human question, or how the idr, askq, and scorecard skills fit together.
version: 0.1.0
license: MIT
metadata:
  tags: [deep-research, notebooklm, antigravity, human-in-the-loop, overview, guide, deterministic, token-efficient]
  related_skills: [integrative-deep-research, askq, deep-research-scorecard]
---

# Interactive Deep Research

This is the umbrella playbook. Use it to understand and coordinate the engine
skills; use `integrative-deep-research` when you actually run the pipeline.

Design principle: deterministic orchestration, NotebookLM-backed reasoning, one
human clarification, local HTML rendering.

## Components

| Component | CLI | Role |
| --- | --- | --- |
| `integrative-deep-research` | `idr` | Runs the full pipeline and renders `report.html`. |
| `askq` | `askq` | One-question human bridge, JSON stdout, audit log. |
| `deep-research-scorecard` | `scorecard` | Converts researched candidates into a weighted ranking. |

```mermaid
flowchart LR
    U["interactive-deep-research<br/>read first"] --> I["idr<br/>plan/resume/run/report"]
    U --> Q["askq<br/>JSON question bridge"]
    U --> S["scorecard<br/>weighted ranking"]
    I --> R["run dir + report.html"]
    Q --> L["optional local JSONL log"]
    S --> O["Markdown/HTML fragment"]
```

## Canonical Flow

```mermaid
flowchart TD
    A["idr plan TOPIC"] --> B["agy seed<br/>short scoping brief"]
    B --> C["NotebookLM FAST pass<br/>source discovery"]
    C --> D["status + import<br/>wait until sources land"]
    D --> E["ONE clarifying question"]
    E --> F["human answer"]
    F --> G["idr resume RUN --answer ..."]
    G --> H["NotebookLM DEEP pass<br/>same notebook, --force"]
    H --> I["fixed queries<br/>overview / comparison / recommendation"]
    I --> J["report.html<br/>local, self-contained, Mermaid"]
```

## How To Invoke

Agent-safe phased mode:

```bash
idr plan "<topic>"
idr resume <run_id> --answer "<answer>"
```

Terminal interactive mode:

```bash
idr run "<topic>"
```

Offline smoke:

```bash
IDR_MOCK=1 idr plan "test topic"
IDR_MOCK=1 idr resume <run_id> --answer "self-hosted only"
```

Live proof mode:

```bash
IDR_REQUIRE_LIVE=1 idr plan "<small synthetic topic>"
IDR_REQUIRE_LIVE=1 idr resume <run_id> --answer "<synthetic answer>"
```

Use `IDR_RUNS_DIR=/tmp/idr-runs` when a test or verifier must avoid writing to
the user's default run directory.

Verification commands:

```bash
pytest -m "not live"
IDR_LIVE_E2E=1 IDR_REQUIRE_LIVE=1 pytest -m live tests/test_live_idr_e2e.py
```

The live command is opt-in because it uses NotebookLM auth, network, and quota.

Scorecard:

```bash
scorecard data/voice_scorecard.json
scorecard data/voice_scorecard.json --html
```

Direct question bridge:

```bash
askq "Which constraint matters most?" --choices "cost|quality|license"
askq "Constraint?" --answer "license" --no-log
```

## Proof Site

`site/` contains the canonical proof-site build inputs and generated local HTML.
It combines two worked examples:

- DE/EN voice cloning stack: `reports/voice/`, `data/voice_scorecard.json`.
- Cross-channel messaging stack: `reports/messaging/`, `data/messaging_scorecard.json`.

Rebuild locally:

```bash
python3 site/build_goal_site.py
open site/goal_site.html
```

## Operational Notes

- `nlm query` returns JSON; consume `.value.answer`.
- Use `--force` for NotebookLM deep research in headless mode.
- Poll/import after fast research before asking the clarifying question.
- Strip `agy` progress noise before treating its stdout as a brief.
- Keep query prompts topic-anchored.
- Use `IDR_MOCK=1` for contributor smoke tests and CI.
- Avoid secrets or personal data in topics, answers, askq logs, NotebookLM
  notebooks, and rendered reports.

## Privacy / No PII

Treat every topic, answer, scorecard, report, and proof-site artifact as
potentially publishable. Use synthetic inputs for tests and examples; keep
private customer data, credentials, account names, internal URLs, and local file
paths out of committed runs and rendered HTML.

## Failure Modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Live run silently degrades | NotebookLM failure fell back to mock text | Use `IDR_REQUIRE_LIVE=1` for proof runs. |
| Agent session blocks | `idr run` invoked interactive `askq` | Use phased `idr plan` then `idr resume`. |
| Proof-site links local paths | Run artifacts were rendered from machine-local paths | Rebuild from repo-relative `reports/` and `site/` inputs. |
| No decisive recommendation | Research stayed qualitative | Add `deep-research-scorecard` with explicit weights. |
