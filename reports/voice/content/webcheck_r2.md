## Runde 2 — Deutsch-spezifische Evidenz (Web)

**Kernbefund:** Echte Deutsch-spezifische Benchmarks existieren kaum. Das EINZIGE Modell mit einer publizierten deutschen Head-to-Head-Evaluation ist **CosyVoice2-EU** (hi-paris).

| Rang | Modell | Deutsch-Evidenz | Harte DE-Zahlen? |
|---|---|---|---|
| 1 | **CosyVoice2-EU** | schlägt XTTS-v2 in 10/12 Zellen, von deutschen Hörern höher bewertet; 1000h DE-Training; bis 90% rel. WER-Reduktion | JA (Paper, self-reported) |
| 2 | **F5-TTS German** (hvoss/marduk-ra) | dedizierte DE-Checkpoints; dok. Fehler (Akronyme „KI", „Dornröschen") | nein, nur qualitativ |
| 3 | **XTTS-v2** | natives DE, de-facto-Baseline, große Community | nein |
| 4 | **Chatterbox Multilingual** | DE unter 23 Sprachen; Qualitätsdaten nur EN-Blindtest | nein |
| 5 | **Fish-Speech/OpenAudio S1** | DE unterstützt; starke Metriken EN-only; Nutzer berichten DE-Inkonsistenz | nein |
| 6 | **Zonos** | DE unterstützt, 44kHz, eSpeak-Phonemisierung | keine Eval |

**Hat etwas bewiesene DE-Überlegenheit ggü. XTTS-v2? Genau eins: CosyVoice2-EU** (einzige publizierte DE-inklusive Eval, die XTTS-v2 direkt schlägt). Sonst: kein DE-Leaderboard, keine publizierten DE-MOS/WER → Modellwahl auf harten DE-Daten nur via CosyVoice2-EU möglich; alles andere braucht eigene Native-Speaker-A/B-Tests.
