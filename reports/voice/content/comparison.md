## Finaler Vergleich — mit Benchmarks & Repo-Links (4 Runden, cross-engine)

| Stack | DE | EN | Benchmark (konkret) | Lizenz | Repo / Link |
|---|---|---|---|---|---|
| **Chatterbox Multilingual** | nativ (23 Spr.) | sehr stark | ~95 vs XTTS 75 (Quality-Test); schlägt ElevenLabs 63,75 % (Vendor-A/B) | **MIT** | [GitHub](https://github.com/resemble-ai/chatterbox) · [HF](https://huggingface.co/ResembleAI/chatterbox) |
| **CosyVoice 3 / CosyVoice2-EU** | nativ + 1000–1500 h DE-Finetune | stark | **DE-Head-to-Head: schlägt XTTS2 10/12, OpenAudio 8/12, ElevenLabs 6/12** | **Apache-2.0** | [CosyVoice](https://github.com/FunAudioLLM/CosyVoice) · [EU-Fork](https://github.com/hi-paris/CosyVoice2-EU) · [CV3-Weights](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512) |
| **OmniVoice** (k2-fsa, 4/2026) | 21,9 k h DE | stark | **SIM-o 0,812 (höchste publ. DE-Similarity)**, WER 0,964 | **Apache-2.0** | [GitHub](https://github.com/k2-fsa/OmniVoice) · [HF](https://huggingface.co/k2-fsa/OmniVoice) |
| **Qwen3-TTS** (1/2026) | nativ (10 Spr.) | stark | WER 1,84 %, SIM 0,789 (aggregat) | **Apache-2.0** | [GitHub](https://github.com/QwenLM/Qwen3-TTS) |
| **OpenAudio S1/S2 (Fish-Speech)** | nativ (13 Spr.) | **#1 open** | **TTS-Arena Elo ~1129 (#1 open-weight)**, EN-WER 0,008 | Research-Lic. (NC) | [GitHub](https://github.com/fishaudio/fish-speech) · [HF](https://huggingface.co/fishaudio/openaudio-s1-mini) |
| ~~XTTS-v2~~ | nativ | stark | Arena-Elo ~886 | CPML (**Coqui tot 12/2025**) | [GitHub](https://github.com/coqui-ai/TTS) · [HF](https://huggingface.co/coqui/XTTS-v2) |
| ~~F5-TTS-German~~ | DE-Finetune | stark | community-getestet | **CC-BY-NC** | [F5-TTS](https://github.com/SWivid/F5-TTS) · [DE-ckpt](https://huggingface.co/hvoss-techfak/F5-TTS-German) |
| Zonos-v0.1 | DE Minderheit | gut | 200 k h, 44 kHz | Apache-2.0 | [GitHub](https://github.com/Zyphra/Zonos) |
| Higgs Audio v2 | DE schwach | exzellent EN | braucht ~24 GB fürs Cloning | Apache-2.0 | [GitHub](https://github.com/boson-ai/higgs-audio) |
| ❌ disqualifiziert (kein/schwaches DE) | — | — | — | — | [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) · [IndexTTS-2](https://github.com/index-tts/index-tts) · [Kokoro](https://huggingface.co/hexgrad/Kokoro-82M) · [Orpheus](https://github.com/canopyai/Orpheus-TTS) · [OpenVoice](https://github.com/myshell-ai/OpenVoice) · [StyleTTS2](https://github.com/yl4579/StyleTTS2) |
