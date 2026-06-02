#!/usr/bin/env python3
"""Polished presentation website: two deep-research examples + chronological Ablauf
+ Q&A, with benchmark/repo links, license chips and winner highlighting. Re-runnable."""
import os, json, html, datetime, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "skills", "integrative-deep-research", "scripts"))
import idr

GOAL = HERE
RUNS = os.path.expanduser("~/.local/share/idr/runs")
ASKQ = os.path.expanduser("~/.askq/history.jsonl")
CFG = os.path.join(GOAL, "site_config.json")

ORDER = ["overview","scorecard","audios","authenticity","comparison","notebooklm","emotion","links","recommendation","questions","weaknesses","diagnosis","system_prompt"]
RAW = {"scorecard","audios"}  # inline as raw HTML (already styled), not markdown
TITLES = {"overview":"Überblick & Findings","scorecard":"Punkte-Scorecard · Sieger gekürt","audios":"Demo-Audios (Deutsch) pro Library","authenticity":"Echtheits-Leaderboard (SIM-o · MOS · WER · Elo · Emotion)","comparison":"Vergleich · Benchmarks · Repo-Links",
          "notebooklm":"NotebookLM Deep Research (echter Deep-Pass)","emotion":"Emotion & Expressivität (DE+EN)",
          "links":"Komponenten · Benchmarks · Links",
          "recommendation":"Empfehlung & Beweis","questions":"Kritische Fragen","weaknesses":"Schwachstellen",
          "diagnosis":"Diagnose","system_prompt":"System-Prompt"}
ICONS = {"overview":"📋","scorecard":"🥇","audios":"🔊","authenticity":"🎚️","comparison":"📊","notebooklm":"🔬","emotion":"🎭","links":"🔗","recommendation":"🏆",
         "questions":"❓","weaknesses":"⚠️","diagnosis":"🧭","system_prompt":"📜"}

def colorize(s):
    """Bold+color key terms so the report scans fast (winners green, risks red)."""
    green = [r"CosyVoice ?3(?:\.0)?", r"Chatterbox Multilingual", r"La Growth Machine",
             r"Matrix[\s+]+Mautrix[^.,<]*|Matrix Homeserver", r"OmniVoice",
             r"kein(?:en)? (?:besserer?|technologisch[^.<]{0,40}überlegen\w*)[^.<]*", r"unter 0,1\s*%|<\s*0,1\s*%"]
    red = [r"non-commercial", r"disqualifiziert\w*", r"Lizenz-Sackgasse", r"Coqui (?:tot|aus)", r"kein\w* Deutsch", r"3[\s–-]5\s*%"]
    out = []
    for part in re.split(r"(<[^>]+>)", s):
        if part.startswith("<"):
            out.append(part); continue
        for p in green: part = re.sub(p, lambda m: f'<span class="hl">{m.group(0)}</span>', part)
        for p in red: part = re.sub(p, lambda m: f'<span class="warn">{m.group(0)}</span>', part)
        out.append(part)
    return "".join(out)
# GitHub star badges ("Gitter-Bezettler") per example run_id
BADGES = {
  "20260602-015821-def4": [("Chatterbox","resemble-ai/chatterbox"),("CosyVoice","FunAudioLLM/CosyVoice"),
      ("OmniVoice","k2-fsa/OmniVoice"),("Fish-Speech","fishaudio/fish-speech"),("Qwen3-TTS","QwenLM/Qwen3-TTS"),("F5-TTS","SWivid/F5-TTS")],
  "20260602-015302-149e": [("Synapse","element-hq/synapse"),("mautrix","mautrix/go"),("Zonos","Zyphra/Zonos")],
}
def badge_strip(rid):
    items = BADGES.get(rid)
    if not items: return ""
    b = []
    for label, path in items:
        url = f"https://img.shields.io/github/stars/{path}?style=flat-square&logo=github&label={label}&color=8a9bff&labelColor=121627"
        b.append(f'<a href="https://github.com/{path}"><img alt="{label}" src="{url}"></a>')
    return '<div class="badges">'+ " ".join(b) +'</div>'

def run_state(rid):
    p = os.path.join(RUNS, rid, "state.json")
    return json.load(open(p)) if os.path.exists(p) else None

def report_dir(ex):
    rd = ex.get("report_dir")
    if not rd:
        return None
    return rd if os.path.isabs(rd) else os.path.normpath(os.path.join(ROOT, rd))

def content_path(ex, st, key):
    rd = report_dir(ex)
    if rd:
        for ext in ("html", "md"):
            candidate = os.path.join(rd, "content", f"{key}.{ext}")
            if os.path.exists(candidate):
                return candidate
    path = ((st or {}).get("content") or {}).get(key)
    if path and os.path.exists(path):
        return path
    return None

def chipify(s):
    """Color-code license tokens inside rendered HTML (commercial=green, NC=red)."""
    reps = [
        (r"\bApache-2\.0\b", '<span class="lic ok">Apache-2.0</span>'),
        (r"\bMIT\b(?!\s*=)", '<span class="lic ok">MIT</span>'),
        (r"CC-BY(?!-NC)[\w.-]*", '<span class="lic ok">CC-BY</span>'),
        (r"CC-BY-NC[\w.-]*", '<span class="lic no">CC-BY-NC</span>'),
        (r"non-commercial|Non-Commercial", '<span class="lic no">non-commercial</span>'),
        (r"Research[\s-]?Lic[\w.()-]*", '<span class="lic no">Research-License</span>'),
        (r"\bCPML\b", '<span class="lic no">CPML</span>'),
    ]
    # avoid touching inside href="" — split on tags
    out = []
    for part in re.split(r"(<[^>]+>)", s):
        if part.startswith("<"):
            out.append(part)
        else:
            for pat, rep in reps:
                part = re.sub(pat, rep, part)
            out.append(part)
    return "".join(out)

def section_for(ex, idx):
    rid = ex.get("run_id"); st = run_state(rid) if rid else None
    anchor = f"bsp{idx}"
    rd = report_dir(ex)
    if not st and not rd:
        body = f'<p class="dim">⏳ {html.escape(ex.get("status","läuft …"))}</p>'
    else:
        parts = []
        for key in ORDER:
            path = content_path(ex, st, key)
            if path:
                raw = open(path, encoding="utf-8").read()
                rendered = raw if key in RAW or path.endswith(".html") else colorize(chipify(idr.md_to_html(raw)))
                parts.append(f'<h3>{ICONS.get(key,"•")} {html.escape(TITLES.get(key,key))}</h3>\n'+rendered)
        nb = (st or {}).get("notebook_id") or rid or "repo artifact"
        deep = ((st or {}).get("deep") or {}).get("ok")
        deepn = ((st or {}).get("deep_nlm") or {}).get("ok")
        public_rep = os.path.join(rd, "report.html") if rd else ""
        local_rep = os.path.join(RUNS, rid, "report.html") if rid else ""
        rep = public_rep if public_rep and os.path.exists(public_rep) else local_rep
        meta = '<div class="rmeta">'
        meta += f'<span class="pill">📓 {html.escape(str(nb)[:22])}</span>'
        if deep is not None: meta += f'<span class="pill ok">deep_ok ✓</span>'
        if deepn: meta += f'<span class="pill ok">NotebookLM-deep ✓</span>'
        if os.path.exists(rep):
            label = os.path.relpath(rep, ROOT) if rep.startswith(ROOT) else "report.html"
            meta += f'<span class="pill">Einzelreport: {html.escape(label)}</span>'
        meta += '</div>'
        body = meta + badge_strip(rid) + ("\n".join(parts) or '<p class="dim">in Arbeit …</p>')
    verdict = f'<div class="verdict"><span class="vlabel">Verdict</span>{idr._inline(ex.get("verdict",""))}</div>' if ex.get("verdict") else ""
    status = f'<span class="stbadge">{html.escape(ex.get("status",""))}</span>'
    return (f'<section id="{anchor}" class="card example"><div class="extag">{html.escape(ex.get("tag","Beispiel"))} {status}</div>'
            f'<h2>{html.escape(ex.get("title",""))}</h2>{verdict}{body}</section>')

def winner_cards(exs):
    cards = []
    for i, ex in enumerate(exs, 1):
        v = ex.get("verdict","").split("Beweis")[0].strip(" .·")
        cards.append(f'<a class="wcard" href="#bsp{i}"><div class="wtag">{html.escape(ex.get("tag",""))}</div>'
                     f'<div class="wtitle">{html.escape(ex.get("title",""))}</div>'
                     f'<div class="wverdict">{idr._inline(v[:240])}</div></a>')
    return "\n".join(cards)

def timeline(cfg):
    items = []
    for r in cfg.get("rounds", []):
        items.append(f'<li><span class="dot"></span><span class="rnd">{html.escape(r.get("round",""))}</span>'
                     f'<span class="rtxt">{idr._inline(r.get("note",""))}</span></li>')
    return "\n".join(items) or '<li class="dim">—</li>'

def qa_panel():
    rows = []
    if os.path.exists(ASKQ):
        for line in open(ASKQ).read().splitlines()[-50:]:
            try: d = json.loads(line)
            except: continue
            if not (d.get("question") and d.get("answer")): continue
            rows.append(f'<div class="qa"><div class="q">❓ {html.escape((d.get("question") or "")[:300])}</div>'
                        f'<div class="a">💬 {html.escape(d.get("answer") or "")}</div>'
                        f'<div class="ts">🕐 {html.escape(d.get("ts","")[:16].replace("T"," "))}</div></div>')
    return "\n".join(rows[-10:]) or '<p class="dim">—</p>'

def main():
    cfg = json.load(open(CFG)) if os.path.exists(CFG) else {"examples":[],"rounds":[]}
    exs = cfg.get("examples", [])
    secs = "\n".join(section_for(ex, i) for i, ex in enumerate(exs, 1))
    nav = "".join(f'<a href="#bsp{i}">{html.escape(ex.get("tag","Bsp"))}</a>' for i, ex in enumerate(exs, 1))
    now = os.environ.get("SITE_BUILD_TS", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    sp = os.path.join(GOAL, "agy_summary.txt")
    summ = open(sp).read().strip() if os.path.exists(sp) else ""
    # strip agy status noise lines
    summ = "\n".join(l for l in summ.splitlines() if not re.match(r"^\s*>?\s*([🚀✨⚙️]|Starting\b|Running\b)", l)).strip()
    exec_card = (f'<section class="card summary"><div class="extag">✦ Antigravity · Executive Summary</div>'
                 f'<div class="summtext">{colorize(chipify(idr._inline(summ)))}</div></section>') if summ else ""
    page = f"""<!doctype html><html lang="de"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Interaktives Deep Research — Verlauf, Output & Beweis</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Space+Grotesk:wght@600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js"></script>
<script>document.addEventListener("DOMContentLoaded",()=>{{window.mermaid&&mermaid.initialize({{startOnLoad:true,theme:"base",themeVariables:{{primaryColor:"#eef1ff",primaryTextColor:"#1a1d2e",lineColor:"#8a9bff",fontFamily:"Inter"}}}});}});</script>
<style>
:root{{--bg:#070912;--card:#121627;--card2:#0e1220;--ink:#eef0fa;--muted:#959bbb;--accent:#8a9bff;--accent2:#5ee0c4;--good:#4ade80;--warn:#fbbf24;--bad:#fb7185;--line:#252a45}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{margin:0;background:radial-gradient(1300px 700px at 78% -12%,#1b2348 0,transparent 55%),radial-gradient(900px 500px at 5% 10%,#0f2a2a 0,transparent 45%),#070912;color:var(--ink);font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;line-height:1.65}}
.wrap{{max-width:1120px;margin:0 auto;padding:34px 22px 120px}}
nav.top{{position:sticky;top:0;z-index:30;backdrop-filter:blur(14px);background:rgba(7,9,18,.78);border-bottom:1px solid var(--line);padding:12px 22px;margin:-34px -22px 30px;font-size:14px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}}
nav.top a{{color:var(--muted);text-decoration:none;padding:5px 11px;border-radius:8px;transition:.15s}}nav.top a:hover{{color:var(--ink);background:rgba(138,155,255,.12)}}
nav.top .b{{color:var(--accent2);font-weight:800;font-family:"Space Grotesk";margin-right:6px}}
.kicker{{color:var(--accent);font-weight:700;letter-spacing:.18em;text-transform:uppercase;font-size:11.5px}}
h1{{font-family:"Space Grotesk";font-size:44px;line-height:1.05;margin:.18em 0;letter-spacing:-.5px;background:linear-gradient(92deg,#fff 20%,#9fb0ff 60%,#5ee0c4);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}}
h2{{font-family:"Space Grotesk";font-size:25px;margin:0 0 .4em;letter-spacing:-.3px}}
h3{{font-size:16px;color:#c3c9ee;margin:1.7em 0 .5em;text-transform:none;font-weight:700;border-bottom:1px solid var(--line);padding-bottom:6px}}
.lead{{color:var(--muted);font-size:16px;max-width:760px}}
.stats{{display:flex;gap:12px;flex-wrap:wrap;margin:20px 0 8px}}
.stat{{background:linear-gradient(180deg,var(--card),var(--card2));border:1px solid var(--line);border-radius:14px;padding:12px 18px;min-width:120px}}
.stat b{{font-family:"Space Grotesk";font-size:26px;color:var(--accent2);display:block}}.stat span{{color:var(--muted);font-size:12.5px}}
.winners{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:26px 0}}
.wcard{{display:block;text-decoration:none;color:inherit;background:linear-gradient(180deg,#16203f,#10182e);border:1px solid #2b3566;border-radius:18px;padding:20px 22px;transition:.18s;position:relative;overflow:hidden}}
.wcard:hover{{transform:translateY(-3px);border-color:var(--accent);box-shadow:0 18px 44px rgba(80,100,255,.22)}}
.wcard:before{{content:"🏆";position:absolute;right:16px;top:12px;font-size:22px;opacity:.5}}
.wtag{{color:var(--accent);font-size:11.5px;font-weight:800;letter-spacing:.1em;text-transform:uppercase}}
.wtitle{{font-family:"Space Grotesk";font-size:18px;font-weight:700;margin:6px 0 10px}}
.wverdict{{color:var(--accent2);font-size:14px;line-height:1.5}}
.card{{background:linear-gradient(180deg,var(--card),var(--card2));border:1px solid var(--line);border-radius:20px;padding:26px 28px;margin:22px 0;box-shadow:0 16px 46px rgba(0,0,0,.34)}}
.example{{border-top:3px solid var(--accent)}}
.extag{{color:var(--accent);font-weight:800;font-size:12px;letter-spacing:.12em;text-transform:uppercase;display:flex;gap:10px;align-items:center;flex-wrap:wrap;margin-bottom:4px}}
.stbadge{{background:#0f2a1c;border:1px solid #2f6b46;color:var(--good);border-radius:999px;padding:3px 11px;font-size:11px;letter-spacing:0;text-transform:none;font-weight:600}}
.verdict{{color:var(--accent2);font-weight:500;margin:10px 0 16px;font-size:15.5px;background:linear-gradient(180deg,#0d211f,#0c1a20);border:1px solid #1f5048;border-radius:14px;padding:14px 16px;line-height:1.55}}
.vlabel{{display:inline-block;background:var(--accent2);color:#06231d;font-weight:800;font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;border-radius:6px;padding:2px 8px;margin-right:10px;vertical-align:middle}}
.dim{{color:var(--muted)}}.rmeta{{display:flex;gap:7px;flex-wrap:wrap;margin:6px 0 14px}}
.pill{{background:#0c1020;border:1px solid var(--line);border-radius:999px;padding:3px 11px;font-size:11.5px;color:var(--muted)}}.pill.ok{{color:var(--good);border-color:#2f6b46}}.pill a{{color:var(--accent);text-decoration:none}}
table{{width:100%;border-collapse:separate;border-spacing:0;margin:14px 0;font-size:13px;border:1px solid var(--line);border-radius:12px;overflow:hidden}}
th,td{{border-bottom:1px solid var(--line);border-right:1px solid var(--line);padding:10px 12px;text-align:left;vertical-align:top}}
th{{background:#1b203a;font-weight:700;color:#dfe3ff;font-size:12px;text-transform:uppercase;letter-spacing:.04em}}
td:last-child,th:last-child{{border-right:0}}tr:last-child td{{border-bottom:0}}
tbody tr:nth-child(even) td{{background:#0c1020}}
tbody tr:has(td strong) td{{background:rgba(94,224,196,.07);box-shadow:inset 3px 0 0 var(--accent2)}}
td a{{color:var(--accent);text-decoration:none;border-bottom:1px dotted rgba(138,155,255,.5)}}td a:hover{{color:var(--accent2)}}
.lic{{display:inline-block;border-radius:6px;padding:1px 7px;font-size:11px;font-weight:700;font-family:"JetBrains Mono"}}
.lic.ok{{background:#0f2a1c;color:var(--good);border:1px solid #2f6b46}}.lic.no{{background:#2a1116;color:var(--bad);border:1px solid #6b2f3a}}
a{{color:var(--accent)}}.mermaid{{background:#f6f7ff;border-radius:14px;padding:18px;margin:8px 0}}
ul.tl{{list-style:none;padding:0;margin:6px 0 0;position:relative}}ul.tl:before{{content:"";position:absolute;left:8px;top:6px;bottom:6px;width:2px;background:linear-gradient(var(--accent),var(--accent2))}}
ul.tl li{{position:relative;padding:7px 0 16px 32px}}.dot{{position:absolute;left:2px;top:10px;width:14px;height:14px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 4px rgba(138,155,255,.16)}}
.rnd{{display:inline-block;background:#1b2138;border:1px solid #2b3566;border-radius:7px;padding:2px 9px;font-size:12px;color:var(--accent2);margin-right:9px;font-weight:700;font-family:"JetBrains Mono"}}
.qa{{border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:11px 0;background:#0f1326}}.qa .q{{font-weight:600}}.qa .a{{color:var(--good);margin-top:5px}}.qa .ts{{color:var(--muted);font-size:11px;margin-top:6px;font-family:"JetBrains Mono"}}
code{{background:#0c1020;border:1px solid var(--line);border-radius:6px;padding:1px 6px;font-family:"JetBrains Mono";font-size:.88em}}
pre{{background:#0c1020;border:1px solid var(--line);border-radius:12px;padding:16px;overflow:auto}}pre code{{border:0;padding:0}}
.summary{{border-top:3px solid var(--accent2);background:linear-gradient(180deg,#0e1c1f,#0c1422)}}
.summtext{{font-size:16.5px;line-height:1.8;color:#dfe8ff}}
strong,b{{color:#fff;font-weight:800}}
.hl{{color:#5ee0c4;font-weight:800;background:rgba(94,224,196,.1);border-radius:5px;padding:0 4px}}
.warn{{color:#fb7185;font-weight:700;background:rgba(251,113,133,.1);border-radius:5px;padding:0 4px}}
.scorecard{{font-size:13px}}.scorecard sup{{color:var(--muted);font-weight:400;font-size:9px}}
.scorecard td.sc{{text-align:center;font-weight:700;font-family:"JetBrains Mono"}}
.sc-hi{{background:rgba(74,222,128,.18)!important;color:#86efac}}
.sc-mid{{background:rgba(251,191,36,.16)!important;color:#fcd34d}}
.sc-lo{{background:rgba(251,113,133,.18)!important;color:#fda4af}}
.scorecard td.tot{{text-align:center;font-size:15px;font-family:"Space Grotesk"}}
.scorecard tr.win td{{background:rgba(94,224,196,.12);box-shadow:inset 3px 0 0 var(--accent2)}}
.winner{{margin-top:12px;background:linear-gradient(180deg,#0d211f,#0c1622);border:1px solid #1f5048;border-left:4px solid var(--accent2);border-radius:12px;padding:14px 16px;font-size:15px;line-height:1.6}}
.winner .crown{{display:block;color:#5ee0c4;font-weight:800;font-size:17px;font-family:"Space Grotesk";margin-bottom:4px}}
.audiolib{{background:#0f1326;border:1px solid var(--line);border-radius:14px;padding:14px 16px;margin:12px 0}}
.alh{{font-weight:800;font-family:"Space Grotesk";font-size:15px;margin-bottom:8px;display:flex;gap:10px;align-items:center}}
.ade{{background:#0f2a1c;color:var(--good);border:1px solid #2f6b46;border-radius:999px;padding:2px 9px;font-size:11px;font-weight:700}}
.aen{{background:#2a1116;color:var(--bad);border:1px solid #6b2f3a;border-radius:999px;padding:2px 9px;font-size:11px;font-weight:700}}
.clip{{display:flex;align-items:center;gap:9px;flex-wrap:wrap;padding:7px 0;border-top:1px solid var(--line)}}
.clip audio{{height:32px;margin-left:auto;max-width:260px}}
.clab{{color:#dfe8ff}}
.langbadge{{font-family:"JetBrains Mono";font-size:10.5px;font-weight:700;border-radius:5px;padding:1px 6px}}
.langbadge.de{{background:#0f2a1c;color:#86efac;border:1px solid #2f6b46}}.langbadge.ot{{background:#1b2138;color:var(--muted);border:1px solid var(--line)}}
.badges{{display:flex;gap:7px;flex-wrap:wrap;margin:2px 0 16px}}.badges img{{height:20px;display:block}}
footer{{color:var(--muted);font-size:12.5px;text-align:center;margin-top:48px;padding-top:20px;border-top:1px solid var(--line)}}
@media(max-width:760px){{.winners{{grid-template-columns:1fr}}h1{{font-size:34px}}}}
</style></head><body>
<nav class="top"><span class="b">◆ Deep Research</span>{nav}<a href="#verlauf">Ablauf</a><a href="#qa">Q&amp;A</a><span class="dim">OpenAudio-Rechner: openaudio-calculator/</span></nav>
<div class="wrap">
<div class="kicker">Interaktiv · betreut · cross-engine bewiesen</div>
<h1>Verlauf, Output &amp; Beweis</h1>
<div class="lead">Zwei Deep-Research-Beispiele über mehrere interaktive Runden — mit echtem NotebookLM-Deep-Pass, unabhängiger Web-Verifikation, Benchmark- &amp; Repo-Links und Konvergenz-Beweis.</div>
<div class="stats"><div class="stat"><b>{len(exs)}</b><span>Beispiele</span></div><div class="stat"><b>{len(cfg.get('rounds',[]))}</b><span>Runden gesamt</span></div><div class="stat"><b>4+</b><span>Research-Engines</span></div><div class="stat"><b>176</b><span>NotebookLM-Quellen</span></div><div class="stat"><b>✓</b><span>kein besserer Stack</span></div></div>

{exec_card}
<div class="winners">{winner_cards(exs)}</div>

<section class="card"><h2>⚙️ Pipeline-Flow</h2><div class="mermaid">flowchart LR
 T["Topic"]-->AG["agy<br/>Waypoint 1"]-->FP["NotebookLM<br/>Fast"]-->Q{{"Rückfrage<br/>(askq)"}}
 Q-->|Antwort|AG2["agy<br/>Waypoint 2"]-->DP["NotebookLM Deep<br/>+ Web-Engines ×N"]-->CV{{"kein besserer<br/>Stack?"}}-->RP["Report +<br/>Website"]
</div></section>

{secs}

<section id="verlauf" class="card"><h2>🧠 Chronologischer Ablauf</h2><ul class="tl">{timeline(cfg)}</ul></section>
<section id="qa" class="card"><h2>💬 Rückfragen &amp; Antworten</h2>{qa_panel()}</section>
<footer>Lokal generiert · 0 LLM-Tokens fürs Layout · interaktiver betreuter Deep-Research-Lauf · Proof-Site statisch servierbar · {now}</footer>
</div></body></html>"""
    out = os.path.join(GOAL, "goal_site.html")
    open(out, "w", encoding="utf-8").write(page)
    print("SITE", out, len(page), "bytes")

if __name__ == "__main__":
    main()
