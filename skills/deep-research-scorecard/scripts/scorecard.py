#!/usr/bin/env python3
"""scorecard — turn a deep-research comparison into a POINTS-scored, weighted
ranking that always crowns a winner and explains WHY. Reusable by any AI/CLI.

Input: a JSON spec (file arg or stdin):
{
  "title": "Best X",
  "scale": 10,                       # optional, default 10 (max per-criterion score)
  "criteria": [ {"key":"de","label":"Deutsch-Qualität","weight":3}, ... ],
  "candidates": [
     {"name":"CosyVoice 3.0","link":"https://github.com/...","note":"...",
      "scores": {"de":9,"en":9, ...}},   # 0..scale per criterion key
     ...
  ]
}

Output (stdout): a markdown scorecard — a per-criterion points table with a
weighted Σ/100 column, sorted best-first (winner name in **bold** so report
renderers highlight the row), followed by a "🏆 Sieger" block that justifies the
win from the data (top weighted contributions + where it beats the runner-up +
the candidate's note). Use --html for an embeddable HTML fragment instead.

Examples:
  scorecard voice.json
  scorecard voice.json --html > frag.html
  cat spec.json | scorecard -
"""
from __future__ import annotations
import argparse, json, sys, html

def compute(spec):
    scale = float(spec.get("scale", 10))
    crit = spec["criteria"]
    wsum = sum(c["weight"] for c in crit) or 1
    rows = []
    for cand in spec["candidates"]:
        sc = cand.get("scores", {})
        raw = sum(sc.get(c["key"], 0) * c["weight"] for c in crit)
        total = round(100.0 * raw / (wsum * scale), 1)
        rows.append({**cand, "total": total, "_raw": raw})
    rows.sort(key=lambda r: r["total"], reverse=True)
    for i, r in enumerate(rows, 1):
        r["rank"] = i
    return scale, crit, rows

def why(spec, crit, rows):
    if not rows: return ""
    win = rows[0]; runner = rows[1] if len(rows) > 1 else None
    scale = float(spec.get("scale", 10))
    # top weighted contributions
    contribs = sorted(crit, key=lambda c: win["scores"].get(c["key"], 0) * c["weight"], reverse=True)
    strong = [c["label"] for c in contribs[:3] if win["scores"].get(c["key"], 0) >= scale * 0.7]
    lines = [f'🏆 **Sieger: {win["name"]} — {win["total"]}/100**']
    if strong:
        lines.append(f'Gewählt wegen Spitzenwerten in: **{", ".join(strong)}**.')
    if runner:
        beats = [c["label"] for c in crit if win["scores"].get(c["key"],0) > runner["scores"].get(c["key"],0)]
        gap = round(win["total"] - runner["total"], 1)
        lines.append(f'Vorsprung **+{gap} Pkt** vor {runner["name"]} ({runner["total"]}/100); schlägt es u. a. bei: {", ".join(beats[:5])}.')
    if win.get("note"):
        lines.append(win["note"])
    return "\n\n".join(lines)

def render_md(spec, scale, crit, rows):
    head = ["Rang", "Tool"] + [c["label"] for c in crit] + ["Σ/100"]
    sep = ["---"] * len(head)
    out = [f'### Scorecard — {spec.get("title","Vergleich")} (gewichtet, {int(scale)}-Punkte-Skala)', ""]
    out.append("| " + " | ".join(head) + " |")
    out.append("| " + " | ".join(sep) + " |")
    for r in rows:
        name = r["name"]
        if r.get("link"): name = f'[{name}]({r["link"]})'
        if r["rank"] == 1: name = f'**{name}**'
        cells = [str(r["rank"]), name] + [str(r["scores"].get(c["key"], "–")) for c in crit] + [f'**{r["total"]}**']
        out.append("| " + " | ".join(cells) + " |")
    weights = ", ".join(f'{c["label"]}×{c["weight"]}' for c in crit)
    out.append("")
    out.append(f'_Gewichte: {weights}_')
    out.append("")
    out.append(why(spec, crit, rows))
    return "\n".join(out)

def _heat(v, scale):
    """css class by normalized score: green / amber / red."""
    try: n = float(v) / scale
    except (TypeError, ValueError): return ""
    return " sc-hi" if n >= 0.75 else (" sc-mid" if n >= 0.5 else " sc-lo")

def render_html(spec, scale, crit, rows):
    th = "".join(f"<th>{html.escape(c['label'])}<sup>×{c['weight']}</sup></th>" for c in crit)
    trs = []
    for r in rows:
        name = html.escape(r["name"])
        if r.get("link"): name = f'<a href="{html.escape(r["link"])}">{name}</a>'
        if r["rank"] == 1: name = f'🏆 <b>{name}</b>'
        cls = ' class="win"' if r["rank"] == 1 else ''
        tds = "".join(f'<td class="sc{_heat(r["scores"].get(c["key"]), scale)}">{r["scores"].get(c["key"],"–")}</td>' for c in crit)
        tot = f'<td class="tot{_heat(r["total"], 100)}"><b>{r["total"]}</b></td>'
        trs.append(f'<tr{cls}><td>{r["rank"]}</td><td>{name}</td>{tds}{tot}</tr>')
    w = html.escape(why(spec, crit, rows)).replace("🏆 **Sieger:", '<span class="crown">🏆 Sieger:').replace("**","").replace("\n\n","</span> ",1)
    if "</span>" not in w: w = w + ""
    return (f'<table class="scorecard"><thead><tr><th>#</th><th>Tool</th>{th}<th>Σ/100</th></tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table><div class="winner">{w}</div>')

def main(argv=None):
    p = argparse.ArgumentParser(prog="scorecard")
    p.add_argument("spec", help="JSON spec file, or - for stdin")
    p.add_argument("--html", action="store_true", help="emit HTML fragment instead of markdown")
    a = p.parse_args(argv)
    spec = json.load(sys.stdin if a.spec == "-" else open(a.spec, encoding="utf-8"))
    scale, crit, rows = compute(spec)
    print(render_html(spec, scale, crit, rows) if a.html else render_md(spec, scale, crit, rows))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
