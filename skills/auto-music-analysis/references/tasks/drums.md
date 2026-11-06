# Identify drum events

Generic onset detection from the [local DSP helper](../tools/local-dsp.md) has no instrument labels. For labeled hits, evaluate the actual exported classes of [Omnizart](../tools/omnizart.md), or obtain authorized component stems with [Music AI](../tools/music-ai.md) and detect onsets on each stem.

Drum stems are audio, not note events. Check leakage, flams, rolls, and missed/duplicate hits before assigning component labels and combining event times. A general drums stem from [audio-separator](../tools/audio-separator.md) does not distinguish kick/snare/hi-hat by itself.

Retain original-file times, component source, thresholds, unsupported classes, and raw outputs. For patterns per beat/bar, use [tempo](tempo.md) and [meter](meter.md) before quantization; export notation through [score assembly](score-export.md).
