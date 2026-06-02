## Echtheits-Leaderboard — harte Benchmarks (Lizenz ignoriert, nur OSS)

| Modell | SIM-o (SeedTTS) | MOS/SMOS | WER (en) | TTS-Arena Elo | Emotion | Deutsch belegt? |
|---|---|---|---|---|---|---|
| **IndexTTS-2** | **0,860** (beste) | SMOS 4,42 | **1,52 %** | – | **ES 0,887 / EMOS 4,22 (SOTA)** | ❌ nur EN/ZH/JP |
| **OpenAudio S1 (Fish)** | hoch (n/p) | „dubbing-actor", #1 Arena | **0,8 %** | **S2 Pro ~1129 (top open)** | 50+ Emotions-Marker | ❌ kein DE-Benchmark |
| **OmniVoice** | **0,830** (24-Spr.) | ≈ SOTA UTMOS/SMOS | 2,85 % | – | gering steuerbar | ✅ 600+ Spr. inkl. DE |
| **CosyVoice 3.0** | 0,718 EN / 0,78 ZH (≈ Mensch 0,755) | „übertrifft v2-Prosodie" | 1,45 % | – | Instruct-Emotion (5000h) | ✅ **nativ DE (1 von 9) + Emotion** |
| **F5-TTS** | 0,803 EN | SMOS 4,44 | 1,94 % | ~885 | gering | ✅ via Fork · **WildSpoof: am schwersten zu erkennen (menschlichst)** |
| **Chatterbox Multilingual** | n/p (63,75 % > ElevenLabs) | – | – | 1006 | **Exaggeration-Regler** | ✅ nativ (23 Spr.) |
| **Higgs Audio v2** | 0,677 | expressiv | 2,44 % | – | **EmergentTTS 75,7 % vs gpt-4o-mini-tts** | multiling., kein DE-Wert |
| **XTTS-v2** | ~F5-Tier (älter) | alternd | höher | 886 | nur via Referenz | ✅ nativ (17 Spr.) |

**Schlüssel-Befund:** Die *objektiv* echtesten/expressivsten Modelle **IndexTTS-2** (SIM-o 0,860 + SOTA-Emotion) und **OpenAudio S1** (#1 Arena) **können kein Deutsch** → für DE+EN disqualifiziert. **Nicht die Lizenz ist die bindende Schranke, sondern Deutsch.** Unter den deutsch-fähigen Modellen ist **CosyVoice 3.0** das echteste + expressivste (Ähnlichkeit ≈ menschliche Aufnahme auf ZH, CER 0,71 %, Instruct-Emotion, Deutsch erstklassig). Lizenz-Drop ändert den **englisch/global**-Sieger (→ IndexTTS-2 / OpenAudio S1), aber **nicht den DE+EN-Sieger** (CosyVoice 3.0). _Anti-Spoofing: F5-TTS-DPS war 2026 bei WildSpoof am schwersten zu detektieren; Chatterbox setzt absichtlich ein Perth-Wasserzeichen (bleibt erkennbar)._
