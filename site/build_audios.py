#!/usr/bin/env python3
"""Turn site/audio_demos.json into the tracked voice report's audio fragment."""
import json, os, html, collections

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "reports", "voice", "content", "audios.html")
BASE = "http://100.120.120.120:5181/audio/"  # local rehost on vcvm

def main():
    data = json.load(open(os.path.join(HERE, "audio_demos.json"), encoding="utf-8"))
    by = collections.OrderedDict()
    for c in data:
        by.setdefault(c["lib"], []).append(c)
    blocks = []
    total_de = 0
    for lib, clips in by.items():
        clips.sort(key=lambda c: (c.get("lang") != "de", c.get("label","")))
        nde = sum(1 for c in clips if c.get("lang") == "de")
        total_de += nde
        badge = f'<span class="ade">{nde} DE-Demos</span>' if nde else '<span class="aen">nur EN/andere</span>'
        rows = []
        for c in clips:
            url = (BASE + c["local"]) if c.get("local") else c["url"]
            lang = (c.get("lang") or "").upper()
            lb = f'<span class="langbadge {"de" if c.get("lang")=="de" else "ot"}">{html.escape(lang)}</span>'
            src = f' · <a href="{html.escape(c.get("source",""))}">Quelle</a>' if c.get("source") else ""
            rows.append(f'<div class="clip">{lb}<span class="clab">{html.escape(c.get("label",""))}</span>{src}'
                        f'<audio controls preload="none" src="{html.escape(url)}"></audio></div>')
        blocks.append(f'<div class="audiolib"><div class="alh">{html.escape(lib)} {badge}</div>{"".join(rows)}</div>')
    frag = (f'<p class="dim">Echte Demo-Aufnahmen je Library — <b>deutsche Beispiele zuerst</b> '
            f'({total_de} DE-Clips gesamt). Player laden on-demand.</p>' + "".join(blocks))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(frag)
    print("AUDIOS", OUT, len(frag), "bytes,", total_de, "DE clips,", len(by), "libs")

if __name__ == "__main__":
    main()
