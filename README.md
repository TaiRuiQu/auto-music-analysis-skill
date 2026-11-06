# Auto Music Analysis Skill

A distributable music analysis skill that lets a language model coordinate audio analysis, traditional machine learning, and deep learning tools, then explain their results.

The skill includes a local DSP helper for **BPM/beat estimates, major/minor key candidates, onset timing, and optional spectrograms**. Source separation, pitched transcription, and drum recognition use external tools documented through concise interfaces and official links. Model weights and inference runtimes are not bundled.

Intended capabilities include BPM, key and mode, main melody, drum event distribution, instrument transcription, and chord progressions. Availability depends on the integrated tools and the current runtime environment.

## Layout

```text
skills/
└── auto-music-analysis/
    ├── SKILL.md              Concise runtime instructions and consent rules
    ├── agents/openai.yaml    Codex interface metadata
    ├── scripts/              Local analysis helper and dependency lists
    └── references/tools.md   Usage interfaces and external tool links

docs/                            Maintainer documents; excluded from the skill
├── tool-research.md              Tool research and provider links
└── tool-integration.md           Integration planning and development notes
```

The distribution unit is the entire `skills/auto-music-analysis/` folder. It contains no research notes, tool selection rationale, audio, model weights, third-party programs, or credentials.

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

For local analysis, reuse Python 3.11+ and FFmpeg/ffprobe where available. Review the Python dependency footprint before installing into a separate environment. Installation through `skills` installs instructions and helper files only; it never installs these dependencies or downloads models automatically.

From the installed skill directory, the helper can inspect audio without Python DSP packages:

```sh
python scripts/analyze_audio.py probe "/absolute/path/song.mp3"
```

After approved dependency setup from `scripts/requirements-basic.txt` (or `scripts/requirements-plot.txt` for plotting):

```sh
python scripts/analyze_audio.py analyze "/absolute/path/song.mp3" --output "/absolute/path/new-results" --spectrogram
```

Outputs include `analysis.json`, numeric features, and an optional spectrogram with **note names on a logarithmic pitch axis and bar numbers horizontally**. Specify known pulse grouping and bar origin with `--beats-per-bar` and `--first-downbeat`; otherwise the plot visibly labels its assumptions. The destination must be new. Results are estimates: the key baseline only compares major/minor profiles, and generic onsets do not identify drum instruments. See [tool interfaces](skills/auto-music-analysis/references/tools.md) for plot alignment, external separation/transcription, and score export. Linked backends are not claimed as installed or quality-tested.

## Packaging

Run the following PowerShell commands from the repository root to create a ZIP with a single top-level skill folder:

```powershell
New-Item -ItemType Directory -Force ./dist | Out-Null
Compress-Archive -Path ./skills/auto-music-analysis -DestinationPath ./dist/auto-music-analysis.zip -Force
```

Recipients can extract `auto-music-analysis/` into their skill search directory. The ZIP is an alternative to installation through the skills CLI.

## Integrating tools

Keep integration planning in [the maintainer guide](docs/tool-integration.md). Keep reusable analysis code and concise invocation instructions in the skill; use temporary scripts for unusual tasks and one-off score cleanup/export.

The [tool research guide](docs/tool-research.md) compares local and hosted candidates. It is not linked from or bundled with the skill. Verification scope and pending backends are tracked in the maintainer guide.

The skill requires explicit consent before downloading any deep learning weights or downloading/installing heavyweight tools, including packages or first-use commands that fetch models automatically. The agent must first explain the intended download, storage and environment impact, resource needs, and alternatives. Remote audio uploads and paid API jobs also require approval for their scope. Users configure API keys locally or through a secure credential input; keys are not stored in the skill.

See the [skills CLI installation reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) and [skill discovery rules](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md) for distribution through the CLI. See the [official OpenAI Skills documentation](https://learn.chatgpt.com/docs/build-skills) for Codex skill behavior.
