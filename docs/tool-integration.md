# Tool Integration Guide for Maintainers

This development guide is outside the distributable skill. Keep research, candidate comparisons, and integration planning here rather than in the agent's runtime instructions.

See [tool-research.md](tool-research.md) for candidate research. The runtime download and remote-service consent rules remain in [the skill](../skills/auto-music-analysis/SKILL.md).

## Adding a tool

After the user selects a tool, record integration details in the repository's development documentation. Include only the instructions actually needed to call an integrated tool in the distributable skill. Verify the real documentation and executable interface rather than guessing commands or parameters from the tool's name.

Each record should contain:

| Field | Information to record |
| --- | --- |
| Identity and status | Tool name; planned, integrated, or unavailable; verified version |
| Capabilities and limitations | Supported analysis tasks, instruments or parts, and conclusions the tool cannot establish |
| Source and distribution | Official source, license, checkpoint source, and separate restrictions on use or redistribution |
| Environment and installation | Dependency versions, supported platforms, CPU or GPU requirements, and necessary installation steps |
| Download approval | Weight files, bundled models, first-use download behavior, estimated transfer and installed sizes, cache location, heavyweight dependencies, and the scope approved by the user |
| Invocation | CLI, Python API, MCP, or HTTP; exact entry point, arguments, and success or failure indicators |
| Input | Formats, sample rate, channels, duration limits, and required preprocessing |
| Output | Files or return structures, time units and origin, pitch representation, label vocabulary, and meaning of confidence scores |
| Operating conditions | Local or remote execution, audio uploads, retention, fees or quota consumption, approved upload and spending scope, and credential variable names; keep credentials out of the skill |
| Verification evidence | Characteristics of the verification input, actual invocation, observed artifacts, and known failure cases |

Documentation alone leaves a tool in the planned state. Mark it integrated only after executing it and checking valid output. Install checkpoints and third-party programs under their own licenses; distributing this skill does not establish permission to redistribute those dependencies.

## Current implementation

| Capability | Delivery | Verification status |
| --- | --- | --- |
| Basic analysis | `scripts/analyze_audio.py`, FFmpeg, librosa 0.11.0; optional Matplotlib | Executed on synthetic fixtures and a user-provided MP3; see below |
| Source separation | Documented external audio-separator CLI and Music AI links | Interface reviewed; not installed or run |
| Pitched transcription | Documented external Basic Pitch CLI and Klangio links | Interface reviewed; not installed or run |
| Drum events | Documented Music AI component stems and Omnizart entry points | Interface reviewed; no drum classification validated |

Do not install every backend to satisfy skill installation. The helper makes no HTTP requests, has no model weights, does not install dependencies, and decodes through existing FFmpeg. The distributed requirements split numerical analysis from optional plotting. No spectrogram-specific model is needed.

The key baseline correlates pooled harmonic STFT chroma against Krumhansl-Kessler major/minor profiles (see [music21's profile documentation](https://music21.org/music21docs/moduleReference/moduleAnalysisDiscrete.html)). It is project glue around librosa features, not a claim that librosa has a universal mode classifier. Tempo uses [librosa beat tracking](https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html); onsets use [onset detection](https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html). Unnormalized harmonic power weights the pooled tonal evidence; relative major/minor ambiguity and key changes remain limitations.

Main melody selection, score quantization, guitar strings/frets, and MusicXML assembly remain contextual tasks for temporary scripts using available libraries. No permanent score-export or fingering engine is added. The sample request does not establish whether the user wants vocal melody or a lead instrument, or the exact guitar notation format.

### Verification record (2026-11-06)

The user explicitly approved installation and validation of the numerical/plotting dependencies, excluding deep learning weights. Installed 40 compatible packages from PyPI in the ignored `dist/runtime-basic` environment (approximately 390 MiB of file data; shared package cache is additional). The validated Windows environment uses Python 3.13.2, librosa 0.11.0, NumPy 2.5.4, SciPy 1.18.1, and Matplotlib 3.11.2. `uv pip check` passed. The complete resolved package list is saved locally in ignored `dist/runtime-basic-installed.txt`; this is not a cross-platform lockfile.

Five CLI tests passed using generated WAV fixtures: known 120 BPM clicks with cropped time/bar coordinates and source-file preservation; silence without invented key/BPM or bar coordinates; metadata and invalid regions; corrupt input; and a C-major chord progression with numeric spectrogram/PNG exports. The known-grid fixture confirms that original-file time 2 seconds maps to bar 2 at 120 BPM with four pulses per bar and bar 1 starting at file time 0. Tests also cover visible-assumption metadata and rejection of plotting when no beat grid or user-supplied tempo exists. These checks verify basic behavior, not accuracy across musical genres or arbitrary recordings. The five-test run took 18.3 seconds after first-use imports/JIT compilation; affected plotting tests were rerun after the final pitch-axis adjustment.

Executed the full user-provided MP3 through `analyze_audio.py analyze INPUT --spectrogram --output dist/sample-basic-analysis`. Probe metadata: 114.48 seconds, 48 kHz stereo, 4,612,333 bytes. Decoded analysis region: 114.453 seconds at 22.05 kHz mono. The run took 23.55 seconds after initial runtime warm-up and produced a valid JSON report, numeric NPZ, and visually checked PNG. No GPU, model downloads, remote uploads, or paid calls were used; peak memory was not measured. The source SHA-256 was unchanged before/after execution.

The sample's baseline tempo was 107.666 BPM with 194 tracked beats and 405 generic onsets. Leading key candidates were D minor (profile correlation 0.5704) and C major (0.5408), triggering an ambiguity warning. These are measured baseline outputs, not reference annotations or a confirmed key/mode. No melody, guitar, or percussion transcription was generated or quality-validated. The latest musical-coordinate plot and matching report are in ignored `dist/sample-musical-log-analysis`. Its vertical axis is strictly logarithmic with note names (C1 through C9 marked); the horizontal axis is relative bar number, using an explicitly assumed four tracked pulses per bar and the first tracked beat as the bar-1 origin. The plot and report disclose these assumptions; no actual meter/downbeat identification is claimed. The input audio, artifacts, and virtual environments are excluded from skill distribution.

## Passing data between tools

- Preserve raw tool outputs where possible. Add small adapter scripts only when needed to bridge incompatible interfaces, and document the conversion.
- Identify audio files, sample rate, channels, and transformations relative to the original input. For timed events, record units, time origin, and analyzed region.
- Preserve original representations for pitches, notes, drums, and chords. When normalization is needed, document mappings and retain values that cannot be mapped.
- Record missing confidence as not provided. Unsupported capability, execution failure, and no detected events are distinct outcomes.
- Keep tool outputs separate from language model interpretations. Choose export formats based on integrated tools when the user requests an export.
