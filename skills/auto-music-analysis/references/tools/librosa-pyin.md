# librosa pYIN

Status: executed locally for full-length monophonic vocal candidates. It returns framewise F0, voiced decisions, and voicing probability; it does not identify the lead singer or return finished note events.

Reuse a clean [vocal stem](audio-separator.md) when the request is a main vocal melody. Run `librosa.pyin` with an explicit plausible F0 range, sample rate, frame length, and hop length; retain those parameters and raw F0/probabilities. Convert frames to original-file seconds, accounting for crop and processing offsets. The executed trial used 16 kHz mono, hop 256, and C3-C5, which are recording-specific choices rather than universal vocal limits.

Continuous F0 needs onset/offset segmentation. Repeated syllables on one pitch can merge; consonants can split a note; portamento can become many chromatic fragments. Preserve raw pitch and seconds alongside quantized notes. Voicing probability measures acoustic support, not note correctness or singer identity. Explain thresholds as heuristics and label unresolved spans rather than claiming verified silence.

When the pitch trace is fragmented, compare one short passage with one justified alternative before rerunning the full song. A larger frame did not resolve a sliding passage in the trial; repeated parameter changes without reference labels should not delay a usable candidate. Evaluate [Basic Pitch](basic-pitch.md) or [Omnizart](omnizart.md) for note-event outputs, or [Tony](tony.md) for manual correction, when boundaries are the actual bottleneck.

See [pitched transcription](../tasks/notes.md) and [score assembly](../tasks/score-export.md).

Source: [official pYIN 0.11.0 API](https://librosa.org/doc/0.11.0/generated/librosa.pyin.html).
