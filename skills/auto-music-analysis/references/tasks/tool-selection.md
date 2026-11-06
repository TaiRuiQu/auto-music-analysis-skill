# Select tools from the observed analysis gaps

Use this task when a capability is missing or repeated fallback work is taking over the analysis. Expected benefits below are integration hypotheses, not measured accuracy or speed claims.

## What the trial actually did

1. Inspected an MP3 and reused an existing FFmpeg/librosa environment.
2. Ran the bundled helper for global tempo, major/minor key candidates, onset strength, and harmonic chroma.
3. Built temporary CQT, spectral whitening, harmonic dictionary, bass weighting, chord template, and Viterbi scripts. Revised feature weighting and vocabulary several times, then compared against STFT templates.
4. Exported a seconds-based chord table and summarized selected progressions. The final two feature paths agreed on only about 55% of triad labels; neither was ground truth. No separated stems or listening validation were used.
5. Only after the user asked about changes, computed local rhythm autocorrelation and frequency-band onsets. Several pulse candidates appeared, but actual tempo changes and meter changes remained unverified.

The avoidable work was rebuilding an existing harmony pipeline, repeatedly tuning on the same unannotated recording, and treating a global BPM as sufficient rhythm preparation. The trial does not establish that any proposed backend will correctly analyze that recording.

The user's subsequent preference is candidate-first time-signature classification: provide a usable hypothesis now, then improve it through review. The trial's unresolved meter must not become a general rule to withhold a signature. Follow [time-signature classification](meter-classification.md), including an explicit working default when evidence is weak.

## Priorities

| Priority / bottleneck | Existing tool to evaluate | Expected benefit and boundary | Task |
| --- | --- | --- | --- |
| First: hand-built chord DSP and repeated parameter revisions | [Chordino](../tools/chordino.md) via [Sonic Annotator](../tools/sonic-annotator.md) | Reuse a complete chroma/bass/template/temporal decoder; saves implementation work. Its dictionary and older algorithm still require comparison and review. | [Chords](chords.md) |
| First: one global BPM conceals local changes | [librosa rhythm functions](../tools/librosa-rhythm.md) | Reuse local tempo, PLP, and time-varying beat tracking in an existing environment; no new neural model. Periodicity is not meter. | [Tempo](tempo.md) |
| First: no beat/downbeat evidence | [Beat This!](../tools/beat-this.md) | Provides beat/downbeat events for a local tempo and bar-boundary candidate map. Requires approved weights/runtime; does not directly establish notated meter. | [Tempo](tempo.md), [meter](meter.md) |
| First: a usable time-signature answer | [Classification workflow](meter-classification.md), using available rhythm evidence; [madmom](../tools/madmom.md) for constrained comparisons | Return a preferred signature plus alternatives without waiting for verification. Model constraints, assumed beat units, and defaults stay explicit. | [Classification](meter-classification.md), [meter](meter.md) |
| Next: melody, bass, and drums interfere with harmony | [audio-separator](../tools/audio-separator.md) | Compare accompaniment/bass/drum evidence with the mix; separation can create artifacts and need not improve results. | [Chords](chords.md), [drums](drums.md) |
| Next: no direct inspection of disputed transitions | [Sonic Visualiser](../tools/sonic-visualiser.md) | Overlay labels and beat events, loop suspect passages, and save corrections. Requires an actual review action; opening a view alone is not listening validation. | [Review](review.md) |
| Alternative: local runtime/platform friction or wider chord labels | [Music AI](../tools/music-ai.md), [Klangio](../tools/klangio.md) | Hosted chord/beat outputs may reduce local setup. Verify schemas, meter-change coverage, retention, and cost; uploads require authorization. | [Chords](chords.md), [meter](meter.md) |
| When notes/scores are requested | [Basic Pitch](../tools/basic-pitch.md), [Omnizart](../tools/omnizart.md), [Sonic Visualiser](../tools/sonic-visualiser.md), [Score Text](../tools/score-text.md) | Use detectors as optional evidence, inspect every event against complementary sources, then manually author the score. Automatic transcription/import/quantization is not a score-authoring path. | [Notes](notes.md), [score](score-export.md) |

## Evaluate before promoting a backend

The subsequent full-vocal trial exposed a different ordering: separate the intended voice before improving F0; validate imports and PCM export before expensive inference; preserve samples before encoding; then address note boundaries. See [audio-separator](../tools/audio-separator.md), [pYIN](../tools/librosa-pyin.md), and [Tony](../tools/tony.md). Record timings for dependency setup, model loading, inference, and export separately. A short F0-window comparison that does not improve the disputed passage is a reason to freeze the candidate and move to note-event/manual tools, not to try many full-song parameter combinations.

Start with one backend and short representative passages, including an ambiguous chord, a suspected rhythm transition, and a quiet region. Record setup cost and runtime. Compare with an independent annotation or an actual review, not just another feature representation of the same algorithm. Where reference labels exist, compare chord vocabulary/overlap and beat/downbeat timing separately. Preserve raw labels and unresolved cases.

Promote only capabilities actually executed and checked. A tool returning a file proves execution, not correctness. Keep single-recording reports and experimental scripts outside the distributable skill; add reusable adapters only after the interface and benefit are established.
