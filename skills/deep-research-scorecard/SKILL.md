---
name: deep-research-scorecard
description: Use during deep research and tool comparisons to turn researched candidates into a weighted Σ/100 ranking, crown one winner, and explain why the winner beats the runner-up. Triggers: "score the candidates", "punkte vergeben", "Sieger küren", "weighted comparison", "100-point scorecard", "rank tools and pick a winner with justification".
version: 0.1.0
license: MIT
metadata:
  tags: [deep-research, comparison, scorecard, ranking, winner, weighted, decision]
  related_skills: [interactive-deep-research, integrative-deep-research, askq]
---

# deep-research-scorecard

`deep-research-scorecard` is a dependency-free ranking utility. Feed it a JSON
spec with candidates, criteria, weights, and evidence-backed scores; it computes
a weighted Σ/100, sorts candidates, and crowns one winner with a short rationale.

CLI: `scorecard` on PATH, or:

```bash
python3 ~/.claude/skills/deep-research-scorecard/scripts/scorecard.py
```

## When To Use

Use this after research has identified credible candidates and decision criteria:

1. Define weighted criteria that reflect the user's actual decision.
2. Score each candidate from evidence on a 0..scale range.
3. Run `scorecard spec.json` for Markdown or `scorecard spec.json --html` for an
   embeddable fragment.
4. Include the weights in the final report; changing weights can change the winner.

## JSON Spec

```json
{
  "title": "Best open-source DE+EN voice cloning",
  "scale": 10,
  "criteria": [
    {"key": "de", "label": "German quality", "weight": 3},
    {"key": "license", "label": "Commercially usable", "weight": 3}
  ],
  "candidates": [
    {
      "name": "CosyVoice 3.0",
      "link": "https://github.com/FunAudioLLM/CosyVoice",
      "note": "Apache license; strong multilingual support.",
      "scores": {"de": 9, "license": 10}
    }
  ]
}
```

## Commands

```bash
scorecard data/voice_scorecard.json
scorecard data/voice_scorecard.json --html > /tmp/scorecard.html
cat spec.json | scorecard -
```

Markdown output contains a ranked table and winner explanation. HTML output emits
`<table class="scorecard">` plus `<div class="winner">` for local reports/sites.

## Validation And Exit Behavior

- stdout is the rendered scorecard only.
- malformed JSON or an invalid spec exits non-zero with a concise stderr error.
- `criteria` must be a non-empty list with `key`, `label`, and numeric `weight`.
- `candidates` must be a non-empty list with `name` and `scores`.
- every score must be numeric and within `0..scale`.
- missing scores are allowed and treated as `0`; use this deliberately.

## Guidance

- Scores should come from research evidence, not from the scorecard script.
- Keep criteria few and decision-relevant.
- Use `askq` if the human needs to confirm weights before ranking.
- Pair with `integrative-deep-research` when the report needs a decisive final
  recommendation instead of a loose comparison.
