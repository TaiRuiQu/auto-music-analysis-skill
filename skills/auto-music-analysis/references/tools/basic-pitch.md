# Basic Pitch

Status: documented external pitched-note backend; not installed or validated here. Use for [pitched transcription](../tasks/notes.md), preferably one isolated instrument. It supports polyphony and pitch bends, but notes in a mix are not instrument assignments or chord symbols.

Its package includes pretrained models, so installation itself requires weight consent under [setup](../tasks/setup.md). Check release-specific Python/platform/runtime support in a separate environment. After approved setup:

```sh
basic-pitch --help
basic-pitch "/absolute/path/new-notes" "/absolute/path/selected-part.wav" --save-note-events --save-model-outputs
```

Preserve MIDI, raw note events, and model outputs. Confirm pitch/time representations from the installed release. It does not determine main-melody intent, guitar fingering, meter changes, or cleaned notation. Follow [score assembly](../tasks/score-export.md) for those outputs.

Source, reviewed 2026-11-06: [official repository](https://github.com/spotify/basic-pitch).
