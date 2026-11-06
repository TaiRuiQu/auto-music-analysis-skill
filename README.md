# Auto Music Analysis Skill

A distributable music analysis and arrangement skill that lets a language model coordinate audio tools, explain their results, and compose editable scores in plain text with Score Text.

The skill includes a local DSP helper for **global BPM/beat estimates, major/minor key candidates, onset timing, and optional spectrograms**. Separate task guides cover chords, local tempo, meter changes, transcription, and review; tool references describe external candidates and their actual integration status. Model weights and inference runtimes are not bundled.

Intended capabilities include BPM, key and mode, main melody, drum event distribution, instrument transcription, and chord progressions. Availability depends on the integrated tools and the current runtime environment.

## Layout

```text
skills/
└── auto-music-analysis/
    ├── SKILL.md              Task routing and shared constraints
    ├── agents/openai.yaml    Codex interface metadata
    ├── scripts/              Local analysis helper and dependency lists
        ├── assets/score-text/    Runnable multi-part Score Text YAML example
    └── references/
        ├── tasks/           One workflow per task (chords, tempo, meter, review, ...)
        └── tools/           One interface/status reference per tool

docs/                            Maintainer documents; excluded from the skill
├── tool-research.md              Integration selection and links to tool references
└── tool-integration.md           Integration planning and development notes
```

The distribution unit is the entire `skills/auto-music-analysis/` folder. It includes task-specific process lessons, integration priorities, and linked tool references. Recording-specific experiments and maintainer verification records stay outside it, together with audio, model weights, third-party programs, and credentials.

## Install with the skills CLI

Use the [`skills` CLI](https://github.com/vercel-labs/skills), distributed through npm. It discovers this repository's `skills/auto-music-analysis/SKILL.md` directly. This installation method does not require publishing this repository as an npm package or adding a `package.json`.

### From a Git repository

Install from `TaiRuiQu/auto-music-analysis-skill` on GitHub.

List the available skills without installing:

```sh
npx skills add TaiRuiQu/auto-music-analysis-skill --list
```

Install into the current project for Codex:

```sh
npx skills add TaiRuiQu/auto-music-analysis-skill --skill auto-music-analysis --agent codex
```

Add `--global` for user-wide installation, or omit `--agent codex` to select another supported agent interactively. Use `--copy` if copying files is preferred over symlinks.

### From a local clone

Run this from the project where you want to use the skill, replacing the source path with the location of this clone:

```sh
npx skills add /path/to/auto-music-analysis-skill --skill auto-music-analysis --agent codex
```

To check discovery from this repository's root without installing:

```sh
npx skills add . --list
```

The CLI installs the complete skill folder, including its interface metadata. Installation does not install audio analysis tools or model weights.

## Use

Example invocation:

```text
Use $auto-music-analysis to analyze the BPM and chord progression of this recording.
```

For text-based composition and arrangement:

```text
Use $auto-music-analysis and Score Text to arrange a short C-major piece for
voice, guitar, piano, and drums. Keep editable YAML, validate and preview it,
then export PDF and MIDI.
```

The skill has a dedicated [Score Text chapter](skills/auto-music-analysis/SKILL.md#score-text-plain-text-composition-and-engraving) and [program, CLI, and syntax reference](skills/auto-music-analysis/references/tools/score-text.md), covering notes, durations, lyrics, guitar TAB, piano, drums, independent voices, meter/tempo changes, and structured diagnostics. The [runnable ensemble example](skills/auto-music-analysis/assets/score-text/ensemble.score.yaml) illustrates syntax. The agent must manually decide and explicitly write every note, rest, and tie in `.score.yaml`; scripts must not generate the musical events. For recordings, [manual score assembly](skills/auto-music-analysis/references/tasks/score-export.md) requires event-by-event comparison of complementary evidence such as spectrograms, waveforms, source/stem comparisons, and actual playback when available, plus an event review table. Short notes, rests, and suspected syncopation receive explicit review. Analysis scripts remain available for evidence, and `score-text validate --json` and render/export commands process the manually authored source. Score Text is an external Node.js 20+ CLI; installing this skill does not install it. Original composition can start directly from text with manually authored events.

Lyrics also require [manual verification and placement](skills/auto-music-analysis/references/tasks/score-export.md#manually-verify-and-place-lyrics): the agent must check every character/syllable and its corresponding note(s), then explicitly write it into the score. Automatic lyric-to-note models, forced alignment, and scripts that distribute words across notes are prohibited. Repeated lyrics, melismas, and continuations must each be reviewed; uncertain text or placement stays explicitly unresolved.

For local analysis, reuse Python 3.11+ and FFmpeg/ffprobe where available. Review the Python dependency footprint before installing into a separate environment. Installation through `skills` installs instructions and helper files only; it never installs these dependencies or downloads models automatically.

From the installed skill directory, the helper can inspect audio without Python DSP packages:

```sh
python scripts/analyze_audio.py probe "/absolute/path/song.mp3"
```

After approved dependency setup from `scripts/requirements-basic.txt` (or `scripts/requirements-plot.txt` for plotting):

```sh
python scripts/analyze_audio.py analyze "/absolute/path/song.mp3" --output "/absolute/path/new-results" --spectrogram
```

Outputs include `analysis.json`, numeric features, and an optional spectrogram with **note names on a logarithmic pitch axis and bar numbers horizontally**. Specify known pulse grouping and bar origin with `--beats-per-bar` and `--first-downbeat`; otherwise the plot visibly labels its assumptions. The destination must be new. See the [local helper interface](skills/auto-music-analysis/references/tools/local-dsp.md) and [plot guidance](skills/auto-music-analysis/references/tasks/spectrograms.md).

The helper has no chord, local-tempo-map, downbeat, or meter-recognition command. Its key baseline compares only major/minor profiles; generic onsets have no drum classes. For the full workflow, start at [the skill's task table](skills/auto-music-analysis/SKILL.md). [Time-signature classification](skills/auto-music-analysis/references/tasks/meter-classification.md) prioritizes a usable preferred signature and alternatives, with explicit heuristic/default status when evidence is incomplete. Review refines the candidate rather than blocking it. [Process lessons and tool priorities](skills/auto-music-analysis/references/tasks/tool-selection.md) explain which existing tools could replace repeated custom DSP and fill the missing rhythm/harmony stages. Documented candidates are not claimed as installed or quality-tested.

## Packaging

Run the following PowerShell commands from the repository root to create a ZIP with a single top-level skill folder:

```powershell
New-Item -ItemType Directory -Force ./dist | Out-Null
Compress-Archive -Path ./skills/auto-music-analysis -DestinationPath ./dist/auto-music-analysis.zip -Force
```

Recipients can extract `auto-music-analysis/` into their skill search directory. The ZIP is an alternative to installation through the skills CLI.

## Integrating tools

Keep execution/validation records in [the maintainer guide](docs/tool-integration.md). Put task workflows in `references/tasks/` and tool-specific interfaces, constraints, official sources, and status in `references/tools/`. Link rather than duplicate them. Temporary scripts may prepare recording-specific evidence or validate/render/convert an already manually authored score; they must not generate or automatically clean up its musical events.

The [maintainer selection guide](docs/tool-research.md) links to the distributable tool references. Verification scope and pending backends are tracked separately from documentation-only research. Adding a reference does not install a backend or establish its quality.

The skill requires explicit consent before downloading any deep learning weights or downloading/installing heavyweight tools, including packages or first-use commands that fetch models automatically. The agent must first explain the intended download, storage and environment impact, resource needs, and alternatives. Remote audio uploads and paid API jobs also require approval for their scope. Users configure API keys locally or through a secure credential input; keys are not stored in the skill.

See the [skills CLI installation reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) and [skill discovery rules](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md) for distribution through the CLI. See the [official OpenAI Skills documentation](https://learn.chatgpt.com/docs/build-skills) for Codex skill behavior.
