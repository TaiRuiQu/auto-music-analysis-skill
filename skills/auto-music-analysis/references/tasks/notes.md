# Transcribe a pitched part

Identify the desired part and output format when ambiguous. Prefer a suitable [isolated stem](../tools/audio-separator.md) for [Basic Pitch](../tools/basic-pitch.md); [Omnizart](../tools/omnizart.md) and authorized [Klangio](../tools/klangio.md) jobs are alternatives with different instrument/output coverage.

Preserve raw notes, onset/offset seconds, pitch representation, bends where supported, and unvoiced/unknown spans. A pitched-note model does not independently assign every note in a mix to its real instrument or establish the intended main melody.

For a complete main-vocal candidate, distinguish source identity, framewise pitch, and note boundaries. [pYIN](../tools/librosa-pyin.md) is a locally executed F0 option; its fast execution does not solve accompaniment leakage or same-pitch syllable segmentation. Compare one representative vocal passage and an instrumental passage before processing the whole recording. Do not keep tuning a foreground-suppression method that demonstrably follows instruments. [Tony](../tools/tony.md) is a candidate for subsequent interactive correction.

Deliver the whole requested time range with explicit unresolved/rest spans when the user prefers a candidate. State that timeline coverage is not recovery of every sung note. For numbered notation, keep the tonic reference and octave convention explicit, retain chromatic notes, and use one structured event source for text, visual score, MIDI, and MusicXML. Keep pre-grid audio and final layout padding separately accounted for.

For notation follow [score assembly](score-export.md), including [tempo](tempo.md) and [meter](meter.md). Guitar strings/frets need tuning and fingering decisions; distinguish a suggested playable arrangement from the original performance. Use temporary cleanup code rather than claiming recovered fingering from MIDI alone.
