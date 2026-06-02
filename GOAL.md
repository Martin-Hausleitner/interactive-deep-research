# GOAL — Interactive Deep Research (2-Tage-Dauerauftrag)

## Mission
Mach das interaktive/integrative Deep-Research-System (idr-Pipeline + die Skills `integrative-deep-research`, `askq`, `interactive-deep-research`, `deep-research-scorecard` + die Beweis-Site) zu einem erstklassigen, sauber dokumentierten, getesteten Open-Source-Repo. End-Zustand: ein modernes README (mit Mermaid: wie die Pipeline funktioniert UND wie man die Skills aufruft), alle Skills sauber dokumentiert + gehärtet, die idr-Pipeline robust + mit echten E2E-Tests abgesichert (live + IDR_MOCK), die Proof-Site neu gerendert + lokal/vcvm bereitgestellt, Repo aufgeräumt (keine Duplikate, kein __pycache__ im Index), committed + gepusht (github Martin-Hausleitner/interactive-deep-research) und `main` als Default-Branch.

## Arbeitsweise (VERBINDLICH)
- IMMER Subagents + Agent-Teams: ein DOC-Subagent (README/Skills), ein TEST-Subagent (E2E + mock), ein VERIFIER-Subagent der jeden „fertig"-Claim adversarial widerlegt, bevor er zählt. Niemals solo.
- NotebookLM zwischendurch nutzen: für Design-Entscheidungen (z.B. „bester README-/Skill-Aufbau", „welche E2E-Tests") `idr plan "<frage>"` bzw. eine kurze NotebookLM-Recherche fahren und die Erkenntnis einarbeiten — Pläne werden mit NotebookLM geschmiedet, nicht geraten.
- End-to-End-Testing ist Kernthema: die idr-Pipeline muss real durchlaufen (echter `nlm`-Lauf, fast+deep) UND offline via IDR_MOCK; schreibe echte Tests, die plan→question→resume→report durchspielen. Kein Mock-only-Beweis.
- Gatekeeper/adversariale Verifikation: jeder Claim braucht echten Beweis (Test-Output, gerendertes report.html, Screenshots der Proof-Site). Verifier-Subagent muss scheitern, bevor grün.
- Nicht stehenbleiben: ~2 Tage Backlog kontinuierlich; nach jedem Etappenziel committen + pushen, dann sofort weiter. Kein Parken am Prompt. Kein PII.

## 2-Tage-Backlog (priorisiert)
1. **Repo-Cleanup**: Duplikate (Root vs site/) dedupen, __pycache__/*.pyc aus dem Index, .gitignore prüfen; Layout kanonisch (skills/ site/ reports/ data/ openaudio-calculator/).
2. **Modernes README.md** mit Mermaid-Diagrammen (Pipeline-Flow + Skill-Aufruf), Quickstart, Install, Proof-Site, Gotchas.
3. **Skills härten + dokumentieren**: integrative-deep-research, askq, interactive-deep-research (umbrella), deep-research-scorecard — jeweils saubere SKILL.md + scripts, Trigger, Beispiele.
4. **E2E-Tests**: pytest/bash, die die idr-Pipeline live (kleiner echter Lauf) + mock durchspielen; askq + scorecard mit echten Inputs; CI-tauglich.
5. **Proof-Site** neu bauen (build_goal_site.py) + lokal/vcvm servieren; `<title>` nach Push verifizieren.
6. **Push + Default-Branch main** (gh repo edit --default-branch main); README-Badges/Links prüfen.
7. **Hardening**: nlm-Fehlerpfade (login/timeout/--force), agy-Fallback, robuste Query-Parsing (.value.answer), Doku der Live-Learnings.

## Definition of Done (pro Item)
Umgesetzt + echtes E2E getestet (nicht nur mock) + Verifier-Subagent-bestätigt (echter Beweis) + committed/gepusht + im README/CHANGELOG vermerkt. Erst dann abhaken.

## Nicht aufhören
~2 Tage Arbeit. Item fertig → nächstes. Bei Unsicherheit über Design: kurze NotebookLM/idr-Recherche, dann weiter. Niemals am Prompt parken.
