#!/usr/bin/env python3
"""idr — Integrative Deep Research driver (deterministic, token-frugal).

A *rigid* pipeline so the orchestrating LLM barely has to think (and barely spends
tokens). The heavy reasoning is delegated to NotebookLM via the `nlm` CLI; the local
agent only fires fixed commands and relays exactly one clarifying question to the human.

Flow (matches the requested design):
  1. seed     — write a research brief and hand it to the local Antigravity agent.
  2. fast pass— `nlm research start --mode fast` (the quick "Google" pass) and ask
                NotebookLM for the single most important clarifying question.
  3. (human types the answer — via the askq bridge or relayed through the agent)
  4. deep pass— `nlm research start --mode deep --auto-import` on the SAME notebook
                (reuses sources = efficient), enriched with the human's answer and an
                explicit instruction to also scout existing flow frameworks
                (LangGraph, Langflow, CrewAI, …).
  5. iterate  — a FIXED set of `nlm query` angles (no improvisation).
  6. report   — generate a self-contained HTML website with the plan + Mermaid
                diagrams. The HTML is built locally with ZERO LLM tokens.

Phased commands (what the agent calls)
  idr.py plan   "<topic>" [--mock]      -> JSON {run_id, rundir, notebook_id, question}
  idr.py resume <run_id> --answer "..." -> JSON {run_id, report}   (runs deep+iterate+report)
  idr.py report <run_id>                -> regenerate HTML from collected content
  idr.py run    "<topic>" [--mock]      -> full interactive loop using askq (terminal/other AIs)

State lives in ~/.local/share/idr/runs/<run_id>/ (state.json, seed.md, content/*.md, report.html).
Set IDR_MOCK=1 (or pass --mock) to stub Antigravity + nlm so the whole loop runs
offline for testing — this is what the self-test subagent uses.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import os
import re
import shutil
import subprocess
import sys
import uuid

RUNS_DIR = os.path.expanduser("~/.local/share/idr/runs")
ASKQ = os.path.expanduser("~/.claude/skills/askq/scripts/askq.py")

# Fixed iteration angles — deterministic, no model improvisation. Topic-agnostic:
# cmd_resume prepends the run's topic so NotebookLM stays anchored to the right
# subject even if the notebook contains some off-topic sources.
QUERY_ANGLES = [
    ("overview", "Give a structured overview of THIS TOPIC with the key findings, strictly on-topic, in markdown. Use ## headings and bullet points. Ignore sources that are not about this topic."),
    ("comparison", "Build a detailed markdown comparison table of the main candidate options/tools/products for THIS TOPIC. Pick columns that fit the topic's key decision criteria, one row per candidate, cover as many candidates as the sources support, and **bold the recommended winner**. Stay strictly on-topic."),
    ("recommendation", "Give a concrete, opinionated recommendation for THIS TOPIC: name the single best pick and why, then a short numbered step-by-step setup/plan. Markdown."),
]


def _now_iso() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _eprint(*a: object) -> None:
    print(*a, file=sys.stderr, flush=True)


def _mock() -> bool:
    return os.environ.get("IDR_MOCK") == "1"


def _rundir(run_id: str) -> str:
    return os.path.join(RUNS_DIR, run_id)


def _load_state(run_id: str) -> dict:
    with open(os.path.join(_rundir(run_id), "state.json"), encoding="utf-8") as fh:
        return json.load(fh)


def _save_state(state: dict) -> None:
    d = _rundir(state["run_id"])
    os.makedirs(os.path.join(d, "content"), exist_ok=True)
    with open(os.path.join(d, "state.json"), "w", encoding="utf-8") as fh:
        json.dump(state, fh, ensure_ascii=False, indent=2)


def _run(cmd: list[str], timeout: int = 600) -> tuple[int, str, str]:
    """Run a subprocess, return (code, stdout, stderr). Never raises on non-zero."""
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except FileNotFoundError as exc:
        return 127, "", str(exc)
    except subprocess.TimeoutExpired:
        return 124, "", f"timeout after {timeout}s"


# ----------------------------------------------------------------------------
# Step 1 — Antigravity seed (local agent gets first crack)
# ----------------------------------------------------------------------------

def _seed_antigravity(rundir: str, topic: str) -> dict:
    seed_path = os.path.join(rundir, "seed.md")
    with open(seed_path, "w", encoding="utf-8") as fh:
        fh.write(
            f"# Research seed — {topic}\n\n"
            f"_Created {_now_iso()} by the integrative-deep-research pipeline._\n\n"
            "## Goal\n"
            f"Run integrative deep research on: **{topic}**.\n\n"
            "## What the Antigravity agent should do first (local pass)\n"
            "- Skim what you already know locally / in this workspace.\n"
            "- Note assumptions and the single biggest open question.\n"
            "- Do NOT answer fully — NotebookLM Deep Research will follow.\n\n"
            "## Then\n"
            "The pipeline hands off to NotebookLM (fast pass → clarifying question → deep pass → report).\n"
        )
    if _mock():
        return {"mock": True, "seed": seed_path, "brief": topic, "agy_used": False}
    # Real Antigravity waypoint: agy reasons locally to sharpen the topic into a
    # high-signal web-research brief BEFORE NotebookLM is called.
    brief = _agy(
        "You are the local scoping agent (waypoint 1) in a deterministic deep-research pipeline.\n"
        f"Topic: {topic}\n\n"
        "Produce a sharpened web-research brief for NotebookLM: max 4 lines. Name the concrete "
        "candidates/entities to compare and the key decision criteria. Output ONLY the brief.",
        timeout=240,
    )
    if brief:
        with open(os.path.join(rundir, "agy_brief.md"), "w", encoding="utf-8") as fh:
            fh.write(brief)
    return {"agy_used": bool(brief), "brief": brief or topic, "seed": seed_path}


def _agy(prompt: str, timeout: int = 300) -> str | None:
    """Run the Antigravity CLI agent non-interactively and return its printed response.
    Returns None in mock mode, if agy is absent, or on failure (callers fall back)."""
    if _mock():
        return None
    agy = shutil.which("agy") or shutil.which("antigravity")
    if not agy:
        return None
    code, out, err = _run([agy, "-p", prompt, "--dangerously-skip-permissions"], timeout=timeout)
    if code != 0 or not out.strip():
        return None
    # Drop agy's leading progress/status noise (e.g. "> 🚀 Starting Gemini CLI ...").
    lines = out.strip().splitlines()
    while lines and re.match(r"^\s*>?\s*([🚀✨⚙️]|Starting\b|Running\b)", lines[0]):
        lines.pop(0)
    return "\n".join(lines).strip() or out.strip()


# ----------------------------------------------------------------------------
# NotebookLM helpers (via nlm CLI) — with mock fallbacks
# ----------------------------------------------------------------------------

def _nlm_fast_research(topic: str, title: str) -> dict:
    if _mock():
        return {"notebook_id": "mock-nb-" + uuid.uuid4().hex[:6], "mock": True}
    code, out, err = _run(
        ["nlm", "research", "start", topic, "--mode", "fast", "--title", title, "--auto-import"],
        timeout=300,
    )
    nb = _extract_notebook_id(out + "\n" + err)
    imported = False
    if nb:
        # --auto-import can return before sources have actually landed, leaving the
        # notebook at 0 sources so the clarifying-question query has nothing to read.
        # Wait for the task to finish, then force an explicit import, then settle.
        _run(["nlm", "research", "status", nb, "--max-wait", "120"], timeout=140)
        ic, _io, _ie = _run(["nlm", "research", "import", nb], timeout=180)
        imported = ic == 0
    return {"notebook_id": nb, "code": code, "imported": imported, "raw": (out or err).strip()[:500]}


def _nlm_deep_research(query: str, notebook_id: str) -> dict:
    if _mock():
        return {"ok": True, "mock": True}
    # Save any pending sources from the prior (fast) task so --force doesn't drop them.
    _run(["nlm", "research", "import", notebook_id], timeout=300)
    # --force avoids the interactive "a research is already pending [y/N]" prompt
    # that otherwise blocks and aborts the deep pass. Retry once on a transient
    # "read operation timed out" when *starting* the research.
    attempts = []
    for _ in range(2):
        code, out, err = _run(
            ["nlm", "research", "start", query, "--mode", "deep", "--notebook-id", notebook_id,
             "--auto-import", "--force"],
            timeout=900,
        )
        attempts.append({"code": code, "raw": (out or err).strip()[:300]})
        if code == 0:
            break
    return {"ok": attempts[-1]["code"] == 0, "code": attempts[-1]["code"],
            "raw": attempts[-1]["raw"], "attempts": attempts}


def _nlm_query(notebook_id: str, prompt: str, mock_text: str) -> str:
    if _mock():
        return mock_text
    code, out, err = _run(["nlm", "query", "notebook", notebook_id, prompt], timeout=300)
    if code == 0 and out.strip():
        return _query_answer(out)
    return mock_text + f"\n\n> _(nlm query failed: {err.strip()[:160]})_"


def _query_answer(out: str) -> str:
    """nlm query returns JSON {"value":{"answer": "..."}} — extract the answer text,
    falling back to raw output if it isn't the expected shape."""
    try:
        data = json.loads(out)
        ans = data.get("value", {}).get("answer")
        return ans.strip() if isinstance(ans, str) and ans.strip() else out.strip()
    except (json.JSONDecodeError, AttributeError):
        return out.strip()


def _extract_notebook_id(text: str) -> str | None:
    # nlm prints something containing the notebook id; grab a plausible token.
    m = re.search(r"(?:notebook[_\s-]*id[:=]?\s*)([A-Za-z0-9_-]{8,})", text, re.I)
    if m:
        return m.group(1)
    m = re.search(r"\b([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})\b", text)
    return m.group(1) if m else None


MOCK_QUESTION = "Should the research prioritize self-hostable open-source frameworks, or also include hosted/SaaS options?"
MOCK_OVERVIEW = (
    "## Overview\n\n"
    "Integrative deep-research pipelines combine a **deterministic control flow** with "
    "**LLM-delegated reasoning**. The control layer stays rigid (fixed steps, fixed prompts) "
    "for token efficiency and reproducibility; the reasoning is pushed to a research engine "
    "(here: NotebookLM).\n\n"
    "- Determinism lives in the orchestrator, creativity lives in the engine.\n"
    "- Human-in-the-loop happens at fixed checkpoints (clarifying question, follow-ups).\n"
    "- Output is a static, shareable artifact (a website report).\n\n"
    "```mermaid\nflowchart LR\n  A[Topic] --> B[Antigravity seed]\n  B --> C[Fast pass]\n"
    "  C --> Q{Clarify?}\n  Q -->|human answer| D[Deep pass]\n  D --> E[Iterate queries]\n"
    "  E --> R[HTML report]\n```\n"
)
MOCK_FRAMEWORKS = (
    "## Existing frameworks\n\n"
    "| Tool | What it covers | Determinism | Report/Website output | Notes |\n"
    "|---|---|---|---|---|\n"
    "| LangGraph | Stateful agent graphs, HITL interrupts | High (explicit graph) | No (bring your own) | Best fit for rigid flows |\n"
    "| Langflow | Visual flow builder over LangChain | Medium | No | Good for prototyping |\n"
    "| CrewAI | Role-based multi-agent | Low–Medium | No | More autonomous |\n"
    "| n8n | General workflow automation | High | Partial (via nodes) | Not LLM-native |\n"
    "| Dify | LLM app platform | Medium | Partial | Hosted-first |\n"
)
MOCK_RECO = (
    "## Recommendation\n\n"
    "Keep the orchestrator a thin deterministic script (this pipeline) and delegate research "
    "to NotebookLM. If you outgrow a single script, port the same fixed graph to **LangGraph** "
    "to keep determinism and gain checkpointing.\n\n"
    "1. Lock the step sequence and prompts.\n"
    "2. Reuse one NotebookLM notebook across fast + deep passes.\n"
    "3. Generate the report locally (no tokens).\n"
)
MOCK_BY_ANGLE = {"overview": MOCK_OVERVIEW, "comparison": MOCK_FRAMEWORKS, "recommendation": MOCK_RECO}


# ----------------------------------------------------------------------------
# Commands
# ----------------------------------------------------------------------------

def cmd_plan(topic: str) -> dict:
    run_id = _dt.datetime.now().strftime("%Y%m%d-%H%M%S") + "-" + uuid.uuid4().hex[:4]
    rundir = _rundir(run_id)
    os.makedirs(os.path.join(rundir, "content"), exist_ok=True)

    seed = _seed_antigravity(rundir, topic)
    fast = _nlm_fast_research(seed.get("brief") or topic, title=f"IDR: {topic[:60]}")
    notebook_id = fast.get("notebook_id")

    question = MOCK_QUESTION if _mock() or not notebook_id else _nlm_query(
        notebook_id,
        f"Topic: {topic}\nAsk the SINGLE most important clarifying question to scope deep "
        "research. Output ONLY the question.",
        MOCK_QUESTION,
    ).strip()

    state = {
        "run_id": run_id,
        "topic": topic,
        "created": _now_iso(),
        "mock": _mock(),
        "seed": seed,
        "notebook_id": notebook_id,
        "question": question,
        "answer": None,
        "phase": "awaiting_answer",
    }
    _save_state(state)
    return {"run_id": run_id, "rundir": rundir, "notebook_id": notebook_id, "question": question}


def cmd_resume(run_id: str, answer: str) -> dict:
    state = _load_state(run_id)
    state["answer"] = answer
    notebook_id = state.get("notebook_id") or "mock-nb"

    # Antigravity waypoint 2: agy folds the human's clarification into a focused
    # deep-research query, then NotebookLM is called with it.
    fallback = (
        f"{state['topic']}\n\nScope clarification from the user: {answer}\n\n"
        "Name the concrete candidates/entities to compare, the key decision criteria, "
        "and prove the single best option."
    )
    agy_q = _agy(
        "You are the local query-crafting agent (waypoint 2) in a deterministic deep-research pipeline.\n"
        f"Topic: {state['topic']}\nUser scope clarification: {answer}\n\n"
        "Write ONE focused deep web-research query (max 6 lines) for NotebookLM that folds in the "
        "clarification, names concrete candidates to compare, the key criteria, and asks to prove "
        "the best option. Output ONLY the query.",
        timeout=240,
    )
    state["agy_deep_query"] = agy_q
    enriched = agy_q or fallback
    deep = _nlm_deep_research(enriched, notebook_id)
    state["deep"] = deep

    content = {}
    for key, prompt in QUERY_ANGLES:
        anchored = f"Topic: {state['topic']}\n\n{prompt}"
        text = _nlm_query(notebook_id, anchored, MOCK_BY_ANGLE[key])
        path = os.path.join(_rundir(run_id), "content", f"{key}.md")
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
        content[key] = path
    state["content"] = content
    state["phase"] = "report"
    _save_state(state)

    report = _build_report(run_id)
    state["report"] = report
    state["phase"] = "done"
    _save_state(state)
    return {"run_id": run_id, "report": report, "notebook_id": notebook_id}


def cmd_run_interactive(topic: str) -> dict:
    plan = cmd_plan(topic)
    # Use the askq bridge to pause for the human answer (terminal / other AIs).
    code, out, err = _run([sys.executable, ASKQ, plan["question"], "--context", f"Topic: {topic}"], timeout=86400)
    answer = topic  # fallback
    try:
        answer = json.loads(out).get("answer") or topic
    except json.JSONDecodeError:
        _eprint("idr: could not parse askq output; using topic as answer")
    return cmd_resume(plan["run_id"], answer)


# ----------------------------------------------------------------------------
# Tiny dependency-free markdown -> HTML (headings, lists, tables, bold, code,
# and ```mermaid fences). Enough for clean research reports.
# ----------------------------------------------------------------------------

def _inline(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"`([^`]+?)`", r"<code>\1</code>", text)
    text = re.sub(r"\[([^\]]+)\]\((https?://[^\)]+)\)", r'<a href="\2">\1</a>', text)
    return text


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]

        # mermaid fence
        if line.strip().startswith("```mermaid"):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1  # skip closing fence
            out.append('<div class="mermaid">\n' + html.escape("\n".join(buf)) + "\n</div>")
            continue
        # generic code fence
        if line.strip().startswith("```"):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith("```"):
                buf.append(lines[i])
                i += 1
            i += 1
            out.append("<pre><code>" + html.escape("\n".join(buf)) + "</code></pre>")
            continue
        # heading
        m = re.match(r"(#{1,4})\s+(.*)", line)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{_inline(m.group(2))}</h{lvl}>")
            i += 1
            continue
        # table (GFM): header row + separator row
        if "|" in line and i + 1 < n and re.match(r"^\s*\|?[\s:|-]+\|?\s*$", lines[i + 1]) and "-" in lines[i + 1]:
            def cells(row: str) -> list[str]:
                return [c.strip() for c in row.strip().strip("|").split("|")]
            header = cells(line)
            i += 2
            rows = []
            while i < n and "|" in lines[i] and lines[i].strip():
                rows.append(cells(lines[i]))
                i += 1
            thead = "".join(f"<th>{_inline(c)}</th>" for c in header)
            tbody = "".join("<tr>" + "".join(f"<td>{_inline(c)}</td>" for c in r) + "</tr>" for r in rows)
            out.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>")
            continue
        # unordered list
        if re.match(r"\s*[-*]\s+", line):
            items = []
            while i < n and re.match(r"\s*[-*]\s+", lines[i]):
                items.append("<li>" + _inline(re.sub(r"\s*[-*]\s+", "", lines[i], count=1)) + "</li>")
                i += 1
            out.append("<ul>" + "".join(items) + "</ul>")
            continue
        # ordered list
        if re.match(r"\s*\d+\.\s+", line):
            items = []
            while i < n and re.match(r"\s*\d+\.\s+", lines[i]):
                items.append("<li>" + _inline(re.sub(r"\s*\d+\.\s+", "", lines[i], count=1)) + "</li>")
                i += 1
            out.append("<ol>" + "".join(items) + "</ol>")
            continue
        # blockquote
        if line.strip().startswith(">"):
            out.append("<blockquote>" + _inline(line.strip()[1:].strip()) + "</blockquote>")
            i += 1
            continue
        # blank
        if not line.strip():
            i += 1
            continue
        # paragraph (gather consecutive non-empty, non-special lines)
        buf = [line]
        i += 1
        while i < n and lines[i].strip() and not re.match(r"(#{1,4}\s|\s*[-*]\s|\s*\d+\.\s|>|```)", lines[i]) and "|" not in lines[i]:
            buf.append(lines[i])
            i += 1
        out.append("<p>" + _inline(" ".join(buf)) + "</p>")
    return "\n".join(out)


HTML_TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>document.addEventListener("DOMContentLoaded",()=>{{if(window.mermaid)mermaid.initialize({{startOnLoad:true,theme:"neutral"}});}});</script>
<style>
:root{{--bg:#0f1220;--card:#171a2b;--ink:#e7e9f3;--muted:#9aa0bf;--accent:#7c8cff;--line:#272b45;}}
*{{box-sizing:border-box}}
body{{margin:0;background:linear-gradient(180deg,#0b0e1a,#0f1220);color:var(--ink);
font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;}}
.wrap{{max-width:920px;margin:0 auto;padding:48px 22px 96px}}
header.hero{{padding:34px 0 8px;border-bottom:1px solid var(--line);margin-bottom:28px}}
.kicker{{color:var(--accent);font-weight:600;letter-spacing:.12em;text-transform:uppercase;font-size:12px}}
h1{{font-size:34px;line-height:1.15;margin:.3em 0}}
.meta{{color:var(--muted);font-size:13px;display:flex;gap:18px;flex-wrap:wrap}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:22px 24px;margin:22px 0;
box-shadow:0 10px 30px rgba(0,0,0,.25)}}
h2{{font-size:23px;margin-top:0;border-left:3px solid var(--accent);padding-left:12px}}
h3{{font-size:18px;color:#cdd2f5}}
a{{color:var(--accent)}}
code{{background:#0d1020;border:1px solid var(--line);border-radius:6px;padding:1px 6px;font-size:.9em}}
pre{{background:#0d1020;border:1px solid var(--line);border-radius:12px;padding:16px;overflow:auto}}
pre code{{border:0;padding:0}}
table{{width:100%;border-collapse:collapse;margin:12px 0;font-size:14px}}
th,td{{border:1px solid var(--line);padding:9px 11px;text-align:left;vertical-align:top}}
th{{background:#1d2138;color:#dfe3ff}}
tr:nth-child(even) td{{background:#141729}}
blockquote{{border-left:3px solid var(--muted);margin:10px 0;padding:4px 14px;color:var(--muted)}}
.mermaid{{background:#fbfbff;border-radius:12px;padding:16px;margin:16px 0}}
.qa{{display:flex;gap:12px;align-items:flex-start}}
.qa .badge{{background:var(--accent);color:#0b0e1a;border-radius:999px;padding:2px 10px;font-size:12px;font-weight:700;white-space:nowrap}}
footer{{color:var(--muted);font-size:12px;margin-top:40px;text-align:center}}
ul,ol{{padding-left:22px}}
</style>
</head>
<body>
<div class="wrap">
<header class="hero">
  <div class="kicker">Integrative Deep Research</div>
  <h1>{topic}</h1>
  <div class="meta"><span>📅 {date}</span><span>🆔 {run_id}</span><span>📓 {notebook}</span><span>{mockflag}</span></div>
</header>

<div class="card">
  <h2>The plan</h2>
  <p>This report was produced by a <strong>deterministic, token-frugal</strong> pipeline:
  a rigid local orchestrator drives fixed steps and delegates all heavy reasoning to NotebookLM.</p>
  <div class="mermaid">
flowchart TD
  T["Topic"] --> S["1 · Antigravity seed (local)"]
  S --> F["2 · NotebookLM fast pass"]
  F --> Q{{"3 · Clarifying question"}}
  Q -->|human answer| D["4 · NotebookLM deep pass (+frameworks scout)"]
  D --> I["5 · Fixed iteration queries"]
  I --> R["6 · This HTML report"]
  </div>
  <div class="qa">
    <span class="badge">Q</span><div>{question}</div>
  </div>
  <div class="qa" style="margin-top:8px">
    <span class="badge">A</span><div>{answer}</div>
  </div>
</div>

{sections}

<footer>Generated locally with zero LLM tokens · askq + integrative-deep-research skill</footer>
</div>
</body>
</html>
"""


def _build_report(run_id: str) -> str:
    state = _load_state(run_id)
    rundir = _rundir(run_id)
    sections_html = []
    titles = {"overview": "Overview & findings", "comparison": "Comparison", "recommendation": "Recommendation & plan"}
    for key, _ in QUERY_ANGLES:
        path = state.get("content", {}).get(key)
        if not path or not os.path.exists(path):
            continue
        with open(path, encoding="utf-8") as fh:
            body = md_to_html(fh.read())
        sections_html.append(f'<div class="card"><h2>{html.escape(titles.get(key, key))}</h2>\n{body}\n</div>')

    page = HTML_TEMPLATE.format(
        title=html.escape(f"Deep Research — {state['topic'][:80]}"),
        topic=html.escape(state["topic"]),
        date=html.escape(state.get("created", _now_iso())[:10]),
        run_id=html.escape(run_id),
        notebook=html.escape(str(state.get("notebook_id") or "—")),
        mockflag="🧪 mock run" if state.get("mock") else "🌐 live",
        question=_inline(state.get("question") or "—"),
        answer=_inline(state.get("answer") or "—"),
        sections="\n".join(sections_html),
    )
    out_path = os.path.join(rundir, "report.html")
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(page)
    return out_path


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="idr", description="Integrative deep research (deterministic).")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("plan", help="Step 1-3: seed + fast pass + clarifying question.")
    sp.add_argument("topic")
    sp.add_argument("--mock", action="store_true")

    sr = sub.add_parser("resume", help="Step 4-6: deep pass + iterate + report.")
    sr.add_argument("run_id")
    sr.add_argument("--answer", required=True)

    rp = sub.add_parser("report", help="Regenerate the HTML report from collected content.")
    rp.add_argument("run_id")

    ri = sub.add_parser("run", help="Full interactive loop (uses askq).")
    ri.add_argument("topic")
    ri.add_argument("--mock", action="store_true")

    args = p.parse_args(argv)
    if getattr(args, "mock", False):
        os.environ["IDR_MOCK"] = "1"

    if args.cmd == "plan":
        print(json.dumps(cmd_plan(args.topic), ensure_ascii=False, indent=2))
    elif args.cmd == "resume":
        print(json.dumps(cmd_resume(args.run_id, args.answer), ensure_ascii=False, indent=2))
    elif args.cmd == "report":
        print(json.dumps({"report": _build_report(args.run_id)}, ensure_ascii=False, indent=2))
    elif args.cmd == "run":
        print(json.dumps(cmd_run_interactive(args.topic), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
