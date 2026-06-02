---
name: askq
description: Use when a script or agent needs to pause and ask a human ONE question and get a typed answer back as structured JSON — a portable human-in-the-loop "Rückfrage" bridge any AI can call as a CLI. Triggers: "ask the user and continue", "human-in-the-loop pause", "question bridge", "clarifying question step", "interactive prompt from a script".
version: 0.1.0
license: MIT
metadata:
  tags: [human-in-the-loop, cli, question, bridge, interactive, deterministic]
  related_skills: [integrative-deep-research]
---

# askq — human-in-the-loop question bridge

A tiny, dependency-free CLI any AI (Claude, Hermes, Codex, Gemini, a shell script)
can shell out to. It prints ONE question for a human, blocks for their typed answer,
and returns clean JSON on **stdout** (question + diagnostics go to **stderr**, so
stdout stays pipeable).

CLI: `askq` (on PATH) or `python3 ~/.claude/skills/askq/scripts/askq.py`

## Usage

```bash
askq "Which region should I target?"                 # interactive: reads one stdin line
askq "Pick a depth" --choices "fast|deep"            # show options
askq "Constraints?" --context "Scoping deep research"# one-line context above the question
echo "EU + self-hosted" | askq "Constraints?"        # pipe the answer in
askq "Constraints?" --answer "EU + self-hosted"      # NON-interactive (automation / tests)
askq "Region?" --timeout 60                          # give up after 60s (pipes only) -> exit 2
```

Output (stdout):

```json
{"id":"3f9a1c2b","question":"Constraints?","choices":null,"answer":"EU + self-hosted","mode":"non-interactive","timed_out":false,"ts":"2026-06-01T23:30:00+02:00"}
```

Exit codes: `0` answered · `2` timed out · `3` no input (EOF) · `64` no question given.
Every Q&A is appended to `~/.askq/history.jsonl` (disable with `--no-log`).

## How an agent should use it

- **Inside a terminal / another CLI agent:** call `askq "..."`; the human types the answer; parse stdout JSON; continue.
- **Inside Claude Code (no interactive stdin):** prefer the phased pattern — print the question, relay it to the human in chat, then re-invoke the downstream step with `--answer "<what the human said>"`. Do not run bare interactive `askq` from the Bash tool; it will block.
- **In automation / tests:** always pass `--answer` (or set `ASKQ_ANSWER`) so nothing blocks.

## Notes
- stdout is JSON only — safe to pipe into `jq -r .answer`.
- This is the deterministic "Rückfrage" primitive used by the `integrative-deep-research` skill.
