# librosa local rhythm functions

Status: library available in the validated basic DSP environment. Local autocorrelation and frequency-band onset experiments were run; the recipes below are upstream interfaces, not bundled CLI features or a validated meter detector. Recheck the installed version; these examples target 0.11.0.

For [tempo mapping](../tasks/tempo.md), reuse cached onset strength and its sample rate/hop length rather than repeatedly decoding the full recording. A documented time-varying path is:

```python
tempo_per_frame = librosa.feature.tempo(
    onset_envelope=onset, sr=sr, hop_length=hop, aggregate=None)
_, beat_frames = librosa.beat.beat_track(
    onset_envelope=onset, sr=sr, hop_length=hop, bpm=tempo_per_frame)
beat_seconds = librosa.frames_to_time(beat_frames, sr=sr, hop_length=hop) + crop_start
```

`librosa.beat.plp(...)` is an alternative local pulse estimator; its local maxima are candidate beats. `feature.tempogram(...)` exposes local autocorrelation. Preserve priors, BPM range, window length, hop, and preprocessing because they affect pulse selection. For biased/noisy envelopes compare suitable detrending and bandwise `onset.onset_strength_multi(...)`; do not treat a preprocessing choice as validation.

These methods provide pulse/beat evidence, not downbeat or notated meter. Multiple autocorrelation peaks often express related pulse levels. A framewise tempo maximum is not a confirmed change point; retain alternatives and follow [tempo](../tasks/tempo.md) and [meter](../tasks/meter.md).

Sources, reviewed 2026-11-06: [time-varying beat example](https://librosa.org/doc/0.11.0/auto_examples/plot_dynamic_beat.html), [tempo](https://librosa.org/doc/0.11.0/generated/librosa.feature.tempo.html), [PLP](https://librosa.org/doc/0.11.0/generated/librosa.beat.plp.html), [multiband onset strength](https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_strength_multi.html).
