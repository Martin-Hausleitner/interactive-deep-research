## Cross-Engine Verifikation (Web, unabhängig von NotebookLM) — Runde 1

**Bester DE+EN-Stack:** **XTTS-v2 (idiap-Fork)** — eines der wenigen Modelle mit *nativem, trainiertem* Deutsch (nicht nur cross-lingual), ~85–95 % Clone-Similarity aus 6–10 s, ~4 GB VRAM, von idiap weiter gepflegt (Coqui-Shutdown Dez 2025).

| # | Stack | DE | EN | Lizenz | VRAM |
|---|-------|----|----|--------|------|
| 1 | **XTTS-v2** (idiap) | nativ trainiert | stark | Coqui PML (NC weights) | ~4 GB |
| 2 | **Fish-Speech / OpenAudio S1/S2** | nativ (13 Sprachen) | SOTA (#1 open auf TTS-Arena, Elo ~1129) | Code Apache-2.0; **Weights CC-BY-NC-SA** | 4–8 GB |
| 3 | **Chatterbox Multilingual** (Resemble) | nativ (23+ Sprachen) | stark | **MIT (kommerziell ok)** | ~6 GB |
| 4 | **CosyVoice2-0.5B** (+EU FR/DE-Fork) | im 9-Sprach-Base; EU-Fork DE/FR | stark | **Apache-2.0** | 4–8 GB |
| 5 | **F5-TTS + DE-Finetune** (hvoss) | nur via DE-Finetune | stark | Base MIT; DE-ckpt CC-BY-NC | 6–8 GB |

**Schlägt etwas XTTS-v2/F5/Fish für DE+EN klar? Nein.** Fish/OpenAudio ist auf Arena-Naturalness vorne (EN/allgemein), hat aber NC-Weights und KEINEN isolierten Deutsch-Benchmark, der einen DE-spezifischen Vorsprung beweist. Für DE+EN mit permissiver Lizenz + nachgewiesenem nativem Deutsch entthront nichts XTTS-v2 sauber → Trade-off, kein klares Upgrade.

**Disqualifiziert für DE+EN (kein/schwaches Deutsch):** GPT-SoVITS (kein DE), IndexTTS/2 (kein DE), Kokoro (kein DE), Orpheus (EN-only), OpenVoice v2 (DE nur "unseen"), StyleTTS2 (DE nur via Training), MaskGCT, Spark-TTS, Parler-TTS, Bark/Tortoise (legacy). Zonos-v0.1 (Apache-2.0) listet Deutsch → solide Mid-Tier-Option.

> Quellen: HF coqui/XTTS-v2 · idiap coqui-ai-TTS · fishaudio/fish-speech + openaudio-s1-mini · TTS-Arena 2026 (offlinetts.com, tts-agi HF space) · resemble-ai/chatterbox · FunAudioLLM/CosyVoice + hi-paris/CosyVoice2-EU · hvoss-techfak/F5-TTS-German · Zyphra/Zonos.
