---
name: auto-music-analysis
description: Analyze music recordings for chords, tempo, meter, key, melody, instrument notes, and drums; compose, arrange, and engrave music as Score Text YAML with PDF, image, MIDI, and MusicXML exports.
---

# Music Analysis and Text Scores

Analyze the supplied recording or compose and arrange a text score within the requested scope. Load the relevant task reference below, then only the tool references it needs. The bundled helper provides basic DSP; the agent manually authors every score event and Score Text handles validation, engraving, and export. Consult each external tool's execution status and check availability on the current host. Successful local trials do not bundle those dependencies or establish musical accuracy.

## Choose a task

| Request | Read |
| --- | --- |
| Chord progression or harmony | [Chord recognition](references/tasks/chords.md) |
| BPM, beats, acceleration, or tempo changes | [Tempo mapping](references/tasks/tempo.md) |
| Time signature / meter classification | [Time-signature candidates](references/tasks/meter-classification.md) |
| Downbeats, bars, or meter changes | [Meter mapping](references/tasks/meter.md) |
| Key, mode, or tonal changes | [Tonality](references/tasks/key.md) |
| Spectrogram or musical-coordinate plot | [Spectrograms](references/tasks/spectrograms.md) |
| Melody or instrument notes | [Pitched transcription](references/tasks/notes.md) |
| Drum hits or percussion patterns | [Drum events](references/tasks/drums.md) |
| MIDI, MusicXML, tablature, or a score | [Score assembly](references/tasks/score-export.md) |
| Compose, arrange, or edit music using plain text / Score Text | [Score Text program, CLI, and syntax](references/tools/score-text.md) |
| Evidence checking and final delivery | [Result review](references/tasks/review.md) |
| Missing capability or tool selection | [Process lessons and integration priorities](references/tasks/tool-selection.md) |

## Score Text: plain-text composition and engraving

Use the user's [score-text](https://www.npmjs.com/package/score-text) CLI to arrange melody, chords, lyrics, guitar, piano, and drums in UTF-8 `.score.yaml`, then export PDF, SVG, PNG, HTML, MIDI, or MusicXML. It processes symbolic scores locally; recovering notes from audio requires the analysis tasks first.

For every score request, read [Score assembly and mandatory manual note review](references/tasks/score-export.md), including for composition and arrangement. Also read the dedicated [Score Text program, CLI, and syntax chapter](references/tools/score-text.md) for setup, event syntax, voices, meter/tempo changes, diagnostics, and layout. The [complete arrangement example](assets/score-text/ensemble.score.yaml) illustrates syntax; its musical content is not evidence for a recording.

Write YAML, run `score-text validate song.score.yaml --json`, repair diagnostics, and run `score-text render song.score.yaml -o preview.png --json` to inspect the layout before exporting the requested formats. Deliver editable YAML and the actual generated files. Label original or added material; retain evidence and uncertainty for recovered notes under the shared constraints below.

## Shared constraints

- **Manually author every score event.** The agent must decide and explicitly write every note's pitch, octave, onset, duration, voice, rest, and tie. Do not use scripts, automatic transcription imports, quantization, gap filling, or template expansion to generate a score's musical events. Analysis scripts may produce spectra, waveforms, pitch/onset candidates, and beat maps; validators and renderers may process an already manually authored score. For recordings, cross-check every event against multiple complementary sources as required by [score assembly](references/tasks/score-export.md). This applies to every part and the whole requested range, including provisional scores.
- **Manually verify and enter lyrics character by character / syllable by syllable.** Do not use automatic models, forced alignment, or scripts to assign lyrics to notes. The agent must verify each character/syllable and its note correspondence against the source, then explicitly write it into the score, including repeated passages and melismas. Text order, lyric count, and model timestamps alone do not establish correspondence. Follow [manual lyric placement](references/tasks/score-export.md#manually-verify-and-place-lyrics); keep unresolved words or placements explicit rather than inventing them.
- For recording analysis, use actual tool outputs; separate measurements, interpretation, and uncertainty. Do not invent recovered notes, chords, meter, confidence, or listening-based validation. Identify newly composed or arranged material as authored content.
- Preserve the source. Keep timestamps in original-file seconds across crops, resampling, stems, and exports.
- A global BPM is not a tempo map; beats are not a time signature. A seconds grid is not a beat grid. For bar-aligned chords or scores, follow the tempo and meter tasks first.
- For chord/rhythm reports, provide a best-effort time-signature candidate, section by section when useful. Prefer a usable provisional candidate over withholding classification until correctness is established. Mark inferred/default assumptions, give a concise alternative when ambiguous, and let review refine it; never present invented measurements as evidence.
- Reuse existing tools and intermediate features. When a suitable backend exists, prefer evaluating it over repeatedly rewriting its algorithm. A fallback remains provisional.
- Before new dependencies, model loading, uploads, or paid jobs, read [Setup and authorization](references/tasks/setup.md). Existing approvals remain valid within their scope.
- Respond in the user's language with findings, tools used, limitations, and links to verified artifacts. Consult [Result review](references/tasks/review.md) before delivery.
