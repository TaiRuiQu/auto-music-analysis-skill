# music21

Status: documented symbolic export option; no installed runtime/export validation claimed here. It reads/writes symbolic formats such as MIDI and MusicXML; it does not transcribe audio.

Use it only to inspect, validate, or convert an already manually authored symbolic score under [score assembly](../tasks/score-export.md). Do not use temporary code to create musical events, import model MIDI into a score, quantize, infer rests, or automatically repair durations. Preserve the authored pitches, voices, durations, ties, tempo/meter changes, and uncertainty; inspect conversions for silent event changes. Library availability does not make recovered fingering or bar structure valid.

A MusicXML reader/engraver is a separate capability; use an existing compatible renderer where available, or follow [setup](../tasks/setup.md) before installing a heavyweight application. Check generated files and rendered layout before claiming readable PDF/PNG coverage.

Source: [official import/export and notation-reader guide](https://music21.org/music21docs/usersGuide/usersGuide_08_installingMusicXML.html).
