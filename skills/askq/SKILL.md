---
name: askq
description: Use when a script or agent needs to ask a human exactly one question and continue with a structured JSON answer. It is the human-in-the-loop bridge used by interactive/integrative deep research. Triggers: "ask the user and continue", "human-in-the-loop pause", "question bridge", "clarifying question step", "interactive prompt from a script".
version: 0.1.0
license: MIT
metadata:
  tags: [human-in-the-loop, cli, question, bridge, interactive, deterministic]
  related_skills: [interactive-deep-research, integrative-deep-research]
---

# askq

`askq` is a tiny dependency-free question bridge. It prints one question for a
human, reads one answer, and writes machine-parseable JSON to stdout. Prompts and
diagnostics go to stderr so stdout remains pipeable.

CLI: `askq` on PATH, or:

```bash
python3 ~/.claude/skills/askq/scripts/askq.py
```

## Usage

```bash
askq "Which region should I target?"
askq "Pick a depth" --choices "fast|deep"
askq "Constraints?" --context "Scoping deep research"
echo "EU + self-hosted" | askq "Constraints?"
askq "Constraints?" --answer "EU + self-hosted"
askq "Region?" --timeout 60
```

Example stdout:

```json
{"id":"3f9a1c2b","question":"Constraints?","choices":null,"answer":"EU + self-hosted","mode":"non-interactive","timed_out":false,"ts":"2026-06-01T23:30:00+02:00"}
```

Exit codes:

- `0`: answered
- `2`: timed out
- `3`: no input / EOF
- `64`: no question supplied

By default every Q&A is appended to `~/.askq/history.jsonl`. Disable this with
`--no-log`, or set a custom path with `--log`.

## Privacy / No PII

Do not enter secrets, credentials, personal data, private customer data, or other
sensitive content into `askq`. The default history file is intentionally simple
and local, but it is still persistent.

For sensitive or test questions:

```bash
askq "Constraint?" --answer "self-hosted" --no-log
askq "Constraint?" --answer "self-hosted" --log /tmp/askq-test.jsonl
rm -f ~/.askq/history.jsonl
```

## Flags And Environment

| Name | Effect |
| --- | --- |
| `--answer TEXT` | Non-interactive answer; returns immediately. |
| `ASKQ_ANSWER=TEXT` | Env equivalent of `--answer` when the flag is absent. |
| `--choices "a|b|c"` | Displays options; answer is returned verbatim. |
| `--timeout N` | Timeout for stdin in pipe/non-TTY mode; exits `2` if exceeded. |
| `--log PATH` | Append JSONL history to a custom file. |
| `--no-log` | Disable history logging for this question. |

## Agent Guidance

- In terminal workflows, call `askq "..."`, parse stdout JSON, and continue.
- In coding-agent sessions without interactive stdin, do not call bare `askq`;
  pass `--answer`, set `ASKQ_ANSWER`, or relay the question in chat and resume
  the downstream command.
- In tests and automation, always use `--answer` or `ASKQ_ANSWER`.

`askq` is the one-question primitive used by `idr run`; phased `idr plan/resume`
usually relays the question through chat instead.

## Failure Modes

| Symptom | Cause | Fix |
| --- | --- | --- |
| Exit `64` | No question text was supplied | Pass a positional question or `--question`. |
| Exit `3` | stdin reached EOF before an answer | Use `--answer`, `ASKQ_ANSWER`, or provide piped/TTY input. |
| Exit `2` | stdin timed out | Increase `--timeout` or switch to non-interactive mode. |
| Log warning on stderr | History path is not writable | Use `--no-log` or `--log <tmpfile>`. |
