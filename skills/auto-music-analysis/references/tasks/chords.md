# Recognize a chord progression

Deliver original-file start/end seconds, source labels, supported chord vocabulary, and unresolved alternatives. Describe whether the output covers triads, sevenths, bass notes, or inversions. Do not silently reduce an extended label to a triad.

## Choose a path

- Inspect audio and baseline tonality with the [local DSP helper](../tools/local-dsp.md). It has no chord-recognition command.
- Prefer evaluating [Chordino](../tools/chordino.md) for an existing local harmony pipeline. [Omnizart](../tools/omnizart.md) is a learned alternative with a different setup burden; confirm its label set.
- For authorized hosted jobs, inspect [Music AI](../tools/music-ai.md) or [Klangio](../tools/klangio.md). Do not assume all consumer-app chord features are in the API.
- If the mix obscures bass/harmony, compare suitable [separated stems](../tools/audio-separator.md) with the mix. A bass note alone does not identify a chord or inversion.

For chord changes in seconds, rhythm evidence can be a parallel check. Include a preferred [time-signature candidate](meter-classification.md) in the report, even if it is an explicitly assumed starting point. For chords per beat/bar, follow [tempo](tempo.md) and [meter](meter.md) before quantizing or numbering bars; provisional grids are useful when labeled. Check transitional or contrasting sections when available; a global key/BPM does not establish one loop for the recording.

## Fallback and review

If only chroma/template DSP is available, label its result provisional and retain settings, alternative labels, and no-chord/unknown regions. A CQT/STFT comparison is a diagnostic, not independent ground truth. Template similarities and agreement rates are not calibrated confidence.

Do not repeatedly add hand-tuned whitening, bass weights, smoothing, or chord vocabularies and treat improved plausibility as validation. If the result changes materially between reasonable settings, preserve ambiguity and use the [tool-selection task](tool-selection.md). Avoid creating a permanent engine from one recording's temporary scripts.

Inspect disputed roots, thirds, extensions, transitions, and fades using [result review](review.md). Correct enharmonic spelling only with retained raw labels. A .5-second sampling grid is not a beat grid; an arrow does not imply one chord per bar.
