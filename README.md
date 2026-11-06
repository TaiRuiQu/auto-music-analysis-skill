# Auto Music Analysis Skill

A distributable music analysis skill that lets a language model coordinate audio analysis, traditional machine learning, and deep learning tools, then explain their results.

The skill scaffold is initialized. **No analysis tools are integrated yet, so it cannot currently calculate BPM or generate scores.** Tools will be added individually as selected by the user.

Intended capabilities include BPM, key and mode, main melody, drum event distribution, instrument transcription, and chord progressions. Availability depends on the tool registry and the current runtime environment.

## Layout

```text
skills/
└── auto-music-analysis/
    ├── SKILL.md              Activation, analysis workflow, and reporting rules
    ├── agents/
    │   └── openai.yaml       Codex interface metadata
    └── references/
        └── tools.md         Tool registry and integration contract
```

The distribution unit is the entire `skills/auto-music-analysis/` folder. Copy its supporting files together with `SKILL.md`. It contains no audio, model weights, third-party programs, or credentials.

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

The CLI installs the complete skill folder, including its references and interface metadata. Installation does not install audio analysis tools or model weights.

## Use

Example invocation:

```text
Use $auto-music-analysis to analyze the BPM and chord progression of this recording.
```

Until tools are integrated, the skill explains which capabilities are missing. The same entry point will coordinate real analysis after integration.

## Packaging

Run the following PowerShell commands from the repository root to create a ZIP with a single top-level skill folder:

```powershell
New-Item -ItemType Directory -Force ./dist | Out-Null
Compress-Archive -Path ./skills/auto-music-analysis -DestinationPath ./dist/auto-music-analysis.zip -Force
```

Recipients can extract `auto-music-analysis/` into their skill search directory. The ZIP is an alternative to installation through the skills CLI.

## Integrating tools

Record real interfaces, input and output formats, dependencies, and verification results in `skills/auto-music-analysis/references/tools.md`. Add `scripts/` inside the skill only when adapters are needed, along with tool-specific dependency instructions. Initialization does not preselect analysis libraries, models, or cloud services.

See the [skills CLI installation reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md) and [skill discovery rules](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md) for distribution through the CLI. See the [official OpenAI Skills documentation](https://learn.chatgpt.com/docs/build-skills) for Codex skill behavior.
