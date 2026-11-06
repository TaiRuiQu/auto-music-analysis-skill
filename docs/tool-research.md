# Minimum Tool Stack: Research and Integration Options

Maintainer research only. This document is outside the distributable skill and is not part of its runtime instructions.

Reviewed on 2026-11-06 using upstream documentation. This is a selection guide, not a quality benchmark. Current implementation and verification are recorded in [tool-integration.md](tool-integration.md). Availability, output schemas, pricing, checkpoints, and dependency compatibility must be rechecked during integration.

## Recommended shape

Keep one small set of bundled analysis and conversion scripts, and load specialized backends only when a task needs them. Define six capability boundaries rather than requiring six large models:

| Boundary | Local candidate | Hosted alternative | Packaging approach |
| --- | --- | --- | --- |
| Inspect and prepare audio | FFmpeg and ffprobe | Usually unnecessary | Bundle a small wrapper; link to external binaries |
| Analyze signals and draw figures | librosa, NumPy/SciPy, SoundFile, Matplotlib | Usually unnecessary for plots | Bundle original scripts; install numerical dependencies separately |
| Separate sources | audio-separator with one explicitly chosen checkpoint | Music AI musical stems; Klangio source separation | Document the provider and interface; keep weights and runtimes external |
| Transcribe pitched parts | Basic Pitch; pYIN for suitable monophonic parts | Klangio instrument transcription | Thin adapter around the chosen backend |
| Recognize drums and harmony | Omnizart drum/chord modules | Music AI chords; drum stems plus local onset detection | Thin adapters; validate supported labels and retain raw results |
| Export notation | music21; optional external notation renderer | Klangio MusicXML/PDF exports | Bundle event-to-score glue; link to a renderer only when needed |

One provider or library may fill several boundaries. These are not six mandatory installations, and a BPM-only request does not need separation or transcription.

## Two viable starting configurations

### Local route

For the smallest number of broad tool groups, evaluate FFmpeg, a librosa-based numerical stack, audio-separator, Omnizart, and music21. Omnizart can cover pitched notes, vocal melody, drums, chords, and beats, reducing the number of separate backends. This is a candidate coverage configuration, not a guarantee of transcription quality or easy installation.

For a more modular implementation, evaluate Basic Pitch for pitched notes and retain Omnizart only for supported drum/chord tasks. This adds an adapter but avoids tying every transcription task to one runtime. Omnizart's TensorFlow, madmom, Vamp, and native dependencies require a real compatibility check in an isolated environment. Do not select it solely because its task list is broad.

Start with the existing system tools and numerical scripts. Add a separator, then a pitched-note backend, then drum/chord recognition and score export as needed. Each model download remains subject to user consent.

### Hosted or hybrid route

Evaluate Music AI for musical stems, drum stems, beats/BPM, chords/key, and vocal pitch tracking. Evaluate Klangio for supported instrument transcriptions and MusicXML/PDF exports. Local numerical scripts can still produce figures, validate timestamps, and prepare reports.

This can avoid local deep learning runtimes. It does not avoid uploads, account access, quotas, fees, or task-specific limitations. A published API is not necessarily anonymous or free. Do not assume that a provider's consumer web application features are all exposed through its API.

For a smaller first milestone, Music AI plus local scripts may cover basic analysis, vocal pitch, and estimated drum event timing. Complete instrument notation still needs an appropriate note transcription and export path. Conversely, Klangio covers several boundaries itself; confirm key/mode outputs and drum API access before claiming full coverage from that provider alone.

## What to write inside this skill

The following are proposed helper responsibilities, not existing executables:

- Audio inspection and preparation: probe duration, codec, sample rate, and channels; convert or crop without changing the original; retain crop offsets and preprocessing provenance.
- Spectral figures: generate labeled STFT or log-frequency spectrograms, optional mel/CQT views, waveforms, and chromagrams; save numeric features and settings alongside images.
- Basic rhythm: return BPM candidates, beat timestamps, onset events, and local changes where supported. Onsets are not automatically drum labels; BPM is not a time signature.
- Tonal baselines: use chroma with documented profile/template matching to propose key and simple chord candidates. This matching is project logic, not a built-in universal key or mode recognizer in librosa. Label it approximate and retain ambiguity.
- Monophonic pitch: wrap pYIN for suitable isolated voices or instruments, preserving unvoiced regions. Polyphonic transcription and selecting the main melody require different evidence.
- Data adapters and reporting: normalize timestamps, preserve provider labels and confidence scales, collect artifacts, and export event tables.
- Score assembly: convert verified note events to MIDI/MusicXML with explicit tempo, meter, quantization, voices, and part assignments. Do not guess missing structure silently.

Reuse library implementations for DSP and notation instead of rebuilding them. Keep model inference, source separation, deep learning runtimes, and engraving applications external. Do not bundle model weights or install heavyweight dependencies merely to provide these helpers.

## Candidate details and official sources

### FFmpeg and ffprobe

Use ffprobe for machine-readable media metadata and FFmpeg for decoding and preparation. They do not estimate musical key, chords, or instrument notes. Reuse an existing installation first; otherwise inspect the selected build and its download impact before installation.

Sources: [ffprobe documentation](https://ffmpeg.org/ffprobe.html), [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html).

### librosa and the numerical plotting stack

librosa supplies DSP, beat tracking, chroma, and pYIN; Matplotlib renders the figures. These functions do not require pretrained deep learning checkpoints. The Python dependency stack still has an installation footprint, which must be inspected rather than described as zero-cost or dependency-free.

A spectrogram is useful evidence but is not itself a transcript or a replacement for structured note/chord detection. Keep time-frequency data and analysis settings, not just a PNG.

Sources: [beat tracking](https://librosa.org/doc/main/api/generated/librosa.beat.beat_track.html), [spectrogram visualization](https://librosa.org/doc/main/auto_tutorials/02-display/02-spectrogram.html), [chroma](https://librosa.org/doc/0.11.0/generated/librosa.feature.chroma_cqt.html), [pYIN](https://librosa.org/doc/0.11.0/generated/librosa.pyin.html).

### audio-separator

Provides CLI/Python access to UVR-family and Demucs separation models. Choose the model by required stems: a two-stem vocal separator is insufficient for drums/bass/other analysis. Four-stem and six-stem configurations offer different instrument coverage; neither identifies arbitrary orchestral parts.

The upstream project documents automatic model downloads on first use, including cache verification and possible replacement. Obtain consent before model loading or any call that could fetch or replace weights. Start with one selected model, not an ensemble or an entire model catalog. Dependency/runtime footprint may exceed the checkpoint size.

Source: [official repository and model download behavior](https://github.com/nomadkaraoke/python-audio-separator).

### Basic Pitch

Converts pitched audio to MIDI, supports polyphony and pitch bends, and is designed to generalize across instruments. Upstream says it works best on one instrument at a time. Prefer appropriate isolated parts; it does not assign every note in a full mix to its real instrument or establish which part is the main melody.

Models and inference runtimes remain subject to consent, including weights bundled with package distributions. Check the selected release's Python/platform/runtime support; do not assume it installs into the project's current interpreter without compatibility work.

Source: [official repository](https://github.com/spotify/basic-pitch).

### Omnizart

Offers separate modules for pitched music, vocal melody, drums, chords, and beats. Its broad scope makes it a candidate for reducing integration count. Check dependency compatibility and checkpoint availability before choosing it as a default backend.

The published drum API documentation describes 13 predicted classes but only three classes written to MIDI. The documented inference interface exposes bass drum, snare, and hi-hat thresholds. Verify the selected version's actual exported classes; do not promise a full drum kit from that interface. Its documented chord labels include major/minor classes and unknown/no-chord values; do not promise arbitrary extended jazz chords without checking the actual model.

Sources: [repository](https://github.com/Music-and-Culture-Technology-Lab/omnizart), [dependency declarations](https://github.com/Music-and-Culture-Technology-Lab/omnizart/blob/main/pyproject.toml), [drum API](https://music-and-culture-technology-lab.github.io/omnizart-doc/drum/api.html), [label mappings](https://music-and-culture-technology-lab.github.io/omnizart-doc/constants.html).

### music21 and optional engraving

music21 reads and writes MIDI and MusicXML and can organize symbolic music data. It does not transcribe audio. Producing readable notation also requires musical decisions about rhythm, voices, rests, and layout. Use an existing compatible MusicXML reader or renderer when PDF/PNG output is needed; install a heavyweight renderer only with consent.

Source: [official import/export and notation-reader guide](https://music21.org/music21docs/usersGuide/usersGuide_08_installingMusicXML.html).

### Music AI API

Officially documented modules include musical stems, drum stems, beats/BPM, chords/key, and vocal pitch tracking. Drum stems are separated audio files, not drum-note events: using per-stem onset detection to estimate hit times is a proposed adapter strategy that needs validation. Vocal pitch output does not establish full polyphonic instrument scores. Speech or lyric transcription must not be mistaken for audio-to-MIDI transcription.

The API uses authenticated asynchronous jobs and workflows. Account workflow configuration or template identifiers must be checked against actual account access. Costs depend on selected modules and processing; calculate the intended pipeline cost instead of assuming a single song incurs one flat fee. No authenticated request or audio upload was tested in this research.

Sources: [quick start](https://music.ai/docs/getting-started/quick-start/), [authentication](https://music.ai/docs/api/authentication/), [musical stems](https://music.ai/modules/stem-separation/musical-stems/), [drum stems](https://music.ai/modules/stem-separation/drum-stems/), [beats](https://music.ai/modules/transcription/beats/), [chords](https://music.ai/modules/transcription/chords/), [vocal pitch tracker](https://music.ai/modules/classification/vocal-pitch-tracker/), [pricing](https://music.ai/pricing/).

### Klangio API

Official API pages advertise piano, guitar, bass, and vocal transcription, MIDI/MusicXML/PDF/GP5 exports, source separation, beat/downbeat/BPM/meter analysis, and chord recognition. Access is requested through the provider. Consumer products include additional features, but their presence does not establish API access to those features, particularly drum transcription.

Check supported instruments, endpoints, plan duration limits, export availability, and retention with the provider before promising a workflow. No account access, paid request, or output quality was tested here.

Sources: [API overview and access request](https://klang.io/api/), [API documentation](https://api-docs.klang.io/).

## Acceptance boundaries for future integration

- Compare short user-authorized examples against actual listening or annotated references before making quality claims. Separate successful API execution from correct musical results.
- Test mixed music, isolated stems, silence, tempo ambiguity, and unsupported instruments as appropriate to the chosen backend; record the verified scope.
- Preserve original time alignment across crops and separated stems. Keep unsupported, failed, and no-event outcomes distinct.
- Treat major/minor estimates as limited outputs. Modal, changing-key, atonal, or non-Western music may need a different analysis method and human review.
- Never promise accurate scores for every instrument in arbitrary recordings. Preserve an explicit unsupported/uncertain result when source coverage or transcription evidence is insufficient.
- Before any installation, first-use model fetch, cloud upload, or paid run, follow the consent rules in [the skill](../skills/auto-music-analysis/SKILL.md).
