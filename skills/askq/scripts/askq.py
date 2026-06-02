#!/usr/bin/env python3
"""askq — a tiny human-in-the-loop question bridge that ANY AI can call as a CLI.

It prints ONE question for a human, blocks for their typed answer, and returns the
result as clean JSON on stdout. The question text and all diagnostics go to stderr,
so stdout stays machine-parseable for piping into another tool or agent.

Why this exists: deterministic pipelines (see the integrative-deep-research skill)
need to pause for a human "Rückfrage" without the orchestrating model having to
improvise. Any agent — Claude, Hermes, Codex, Gemini, a plain shell script — can
shell out to `askq "question"` and get a structured answer back.

Modes
  interactive (default)  read one line from stdin (a TTY or a pipe).
  non-interactive        --answer TEXT  (or env ASKQ_ANSWER) returns immediately.
                         Use this in automation and tests so nothing blocks.
  --choices "a|b|c"      present options; the answer is returned verbatim.
  --timeout N            seconds to wait for stdin in interactive mode; on
                         timeout, exit 2 with answer=null and timed_out=true.

Every Q&A is appended to ~/.askq/history.jsonl (disable with --no-log).

Examples
  askq "Which region should I target?"
  askq "Pick a depth" --choices "fast|deep"
  echo "EU + self-hosted" | askq "Constraints?"
  askq "Constraints?" --answer "EU + self-hosted"        # non-interactive / tests
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import select
import sys
import uuid

LOG_DEFAULT = os.path.expanduser("~/.askq/history.jsonl")


def _now_iso() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _eprint(*args: object) -> None:
    print(*args, file=sys.stderr, flush=True)


def _read_stdin_line(timeout: int) -> tuple[str | None, bool]:
    """Return (line, timed_out). line is None on EOF/timeout."""
    if timeout and timeout > 0 and not sys.stdin.isatty():
        # Only meaningful for pipes/non-tty; TTYs block on input() anyway.
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if not ready:
            return None, True
    try:
        line = sys.stdin.readline()
    except (EOFError, KeyboardInterrupt):
        return None, False
    if line == "":  # EOF
        return None, False
    return line.rstrip("\n"), False


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        prog="askq",
        description="Ask a human one question and return the answer as JSON.",
    )
    p.add_argument("question", nargs="?", help="The question to ask. If omitted, read from --question or stdin first line.")
    p.add_argument("--question", dest="question_opt", help="Question text (alternative to positional).")
    p.add_argument("--choices", help="Pipe- or comma-separated answer options to display.")
    p.add_argument("--answer", help="Provide the answer directly (non-interactive / tests).")
    p.add_argument("--timeout", type=int, default=0, help="Seconds to wait for stdin (0 = no timeout).")
    p.add_argument("--id", help="Stable id for this question (default: random).")
    p.add_argument("--context", help="Optional one-line context shown above the question.")
    p.add_argument("--log", default=LOG_DEFAULT, help="History log path (jsonl).")
    p.add_argument("--no-log", action="store_true", help="Do not append to the history log.")
    args = p.parse_args(argv)

    question = args.question or args.question_opt
    choices = None
    if args.choices:
        sep = "|" if "|" in args.choices else ","
        choices = [c.strip() for c in args.choices.split(sep) if c.strip()]

    # Resolve the answer source.
    answer = args.answer if args.answer is not None else os.environ.get("ASKQ_ANSWER")
    mode = "non-interactive" if answer is not None else "interactive"
    timed_out = False

    if question is None and mode == "interactive":
        # Allow `echo "Q\nA" | askq` style where first line is the question.
        first, _ = _read_stdin_line(args.timeout)
        question = first
    if not question:
        _eprint("askq: no question provided")
        return 64  # EX_USAGE

    if mode == "interactive":
        if args.context:
            _eprint(f"› {args.context}")
        _eprint(f"❓ {question}")
        if choices:
            _eprint("   options: " + " | ".join(choices))
        _eprint("   (type your answer, then Enter)")
        line, timed_out = _read_stdin_line(args.timeout)
        answer = line

    result = {
        "id": args.id or uuid.uuid4().hex[:8],
        "question": question,
        "choices": choices,
        "answer": answer,
        "mode": mode,
        "timed_out": timed_out,
        "ts": _now_iso(),
    }

    if not args.no_log:
        try:
            os.makedirs(os.path.dirname(args.log), exist_ok=True)
            with open(args.log, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(result, ensure_ascii=False) + "\n")
        except OSError as exc:  # logging must never break the bridge
            _eprint(f"askq: warning: could not write log: {exc}")

    print(json.dumps(result, ensure_ascii=False))
    if timed_out:
        return 2
    if answer is None:
        return 3  # no input received (EOF)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
