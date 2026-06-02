## Überblick — Bester Open-Source Voice-Cloning-Stack für Deutsch + Englisch (2026)

**Deutsch ist der entscheidende Filter.** Viele Top-Modelle 2025/26 sind EN/ZH-first und behandeln Deutsch nur als cross-lingual Best-Effort. Echte DE-Benchmarks fehlen fast völlig — es gibt **kein deutsches TTS-Leaderboard** und kaum publizierte DE-MOS/WER-Zahlen. Vier interaktive Runden (agy→NotebookLM Fast + 3 unabhängige Web-Engines) haben das Feld vermessen und gegen ein internes Baseline-Artefakt abgeglichen.

```mermaid
flowchart TD
  Q["DE+EN Voice Cloning"] --> L{"Lizenz?"}
  L -->|kommerziell| C["Chatterbox Multilingual (MIT)"]
  L -->|DE-Timbre kritisch| CV["CosyVoice 3 / CosyVoice2-EU (Apache)"]
  L -->|max Qualität, non-commercial| F["OpenAudio S1/S2 (Fish)"]
  L -->|permissiv + höchste SIM-o| O["OmniVoice (Apache)"]
```
