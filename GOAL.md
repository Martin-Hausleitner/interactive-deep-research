# v0.1.0 Release Goal — Interactive Deep Research

Status: achieved for the first public source release, pending the final
`v0.1.0` tag and GitHub Release publication.

## Mission
Publish the interactive/integrative Deep Research system as a clean,
source-installable OSS repository: documented packaged skills, deterministic
mock verification, one opt-in live NotebookLM E2E proof, a rendered public proof
site, and public-artifact hygiene gates.

## Release Scope
1. **Repo-Cleanup**: Duplikate (Root vs site/) dedupen, __pycache__/*.pyc aus dem Index, .gitignore prüfen; Layout kanonisch (skills/ site/ reports/ data/ openaudio-calculator/).
2. **Modernes README.md** mit Mermaid-Diagrammen (Pipeline-Flow + Skill-Aufruf), Quickstart, Install, Proof-Site, Gotchas.
3. **Skills härten + dokumentieren**: integrative-deep-research, askq, interactive-deep-research (umbrella), deep-research-scorecard — jeweils saubere SKILL.md + scripts, Trigger, Beispiele.
4. **E2E-Tests**: pytest/bash, die die idr-Pipeline live (kleiner echter Lauf) + mock durchspielen; askq + scorecard mit echten Inputs; CI-tauglich.
5. **Proof-Site** neu bauen (build_goal_site.py) + lokal/remote servieren; `<title>` nach Push verifizieren.
6. **Push + Default-Branch main** (gh repo edit --default-branch main); README-Badges/Links prüfen.
7. **Hardening**: nlm-Fehlerpfade (login/timeout/--force), agy-Fallback, robuste Query-Parsing (.value.answer), Doku der Live-Learnings.

## Definition of Done (pro Item)
Umgesetzt + echtes E2E getestet (nicht nur mock) + Verifier-Subagent-bestätigt (echter Beweis) + committed/gepusht + im README/CHANGELOG vermerkt. Erst dann abhaken.

## Completion Evidence - 2026-06-03

- Public repo: `Martin-Hausleitner/interactive-deep-research`, visibility
  `PUBLIC`, default branch `main`.
- Proof site: deployed via GitHub Pages at
  `https://martin-hausleitner.github.io/interactive-deep-research/` and
  remotely validated with HTTP 200, title, Pipeline-Flow, and both examples.
- Live E2E: passed on `main` at
  `de264255019b2e69e14045611c8c60f4ab2ac74f`; run id
  `20260603-023238-bb7f`; `mock=false`; `phase=done`; `deep.ok=true`.
- CI/Pages: passing on `main`; latest evidence is recorded in
  `VERIFICATION.md`.
- Release: `v0.1.0` is the first OSS release target; final tag and GitHub
  Release evidence belong in `VERIFICATION.md`.
