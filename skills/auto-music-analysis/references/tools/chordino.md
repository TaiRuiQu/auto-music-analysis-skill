# Chordino / NNLS Chroma

Status: upstream documentation reviewed 2026-11-06; not installed, executed, or quality-tested by this skill. Candidate for [chord recognition](../tasks/chords.md).

Chordino is a Vamp plugin built on NNLS Chroma, with tuning, spectral whitening, harmonic-note decomposition, chord-dictionary matching, and optional HMM/Viterbi smoothing. It can replace much of the trial's repeatedly rewritten DSP. Upstream explicitly describes a simple, non-state-of-the-art transcription method; no accuracy or speed gain on this recording has been demonstrated.

Use a compatible installed [Sonic Annotator](sonic-annotator.md) host for batch extraction, or [Sonic Visualiser](sonic-visualiser.md) for review. Discover the actual output ID through the host. The documented plugin identifier is `vamp:nnls-chroma:chordino`; the host's executable transform ID also identifies an output. Do not guess that output or its CSV schema.

Keep plugin version, `chord.dict`, tuning/whitening/roll-on settings, smoothing choice, timestamps, and raw labels. Dictionary coverage is the supported vocabulary, not every extended chord/inversion. Inspect no-chord/unknown behavior and the last event's end time. Bass chroma is evidence, not an automatic inversion guarantee.

No neural checkpoint is needed by this described algorithm, but host/plugin binaries still have platform/architecture, license, and installation requirements. Follow [setup](../tasks/setup.md) before a new installation; validate binary availability and size rather than assuming historical download links work.

Source: [official Chordino/NNLS Chroma documentation](https://isophonics.net/nnls-chroma).
