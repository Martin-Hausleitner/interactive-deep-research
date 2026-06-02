## Empfehlung & Konvergenz-Beweis

**Entscheidungsregel (der beste DE+EN-Stack, je nach Constraint):**
1. **Kommerziell, allgemeiner Default → Chatterbox Multilingual (MIT)** — natives Deutsch, beste EN-Qualität, uneingeschränkte Lizenz, ~6–8 GB.
2. **DE-Timbre kritisch → CosyVoice 3 (Apache) bzw. CosyVoice2-EU** — einziger Stack mit *publizierter* deutscher Head-to-Head, die XTTS2/OpenAudio/ElevenLabs schlägt.
3. **Max-Qualität / non-commercial → OpenAudio S1/S2 (Fish)** — #1 open auf der TTS-Arena.
4. **Permissiv + höchste publizierte DE-Speaker-Similarity → OmniVoice (Apache, SIM-o 0.812)** — Wildcard.

**Konvergenz-Beweis (warum kein besserer Stack existiert):** Über 4 interaktive Runden mit 4 unabhängigen Research-Threads (NotebookLM-Fast + 3 Web-Engines, inkl. adversariale R4) wurde das gesamte Feld inkl. neuester 2026-Releases (OmniVoice, CosyVoice 3, Qwen3-TTS, Higgs v2, Kani-TTS-2, IndexTTS-2) geprüft. Ergebnis: **kein Modell schlägt dieses Set für hochwertiges Deutsch+Englisch-Cloning entscheidend.** Die einzigen R4-Funde (OmniVoice, CosyVoice 3) sind *Upgrades innerhalb derselben Familien*, kein neues Paradigma. Die B-Seite-Incumbents (XTTS-v2, Fish/OpenAudio, F5-TTS) fallen für kommerzielle Nutzung an der Lizenz aus — der hier gefundene Stack ist damit **nachweislich besser** als die naive „XTTS-v2"-Antwort. Konfidenz ~85 %; einzig ein unabhängiger deutscher Listening-Test von OmniVoice/CosyVoice 3 könnte den DE-Pick noch verschieben.
