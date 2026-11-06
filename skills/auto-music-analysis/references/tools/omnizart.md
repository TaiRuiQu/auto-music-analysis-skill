# Omnizart

Status: documented candidate; not installed or run. Separate modules cover pitched music/vocals, drums, chords, and beats. Choose a module for the requested [notes](../tasks/notes.md), [drums](../tasks/drums.md), or [chords](../tasks/chords.md), rather than treating broad module coverage as verified quality.

For chords, the documented Python app is `omnizart.chord.app.ChordTranscription`, with `transcribe(input_audio, model_path=..., output=...)`. Recheck the installed signature, checkpoint path, output files, timestamp origin, and vocabulary before writing an adapter. Documentation of a method is not proof its checkpoint is available or compatible.

Confirm actual major/minor/unknown/no-chord mappings before promising extended labels. The published drum API describes 13 predicted classes but only three classes written to MIDI; preserve raw predictions if supported and do not promise full-kit MIDI coverage.

TensorFlow/native dependencies and checkpoints require compatibility checks and [setup consent](../tasks/setup.md). Keep this environment separate from basic DSP when necessary; do not install all modules or checkpoints by default.

Sources, reviewed 2026-11-06: [repository](https://github.com/Music-and-Culture-Technology-Lab/omnizart), [chord API](https://music-and-culture-technology-lab.github.io/omnizart-doc/chord/api.html), [drum API](https://music-and-culture-technology-lab.github.io/omnizart-doc/drum/api.html), [label constants](https://music-and-culture-technology-lab.github.io/omnizart-doc/constants.html).
