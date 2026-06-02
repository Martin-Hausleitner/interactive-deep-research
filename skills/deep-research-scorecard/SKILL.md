---
name: deep-research-scorecard
description: Use during deep research / tool comparisons to turn candidates into a POINTS-scored, weighted ranking that always crowns a winner and explains WHY. Triggers: "score the candidates", "punkte vergeben", "Sieger küren", "weighted comparison", "100-point scorecard", "rank tools and pick a winner with justification".
version: 0.1.0
license: MIT
metadata:
  tags: [deep-research, comparison, scorecard, ranking, winner, weighted, decision]
  related_skills: [integrative-deep-research, comparison-deep-research, tool-comparison-heatmap, askq]
---

# deep-research-scorecard

A tiny, dependency-free CLI that makes every deep-research comparison **decisive**:
score each top candidate per criterion, apply weights, compute a Σ/100, rank
best-first, and **crown a winner with a data-driven justification**. The math is
deterministic (in code); the per-criterion scores come from your research.

CLI: `scorecard` (on PATH) or `python3 ~/.claude/skills/deep-research-scorecard/scripts/scorecard.py`

## How to use in a deep research

1. Gather candidates + evidence (via NotebookLM / web research).
2. Pick weighted criteria (the decision drivers — e.g. quality, license, cost).
3. Score each candidate 0..scale (default 10) per criterion from the evidence.
4. Run `scorecard spec.json` → paste the markdown into the report (winner row is
   `**bold**` so renderers highlight it), or `--html` for an embeddable fragment.

## Spec (JSON)

```json
{
  "title": "Best open-source DE+EN voice cloning",
  "scale": 10,
  "criteria": [
    {"key": "de", "label": "Deutsch-Qualität", "weight": 3},
    {"key": "license", "label": "Kommerziell nutzbar", "weight": 3}
  ],
  "candidates": [
    {"name": "CosyVoice 3.0", "link": "https://github.com/FunAudioLLM/CosyVoice",
     "note": "Apache, instruct-Emotion + Non-verbals, nativ DE.",
     "scores": {"de": 9, "license": 10}}
  ]
}
```

## Output
- A `Rang | Tool | <criteria…> | Σ/100` table, sorted, winner bolded.
- The exact weights used.
- `🏆 Sieger: <name> — <score>/100` + why: its top weighted strengths, the point
  gap and which criteria it beats the runner-up on, plus its note.

`--html` emits `<table class="scorecard">` + `<div class="winner">` for websites.

## Notes
- Always state the weights — they encode the decision. Changing weights changes the winner; that transparency is the point.
- Pairs with [[integrative-deep-research]] (add a scorecard step) and [[askq]] (let a human confirm the weights).
