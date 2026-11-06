---
name: auto-music-analysis
description: Analyze user-provided recordings for BPM, key and mode, melody, drum events, instrument parts, and chord progressions using available audio analysis and transcription tools.
---

# Music Analysis

Analyze the supplied audio within the user's requested scope. Use `scripts/analyze_audio.py` for local BPM/key candidates, timed features, and optional spectrograms; read [references/tools.md](references/tools.md) for its interface and external separation, pitched transcription, and drum tools when needed. Report unavailable capabilities clearly.

- Use documented tool interfaces and actual outputs. Do not invent measurements, notes, chords, confidence scores, or tool calls.
- Preserve the original audio. Report times in seconds from its start, accounting for crop offsets and other time transformations.
- Musical spectrograms use note names on a logarithmic pitch axis and bar numbers horizontally. Record any assumed beat grouping or bar origin; tempo alone does not establish bar lines.
- Distinguish measured results from musical interpretation and uncertainty. Describe transcription and export coverage according to actual tool capabilities.
- For melody or scores, identify the intended part and output format when ambiguous. Key candidates, unlabeled onsets, and MIDI notes alone do not establish arbitrary modes, drum classes, or guitar fingering. Use temporary scripts for one-off cleanup and score export.
- Respond in the user's language with relevant findings, tools used, limitations, and links to verified output files.

## Setup consent

Before downloading any deep learning weights or downloading/installing heavyweight tools, explain the purpose, source, expected download and storage size, environment changes, hardware needs, and runtime impact; state unknowns explicitly. Obtain explicit user consent before proceeding. This includes bundled weights and automatic downloads on first use. Reuse previously approved local tools and weights without asking again when no new download or material change is involved.

Before uploading audio or starting paid API jobs, confirm the provider, data sent, known retention conditions, and cost or quota impact unless that scope is already authorized. Have the user configure API keys locally or through secure input; never expose keys in chat, logs, reports, or the skill.
