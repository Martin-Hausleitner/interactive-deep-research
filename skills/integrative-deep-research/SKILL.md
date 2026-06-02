---
name: integrative-deep-research
description: Use when the user wants a deep, integrative research run that (1) hands a seed to the local Antigravity agent, (2) does a fast NotebookLM pass that returns ONE clarifying question the human answers, (3) escalates to a NotebookLM deep-research pass on the same notebook, (4) iterates with fixed queries, and (5) outputs a polished HTML website report with diagrams. Deterministic and token-frugal — the model fires fixed CLI steps; NotebookLM does the heavy reasoning. Triggers: "integrative deep research", "tiefe Recherche mit Notebook LM und Rückfrage", "deep research website report with diagrams", "Antigravity + NotebookLM research pipeline".
version: 0.1.0
license: MIT
metadata:
  tags: [deep-research, notebooklm, antigravity, deterministic, token-efficient, report, mermaid, human-in-the-loop]
  related_skills: [askq, notebooklm-mcp-cli, deep-research, comparison-deep-research]
---

# Integrative Deep Research

A **rigid, token-frugal** pipeline. The orchestrating model does almost no reasoning:
it fires fixed CLI commands and relays exactly one clarifying question. All heavy
reasoning is delegated to **NotebookLM** (via the `nlm` CLI). The final artifact is a
self-contained **HTML website report** with Mermaid diagrams, built locally with **zero
LLM tokens**.

Driver: `idr` (on PATH) or `python3 ~/.claude/skills/integrative-deep-research/scripts/idr.py`
Question bridge: the [[askq]] skill.

## The fixed flow

1. **Antigravity seed (local).** Write a research brief and open it in Antigravity (`agy`/`antigravity` CLI) so its local agent gets first crack.
2. **NotebookLM fast pass.** `nlm research start --mode fast` (~30s) creates a notebook and discovers sources; one `nlm query` asks NotebookLM for the single most important clarifying question.
3. **Clarifying question → human.** The human answers (deferred until here — no questions before this point).
4. **NotebookLM deep pass.** `nlm research start --mode deep --auto-import` on the **same notebook** (reuses sources = efficient), enriched with the human's answer and an instruction to also scout existing flow frameworks (LangGraph, Langflow, CrewAI, n8n, Dify).
5. **Iterate.** A FIXED set of `nlm query` angles (overview, frameworks comparison table, recommendation+plan). No improvisation.
6. **Report.** Generate `report.html` — a polished website with the plan, a Mermaid flow diagram, the Q&A, findings, a framework comparison table, and sources.

## How to run it (token-efficient, phased — preferred in Claude Code)

```bash
# Step 1–3: seed + fast pass + clarifying question. Prints JSON {run_id, question, ...}.
idr plan "<the user's topic>"
```
Relay the returned `question` to the human in chat. When they answer:
```bash
# Step 4–6: deep pass + iterate + build the HTML report. Prints {run_id, report}.
idr resume <run_id> --answer "<what the human said>"
```
Then open the report: `open "<report path>"`. Optionally regenerate: `idr report <run_id>`.

**Do this and little else.** Don't read source contents or re-summarize — NotebookLM
already did the reasoning and the HTML is generated locally. That is the whole point:
minimal tokens, deterministic behavior.

## Full interactive loop (terminal / other AIs)

```bash
idr run "<topic>"     # blocks on askq for the human answer, then finishes end-to-end
```

## Preflight & auth
- NotebookLM needs auth: if `nlm` errors, run `nlm login` (or `nlm doctor`).
- Antigravity is optional; if its CLI is absent the seed file is still written and the pipeline continues.

## Testing / offline
Set `IDR_MOCK=1` or pass `--mock` to stub Antigravity + NotebookLM with canned content.
The full loop (plan → question → resume → HTML) runs offline — used by the self-test.

```bash
IDR_MOCK=1 idr plan "test topic"
IDR_MOCK=1 idr resume <run_id> --answer "self-hosted only"
```

State lives in `~/.local/share/idr/runs/<run_id>/` (`state.json`, `seed.md`, `content/*.md`, `report.html`).
