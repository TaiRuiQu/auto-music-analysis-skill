# Music AI

Status: public documentation reviewed 2026-11-06; no authenticated workflow, upload, paid request, or quality test. Hosted candidate for [chords](../tasks/chords.md), [tempo](../tasks/tempo.md), and [drums](../tasks/drums.md).

| Documented module | Useful output / boundary |
| --- | --- |
| Chords | Root key and timed chord annotations with multiple chord classes; inspect actual vocabulary and bass fields |
| Beats | Numeric BPM and `beatMap` annotations with time/beat number; verify whether returned events support local tempo/downbeat/meter analysis rather than assuming a change map |
| Musical stems | Separated audio; choose actual supported parts |
| Drum stems | Kick/snare/hi-hat/toms/cymbals/other audio; not drum-note events |

Read [setup](../tasks/setup.md) before uploading or paying. Confirm account access, actual workflow ID, parameter schema, retention, and module-dependent costs. Public module pages use `inputFileUrl`, but the account workflow API may use different configured parameters; do not invent or translate identifiers by guesswork.

Preserve raw asynchronous-job outputs and actual file formats. Validate JSON-string versus file-URL outputs, timestamps, units, and label sets against the selected workflow. Keep provider confidence semantics. Global key or BPM is not a local key/tempo/meter map; follow the corresponding task for derived claims.

Sources: [quick start](https://music.ai/docs/getting-started/quick-start/), [file formats](https://music.ai/docs/api/file-formats/), [chords](https://music.ai/modules/transcription/chords/), [beats](https://music.ai/modules/transcription/beats/), [musical stems](https://music.ai/modules/stem-separation/musical-stems/), [drum stems](https://music.ai/modules/stem-separation/drum-stems/).
