# Assemble notation

Establish the requested parts and format. For plain-text composition, arrangement, numbered notation, guitar TAB, or multi-part engraving, use [Score Text: program, CLI, and syntax](../tools/score-text.md). Its YAML supports editable source plus PDF/SVG/PNG/HTML, MIDI, MusicXML, and normalized JSON exports. Use [music21](../tools/music21.md) for programmatic symbolic assembly/conversion or an actually supported [Klangio](../tools/klangio.md) export. Raw MIDI is not a cleaned readable score.

For original compositions or arrangements from user-supplied notes, write the symbolic score directly; audio analysis is only needed when recovering material from a recording. Mark composed additions and provisional transcription separately. Follow Score Text's validate → repair → preview → export workflow and include the editable `.score.yaml` with checked outputs.

Before quantizing, reconcile [notes](notes.md) or [drum events](drums.md) with [tempo regions](tempo.md), [meter regions](meter.md), first downbeat, pickups, and original-file offsets. Preserve proposed tempo/meter changes instead of applying one global value. If the structure remains uncertain, use a preferred [time-signature candidate](meter-classification.md) to produce an explicitly marked draft when useful; also preserve unquantized event times so the user can revise the meter. Do not present assumed bar structure as verified.

Keep voice assignments, rests, ties, quantization choices, and unresolved events explicit. Chord [recognition](chords.md) and symbolic chord spelling need their own evidence. Guitar tablature also needs tuning and string/fret choices.

Use temporary code for one-off assembly. A PDF/PNG renderer is optional; follow [setup](setup.md) if a heavyweight renderer must be installed. Verify the exported file through an available reader/renderer before delivery and disclose unverified layout or unsupported output coverage.
