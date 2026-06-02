#!/usr/bin/env python3
"""Turn audio_demos.json into an embeddable HTML fragment: <audio> players grouped
per library, German clips first. Writes to the voice run's content/audios.html."""
import json, os, html, collections

GOAL = os.path.expanduser("~/.local/share/idr/goal_voicecloning")
OUT = os.path.expanduser("~/.local/share/idr/runs/20260602-015821-def4/content/audios.html")
BASE = "http://100.120.120.120:5181/audio/"  # local rehost on vcvm

def main():
    data = json.load(open(os.path.join(GOAL, "audio_demos.json")))
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
    open(OUT, "w", encoding="utf-8").write(frag)
    print("AUDIOS", OUT, len(frag), "bytes,", total_de, "DE clips,", len(by), "libs")

if __name__ == "__main__":
    main()
