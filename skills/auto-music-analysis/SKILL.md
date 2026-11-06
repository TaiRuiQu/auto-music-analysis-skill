---
name: auto-music-analysis
description: Analyze user-provided music with audio analysis, machine learning, and transcription tools to explain BPM, key and mode, melody, drum events, instrument parts, and chord progressions. Use for recording analysis and audio-to-score requests; general music theory questions, composition, and lyric writing do not require this skill.
---

# Auto Music Analysis

Turn music questions into executable audio analysis tasks, then explain the results using tool evidence. The host language model coordinates the tools. This skill does not require a particular model provider or run a separate language model service.

## Tool availability

This is an initial scaffold. No audio analysis tools are integrated yet. The following table describes intended capabilities, not implemented features.

Read [references/tools.md](references/tools.md) before analysis to identify registered tools, their interfaces, and their limitations. Check availability in the current environment: an integrated tool may still be unavailable at runtime. An existing tool outside the registry may be used after verifying its real interface and capabilities; identify its source in the report.

| User goal | Required tool capability | Possible evidence-based output |
| --- | --- | --- |
| Basic information | Audio metadata, tempo, beat, key, or mode analysis | Duration, BPM, meter, tonic and mode, and supported changes over time |
| Main melody | Predominant melody extraction or pitch and note recognition for the relevant part | Timed pitch contours or note events |
| Drum distribution | Drum event detection and classification | Event times, drum classes, and beat positions when supported |
| Instrument scores | Transcription for the relevant instruments, with source separation when necessary | Notes organized by part; MIDI, MusicXML, or rendered notation when supported |
| Chord progression | Chord recognition over time | Chord labels with start and end times; harmonic function when supported by tonal evidence |

## Analysis workflow

1. Identify readable audio and the requested scope. If no accessible audio is provided, request a file or valid path. Proceed directly when the goal is clear. For a broad request such as "analyze this song," start with available basic information and a summary; produce full instrument scores only as needed.
2. Select tools and dependencies for the requested goal. A BPM request does not require full source separation and instrument transcription by default. Preserve the original audio and record cropping, resampling, channel changes, and other preprocessing.
3. Follow the tool's documented interface. Preserve raw outputs and any available tool version, model or checkpoint identifier, important parameters, and artifact paths. Mark unavailable provenance as not provided rather than inventing it.
4. Check that execution succeeded and outputs exist and are readable. Check event times against audio duration, interval ordering, and consistency between part identities and output labels. Investigate anomalous inputs or parameters; stop repeating a failed call when there is no new evidence to guide a correction.
5. Explain the results while preserving local changes, disagreements, and uncertainty. When verification is useful, inspect the relevant segment or use complementary evidence already available.

When a tool is missing, identify affected tasks and continue independent work that remains possible. If all relevant tools are unavailable, state that audio measurement cannot currently be completed and identify the capabilities needed for integration. Do not fabricate calls, BPM values, notes, drum events, or chords to fill a report.

## Evidence and timing

- Distinguish tool measurements, musical interpretation based on those measurements, and unverified judgments. Use direct listening only when the host actually supports audio perception, and label listening-based judgments accordingly.
- Report BPM, meter, key, and mode separately. A tool result for one does not automatically establish the others.
- Preserve conflicting candidates with their tools and analysis regions. Do not present a candidate as conclusive without supporting evidence.
- Quote numerical confidence only when supplied by the tool, retaining its original scale. Do not invent percentages or directly compare scores from different tools.
- Express reported times in seconds from the start of the original audio. Add crop offsets back to segment results and map time-stretched results back to the original timeline. Preserve the tool's original time basis as provenance. Do not invent bar numbers or positions within beats without supporting alignment.
- Distinguish predominant melody from full polyphonic transcription, source separation from instrument identification, and note transcription from engraved notation. Describe artifacts according to actual tool capabilities.

## Deliverables

Respond in the user's language. Lead with findings relevant to the request, then provide evidence and limitations. Include the following as applicable to completed work:

- Input file, analyzed region, and completed or unavailable tasks.
- Important measurements or time intervals; summaries and artifact files for large event lists.
- Tools, important parameters, and accessible paths to raw results and exports.
- Execution errors, alternative interpretations, and regions needing human review.

Link only to files that were actually generated and checked. Do not produce unsupported empty scores or invented data to satisfy an output format.
