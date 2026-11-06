# Manually author and review notation

Establish the requested parts, range, and format. Use [Score Text](../tools/score-text.md) for editable `.score.yaml` and supported PDF/SVG/PNG/HTML, MIDI, and MusicXML exports. Read this workflow for every score, including compositions, arrangements, percussion, numbered notation, and guitar TAB.

## Authoring boundary

The agent itself must reason about and explicitly write every musical event in every voice, bar by bar. Here, manual means agent-authored note decisions; it does not require the user to enter the notes. For each note decide pitch (or drum component), octave where applicable, metrical onset, duration, voice, and ties; decide every rest separately.

Do not write or run scripts that generate score events from audio, F0 frames, onset tables, detected MIDI, rules, loops, or accompaniment templates. Do not automatically import a transcription into the score, snap events to a grid, convert unvoiced frames or gaps into rests, split/merge notes by thresholds, or emit YAML/MusicXML through programmatic symbolic assembly. Calling the result a draft does not waive this rule. Do not generate an automatic score first and merely spot-check or cosmetically repair it afterward.

Scripts and tools may prepare evidence (stems, crops, waveforms, spectra, pitch/onset candidates, beat maps), save explicitly authored text, check duration arithmetic, validate, render, or convert an already manually authored score. Rendering that authored source to MIDI/MusicXML is permitted; using model MIDI as the score's event source is not. No postprocessing may silently invent, delete, split, move, or shorten events. Structural template scaffolding is allowed, but enter the actual musical content explicitly. Repeated material must also be reviewed for each occurrence; do not expand an accompaniment rule into unchecked parts.

Original compositions and arrangements from user-supplied notes use the same manual authoring rule without requiring nonexistent audio evidence. Check each event against the supplied material or compositional intent and label additions. For recording transcription, use the evidence workflow below.

## Cross-check each recovered event

1. Establish [tempo regions](tempo.md), [meter regions](meter.md), first downbeat, pickups, and original-file offsets. Keep a preferred [time-signature candidate](meter-classification.md) provisional when necessary. A plausible bar grid alone does not verify a note's rhythm.
2. Work in short phrases and inspect every event using at least two complementary evidence sources. Use a time/pitch-resolved [spectrogram](spectrograms.md) or equivalent visual pitch evidence alongside waveform/onset evidence, actual playback when available, and comparison of the original mix with a suitable stem. Use pitch models and theory as supporting clues, not authorities. Two exports or plots of the same detector are not independent confirmation. Note which evidence supports pitch and which supports boundaries.
3. Choose each pitch and octave from the fundamental/harmonic pattern, surrounding melody or voice leading, and the source context. Check octave errors, overtone substitutions, slides, vibrato, repeated same-pitch attacks, and stem leakage. Do not turn every F0 fluctuation into a separate note.
4. Decide the written onset and duration in the phrase's metrical context. Distinguish performance timing from intended notation. Inspect the boundary before and after each event instead of rounding timestamps independently. Keep actual timing observations separate from the chosen notation.
5. Write each reviewed event directly into the editable score. Keep a compact companion review table keyed by part/voice, bar, and event index, with source time span, pitch/component, beat position, written duration, evidence locations, decision/reason, and review status. Rests and tied continuations need entries too. Keep uncertainty in this table rather than unsupported Score Text fields.

If the available evidence cannot resolve an event, preserve alternatives or an unresolved span in the review table and identify any provisional notation. Missing pitch detections are not rests. Do not claim multi-source or listening validation that did not occur, or fill missing coverage with generated notes. Deliver the manually reviewed portion with explicit coverage limits when a full score cannot be supported.

## Short notes, rests, and syncopation

- Inspect every short fragment, short rest, unexpected offbeat attack, and tie across a beat/bar against the source and the surrounding phrase. Pay particular attention to isolated 32nd/64th notes, repeated tiny gaps, and a run of syncopations absent from parallel phrases; these are review triggers, not automatic errors.
- A dropout in F0, a consonant, breath noise, a transient, or separation artifacts do not by themselves establish a new note or rest. For a rest, corroborate an actual break in the target part using the source context and boundary evidence. Distinguish damping or decay from the intended notated duration; do not fill every numerical inter-event gap with a rest.
- For repeated same-pitch notes, require evidence of rearticulation rather than a detector reset. For a sustained note crossing a strong beat or bar line, choose readable durations and ties deliberately. Do not replace a real repeated attack with a tie.
- Compare suspected syncopation with the established pulse, accents, lyrics/articulation when present, and analogous phrases. Keep real short notes, rests, tuplets, and syncopation when supported. Do not enforce a blanket minimum duration, straighten the rhythm mechanically, or lengthen notes merely to make a bar add up.
- Recheck the grid or phrase interpretation when notation becomes implausibly fragmented. Resolve each affected event manually; do not fix the symptom with a smoothing, quantization, or gap-filling script.

## Manually verify and place lyrics

Do not use automatic lyric-to-note models, forced aligners, ASR timestamps, or scripts to distribute lyrics into note events. Do not zip a lyric string/word list to detected notes, assign by equal spacing or text order, or bulk-import an automatic mapping and only spot-check it. Correct text and matching item counts do not prove correct musical placement.

For recordings, work phrase by phrase: compare the lyric text with the performed words using actual playback when available, then inspect vocal attacks, vowels, note boundaries, and the metrical context. Spectrograms and waveforms support timing decisions but do not establish the identity of a word by themselves. Resolve text variants and repeated/omitted words against the actual performance; supplied lyrics are a text reference, not a timing map. Never claim to have heard or verified words when playback was unavailable.

The agent must verify and explicitly enter each Chinese character or sung syllable, and each syllable of other languages, into the corresponding score event(s). Decide one-syllable/multiple-note melismas, multiple syllables on a repeated pitch, pickups, cross-bar continuations, rests, and backing voices individually. Distinguish a new articulated syllable from the continuation of a previous vowel. A lyric continuation does not itself justify a pitch tie, and syllable count must not be used to invent note attacks or alter verified rhythm.

Add the exact character/syllable, source text location, source-time evidence, mapped event or event range, continuation status, and review status to the companion review table. Inspect each occurrence in repeated passages; do not assume identical words or placement. After verifying an item, explicitly write its `lyric` value or its position in the `lyrics` array; choose extension/placeholder markers deliberately using [Score Text syntax](../tools/score-text.md#bars-lyrics-and-independent-voices). Recheck every written item against the mapping and rendered score. Array-length validation and visual alignment alone are insufficient.

When a word or its placement cannot be established, mark it unresolved in the table and disclose the lyric coverage gap; do not silently fill it with a guessed word, a rest marker, or an automatically assigned syllable. For original settings of user-supplied lyrics, decide the text setting manually from the intended phrasing and explicitly enter every character/syllable without claiming recording-based verification.

## Validate and deliver

Keep voice assignments, chord spelling, guitar tuning/fingering, and composed additions explicit. Chord [recognition](chords.md) has its own evidence requirements. Use a single manually authored score source for all exported formats.

Run Score Text's validate → repair → preview → export workflow. Resolve bar-duration errors by reviewing the relevant events and meter; do not automatically insert rests, stretch notes, or drop content to satisfy the validator. Check every voice's total, lyric alignment, ties, and all rendered pages. When playback is actually available, compare exported playback with the original phrase and revisit discrepancies; generating MIDI is not listening validation.

Before delivery, follow [result review](review.md). Verify exported files through an available reader/renderer and disclose unsupported or unverified layout. Deliver editable `.score.yaml`, requested exports, the event review table, and concise coverage/uncertainty notes. Follow [setup](setup.md) if a heavyweight renderer must be installed.
