# Tool Integration Guide for Maintainers

This development guide is outside the distributable skill. Keep recording-specific experiments, environment details, and verification history here. Task workflows and concise tool selection/interfaces live in the skill's linked references.

See [tool-research.md](tool-research.md) for the integration selection index and [runtime setup rules](../skills/auto-music-analysis/references/tasks/setup.md) for downloads, uploads, and paid jobs.

## Adding a tool

When a tool is selected for evaluation, record integration details here. Put its concise interface and limits in one `references/tools/` file and link it from relevant task guides. Label documentation-only candidates explicitly. Verify the real interface rather than guessing commands or parameters; do not promote a candidate to integrated until execution and output checks succeed.

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
| Source separation | Locally executed audio-separator 0.48.0 / one UVR vocals model; external Music AI links | WAV validity and duration checked; not bundled; musical accuracy unmeasured |
| Pitched transcription | Locally executed librosa pYIN and temporary note segmentation; external Basic Pitch / Klangio links | Full-song candidate exported and structurally checked; not listening-validated; external note backends untested |
| Drum events | Documented Music AI component stems and Omnizart entry points | Interface reviewed; no drum classification validated |
| Chord recognition | Documented Chordino/Sonic Annotator, Omnizart, Music AI, Klangio | External backends not executed; temporary template experiments are not a bundled chord recognizer |
| Local tempo | Documented librosa time-varying tempo/PLP and Beat This! | Local onset/autocorrelation experiments executed; no bundled tempo-map CLI or verified musical tempo changes |
| Downbeats and meter | Documented Beat This!, madmom, Klangio and review workflow | Not executed; no confirmed meter-change detection |
| Text composition and engraving | External `score-text@0.1.0` CLI; dedicated syntax reference and bundled YAML example | Four syntax examples and multi-part sample validated; all seven export formats exercised; PNG visually checked; see below |

Do not install every backend to satisfy skill installation. The helper makes no HTTP requests, has no model weights, does not install dependencies, and decodes through existing FFmpeg. The distributed requirements split numerical analysis from optional plotting. No spectrogram-specific model is needed.

The key baseline correlates pooled harmonic STFT chroma against Krumhansl-Kessler major/minor profiles (see [music21's profile documentation](https://music21.org/music21docs/moduleReference/moduleAnalysisDiscrete.html)). It is project glue around librosa features, not a claim that librosa has a universal mode classifier. Tempo uses [librosa beat tracking](https://librosa.org/doc/0.11.0/generated/librosa.beat.beat_track.html); onsets use [onset detection](https://librosa.org/doc/0.11.0/generated/librosa.onset.onset_detect.html). Unnormalized harmonic power weights the pooled tonal evidence; relative major/minor ambiguity and key changes remain limitations.

Main melody selection, score quantization, and guitar strings/frets remain contextual decisions based on the requested score and source evidence. Score Text supplies a text-based arrangement and engraving path; music21 remains available for programmatic symbolic assembly. No audio-to-score or fingering inference engine is bundled. For recording-specific requests, establish whether the user wants vocal melody or a lead instrument and which guitar notation format is needed.

### Verification record (2026-11-06)

The user explicitly approved installation and validation of the numerical/plotting dependencies, excluding deep learning weights. Installed 40 compatible packages from PyPI in the ignored `dist/runtime-basic` environment (approximately 390 MiB of file data; shared package cache is additional). The validated Windows environment uses Python 3.13.2, librosa 0.11.0, NumPy 2.5.4, SciPy 1.18.1, and Matplotlib 3.11.2. `uv pip check` passed. The complete resolved package list is saved locally in ignored `dist/runtime-basic-installed.txt`; this is not a cross-platform lockfile.

Five CLI tests passed using generated WAV fixtures: known 120 BPM clicks with cropped time/bar coordinates and source-file preservation; silence without invented key/BPM or bar coordinates; metadata and invalid regions; corrupt input; and a C-major chord progression with numeric spectrogram/PNG exports. The known-grid fixture confirms that original-file time 2 seconds maps to bar 2 at 120 BPM with four pulses per bar and bar 1 starting at file time 0. Tests also cover visible-assumption metadata and rejection of plotting when no beat grid or user-supplied tempo exists. These checks verify basic behavior, not accuracy across musical genres or arbitrary recordings. The five-test run took 18.3 seconds after first-use imports/JIT compilation; affected plotting tests were rerun after the final pitch-axis adjustment.

Executed the full user-provided MP3 through `analyze_audio.py analyze INPUT --spectrogram --output dist/sample-basic-analysis`. Probe metadata: 114.48 seconds, 48 kHz stereo, 4,612,333 bytes. Decoded analysis region: 114.453 seconds at 22.05 kHz mono. The run took 23.55 seconds after initial runtime warm-up and produced a valid JSON report, numeric NPZ, and visually checked PNG. No GPU, model downloads, remote uploads, or paid calls were used; peak memory was not measured. The source SHA-256 was unchanged before/after execution.

The sample's baseline tempo was 107.666 BPM with 194 tracked beats and 405 generic onsets. Leading key candidates were D minor (profile correlation 0.5704) and C major (0.5408), triggering an ambiguity warning. These are measured baseline outputs, not reference annotations or a confirmed key/mode. No melody, guitar, or percussion transcription was generated or quality-validated. The latest musical-coordinate plot and matching report are in ignored `dist/sample-musical-log-analysis`. Its vertical axis is strictly logarithmic with note names (C1 through C9 marked); the horizontal axis is relative bar number, using an explicitly assumed four tracked pulses per bar and the first tracked beat as the bar-1 origin. The plot and report disclose these assumptions; no actual meter/downbeat identification is claimed. The input audio, artifacts, and virtual environments are excluded from skill distribution.

### Full-length harmony/rhythm trial (2026-11-06)

Processed the user-provided `Une_vie_a_taimer.mp3`: 660.036 seconds in probe metadata, 660.0 decoded seconds, 44.1 kHz stereo input. Reused the approved local DSP environment; no new packages/checkpoints, remote uploads, or paid jobs. The source SHA-256 was unchanged.

The bundled helper returned global BPM 123.046875 and E-minor as its leading global profile candidate (correlation 0.7361). Neither establishes a fixed tempo or confirmed local tonality. Temporary scripts then tried CQT resolution changes, harmonic masking, whitening, nonnegative harmonic dictionaries, bass/voicing weights, several chord vocabularies, and Viterbi smoothing. The final CSV had 303 segments on a .5-second seconds grid. Final CQT and STFT triad paths agreed on 55.38%; no ground-truth accuracy or listening validation was measured. Several reported progressions remain provisional.

After the user's rhythm follow-up, temporary scripts computed detrended local onset tempograms and three frequency-band onset autocorrelations. Approximately 90- and 60-pulse/minute families were prominent in different passages, with related subdivisions and disagreements. These are periodicity candidates, not confirmed tempo or time-signature changes. No beat/downbeat model, bar/meter-change map, or trusted-score comparison was executed.

Local artifacts remain under ignored `dist/une-vie-a-taimer-basic`, `dist/une-vie-a-taimer-chords`, and `dist/une-vie-a-taimer-rhythm`; one-off scripts also remain ignored. They are not prerequisites for installing or running the skill.

Reusable corrections are captured in [process lessons and priorities](../skills/auto-music-analysis/references/tasks/tool-selection.md): evaluate an existing chord pipeline before rebuilding it; use local beat/downbeat evidence for rhythm changes; distinguish pulse counts from notated meter; retain disagreement/abstention and record what was actually reviewed. New tool references were researched, not installed or benchmarked.

The user then explicitly prioritized having a usable time-signature candidate over waiting for correctness. The new [classification task](../skills/auto-music-analysis/references/tasks/meter-classification.md) therefore returns a preferred signature, alternatives, and model/heuristic/default status. Unknown measured events remain unknown, but uncertain musical interpretation no longer blocks a provisional signature or an explicitly marked draft grid. This is workflow guidance, not a newly executed meter model.

### Full-vocal candidate trial (2026-11-06)

A supervised subagent processed the user-provided 244.246-second decoded recording. The user separately approved a CPU audio-separator environment and one 66,759,214-byte UVR-MDX-NET-Inst_HQ_3.onnx model. The official model SHA-256 was checked. The Windows environment used audio-separator 0.48.0, CPU torch 2.15.0, and onnxruntime 1.31.1; its file data occupied about 932 MiB, excluding shared caches. Missing audioread required repair; dependency checks then passed. This approval concerns this local environment/model, not arbitrary future downloads.

Traditional REPET-SIM foreground suppression took about 44 seconds but still followed instrumental strings. pYIN took about 5.5 seconds; repeated F0 tuning was not the first priority. Dedicated separation first failed after inference because the soundfile output path reused the MP3 subtype in WAV. The successful retry used PCM WAV input and explicit PCM_16 output with raw-sample backups. It took 162.58 seconds: 12.48 seconds model setup and 150.10 seconds inference/export. Output WAVs had the original decoded duration and source hash remained unchanged.

The same pYIN settings on the separated voice took 5.88 seconds including I/O, then note/score export took 2.26 seconds. In the first 12 seconds, voiced frames fell from 53.6% to 0%; this is evidence of less instrumental interference, not measured accuracy. A short 1024-versus-2048 frame comparison did not resolve slide fragmentation; parameters were frozen instead of rerunning the entire song repeatedly. Final structured events yielded 451 note candidates and 141 provisional 4/4 bars at a beat-time regression tempo of 138.005 BPM. JSON coverage/bar sums, MusicXML parse/bar durations, and MIDI paired note events were checked. A full timeline with unresolved spans is not proof that every sung note was recovered. No listening or trusted-score validation occurred.

Recording-specific logs, scripts, stems, editable outputs, and the supervision report remain in ignored `dist/viva-*` locations. Reusable lessons are in the [vocal note task](../skills/auto-music-analysis/references/tasks/notes.md), [audio-separator](../skills/auto-music-analysis/references/tools/audio-separator.md), [pYIN](../skills/auto-music-analysis/references/tools/librosa-pyin.md), and [Tony](../skills/auto-music-analysis/references/tools/tony.md) references. No models, audio, runtimes, or single-recording scripts are added to the skill distribution.

### Score Text integration trial (2026-11-06)

Integrated the user's [Score Text](../skills/auto-music-analysis/references/tools/score-text.md) into task routing, score assembly, interface metadata, and the README. The dedicated English reference covers the program, CLI, Score Text v1 syntax, and validate/repair/preview/export workflow. The bundled original English arrangement at `assets/score-text/ensemble.score.yaml` contains voice, guitar, piano, and drums across 4/4, 6/8, and 3/4. No audio transcription is implied.

Verified the published npm `score-text@0.1.0` tarball against its registry SHA-1 and ran its built CLI on Node.js 22.23.4. The archive was 14,567,052 bytes compressed and 18,374,823 bytes unpacked before dependencies. Reused the existing adjacent Score Text project's dependencies through a junction in ignored `dist/score-text-qa/package/node_modules`; no global install or new dependency stack was created. No model weights, credentials, audio uploads, or paid calls were used. Package code is MIT; bundled fonts retain their own licenses. The program and dependencies remain outside the distributed skill.

All four YAML examples in the reference passed parsing and layout after adding the explicitly documented surrounding score structure to fragments. The bundled arrangement passed CLI validation as three bars, four tracks, one page. Inspected normalized events and checked every voice's tick sum against its bar. A deliberately shortened voice returned exit code 1 and a `BAR_DURATION` diagnostic on stderr with no stdout result; successful `inspect` returned a raw score without an `ok` wrapper.

Exercised PNG, PDF, SVG, HTML, MIDI, MusicXML, and JSON exports. Checked file signatures or parsed structures as appropriate. An independent MIDI reader recovered four tracks, 76 notes, all three time signatures, and the expected quarter-note-equivalent tempo values. An independent XML parser found four parts with three measures each; this was a structural check, not MusicXML XSD validation. Visually inspected the final English PNG for part alignment, lyrics, chord diagrams, meter changes, and page fit. No listening validation or cross-editor rendering was performed.

The skill frontmatter validator and portable-reference checks passed; all 29 skill Markdown documents were reachable with no missing local links. An English-language scan found no Chinese characters in the distributed skill or README. Temporary verification code, the tarball, runtime junction, export files, and `verification.json` remain in ignored `dist/score-text-qa/`.

## Passing data between tools

- Preserve raw tool outputs where possible. Add small adapter scripts only when needed to bridge incompatible interfaces, and document the conversion.
- Identify audio files, sample rate, channels, and transformations relative to the original input. For timed events, record units, time origin, and analyzed region.
- Preserve original representations for pitches, notes, drums, and chords. When normalization is needed, document mappings and retain values that cannot be mapped.
- Record missing confidence as not provided. Unsupported capability, execution failure, and no detected events are distinct outcomes.
- Keep tool outputs separate from language model interpretations. Choose export formats based on integrated tools when the user requests an export.
