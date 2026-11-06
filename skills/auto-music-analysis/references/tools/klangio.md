# Klangio API

Status: public API overview reviewed 2026-11-06; no account access, request, or output validation. Candidate for [notes](../tasks/notes.md), [chords](../tasks/chords.md), [meter](../tasks/meter.md), and [score exports](../tasks/score-export.md).

The overview advertises piano/guitar/bass/vocal transcription, MIDI/MusicXML/PDF/GP5, source separation, beat/downbeat/BPM/meter analysis, and timed chord recognition. Check the selected endpoint's actual schema, instruments, duration limits, and export coverage; consumer-app features do not establish API availability.

An advertised meter result does not establish support for changing/odd/compound time signatures or a per-section meter map. Confirm these properties and timestamp units with an actual authorized response before promising them.

Follow [setup](../tasks/setup.md) for provider access, audio upload, retention, pricing/quota, and credentials. Do not invent endpoints or token requirements from the overview. Preserve raw responses as candidate evidence. Provider-generated MIDI/MusicXML/PDF must not become the delivered score or be imported as its event source; follow [manual score assembly](../tasks/score-export.md) to cross-check and explicitly author every event. Successful provider export is not musical validation.

Sources: [API overview](https://api-docs.klang.io/), [access request](https://klang.io/api/).
