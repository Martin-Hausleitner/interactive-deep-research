## Emotion & Expressivität — funktioniert das wirklich? (DE+EN)

| Modell | Emotions-Steuerung | Non-verbals (Lachen/Seufzen) | Deutsch? | Quelle |
|---|---|---|---|---|
| **CosyVoice 3** | Natürlichsprachliche **instruct**-Steuerung (Emotion/Tempo/Rolle) | **Ja** — `[laughter]`, `[breath]`, `<strong>` | **Ja, nativ** | [GitHub](https://github.com/FunAudioLLM/CosyVoice) · [CV3-Paper](https://arxiv.org/html/2505.17589v2) |
| **OpenAudio S1 / Fish-Speech** | 24+ Emotions-Tags + 20+ komplexe Zustände | **Ja, reichste Auswahl** — `(laughing)`,`(sobbing)`,`(sighing)` | Ja (13 Spr.) | [fish.audio/blog/s1](https://fish.audio/blog/introducing-s1) |
| **Chatterbox Multilingual** | globaler `exaggeration`-Regler (0.25–2.0) | nein (keine Tags) | **Ja, nativ (DE „excellent")** | [GitHub](https://github.com/resemble-ai/chatterbox) |
| **Orpheus** | inline Emotions-Tags | **Ja** — `<laugh><sigh><gasp>` | Ja + dedizierter DE-Finetune | [GitHub](https://github.com/canopyai/Orpheus-TTS) |
| **Higgs Audio v2** | implizit/kontextuell (SOTA EmergentTTS-Emotions EN) | teilweise (Stage-Directions) | gelistet, DE-Expressivität unbelegt | [boson.ai](https://www.boson.ai/blog/higgs-audio-v2) |
| **IndexTTS-2** | **SOTA Emotion** (entkoppelt, Emotion-Vektoren, Dauer-Control) | aus Emotions-Referenz | **❌ kein Deutsch (nur EN/ZH)** | [arXiv 2506.21619](https://arxiv.org/abs/2506.21619) |
| ~~XTTS-v2~~ | **keine native Emotion** (nur aus Referenz) | nein | Ja (Cloning) | [HF Discussion](https://huggingface.co/coqui/XTTS-v2/discussions/19) |

**Befund:** Das *technisch* beste Emotions-Modell **IndexTTS-2 ist disqualifiziert — kein Deutsch.** Unter den deutsch-fähigen Modellen gewinnt **CosyVoice 3** für *expressives* Cloning (instruct + Non-verbals + nativ DE), gefolgt von **OpenAudio S1** (reichste Tags, aber non-commercial). XTTS-v2 fällt ohne native Emotion ans Ende. **→ Die Emotions-Anforderung bestätigt CosyVoice 3 als Gesamtsieger** (knockt IndexTTS-2 raus).
