# Select an integration stack

Maintainer selection task, reviewed 2026-11-06. This file is not bundled. Canonical tool details and official sources now live in one file per tool inside the skill, so a distributed copy has the references it needs. Execution and quality evidence remain in [tool-integration.md](tool-integration.md).

## Start from the observed task

Read [process lessons and integration priorities](../skills/auto-music-analysis/references/tasks/tool-selection.md) for the harmony/rhythm trial and its unresolved gaps. The trial supports improving the workflow; it does not benchmark the candidate tools.

- For harmony, use the [chord task](../skills/auto-music-analysis/references/tasks/chords.md): evaluate [Chordino](../skills/auto-music-analysis/references/tools/chordino.md) with [Sonic Annotator](../skills/auto-music-analysis/references/tools/sonic-annotator.md) before repeatedly rebuilding a template decoder. [Omnizart](../skills/auto-music-analysis/references/tools/omnizart.md) is a separate learned candidate with a different dependency burden.
- For rhythm, use the separate [tempo](../skills/auto-music-analysis/references/tasks/tempo.md), [time-signature classification](../skills/auto-music-analysis/references/tasks/meter-classification.md), and [meter mapping](../skills/auto-music-analysis/references/tasks/meter.md) tasks. Give a usable signature candidate even before verification. Reuse [librosa rhythm functions](../skills/auto-music-analysis/references/tools/librosa-rhythm.md), then evaluate [Beat This!](../skills/auto-music-analysis/references/tools/beat-this.md) for missing beat/downbeat evidence. [madmom](../skills/auto-music-analysis/references/tools/madmom.md) is a constrained decoding option, not an arbitrary meter-change guarantee.
- For mixture interference, compare a selected [audio-separator](../skills/auto-music-analysis/references/tools/audio-separator.md) model on representative passages before committing to full-song separation. Avoid downloading every model.
- For disputed passages, use [Sonic Visualiser](../skills/auto-music-analysis/references/tools/sonic-visualiser.md) and the [review task](../skills/auto-music-analysis/references/tasks/review.md). Do not claim that feature agreement or opening a session is listening validation.
- For requested note/score outputs, follow [pitched notes](../skills/auto-music-analysis/references/tasks/notes.md) and [score assembly](../skills/auto-music-analysis/references/tasks/score-export.md), using [Basic Pitch](../skills/auto-music-analysis/references/tools/basic-pitch.md) or an appropriate transcription backend and [music21](../skills/auto-music-analysis/references/tools/music21.md).
- For original composition, arrangement, or text-driven engraving, use [Score Text](../skills/auto-music-analysis/references/tools/score-text.md): the model writes YAML, validates and repairs it, checks a rendered preview, and exports PDF/images, MIDI, or MusicXML. Audio recognition is a separate input stage when needed.

## Local and hosted choices

Reuse FFmpeg/ffprobe and the numerical stack first; their actual bundled interface is in [local DSP](../skills/auto-music-analysis/references/tools/local-dsp.md). FFmpeg handles decoding/probing, not musical recognition ([ffprobe](https://ffmpeg.org/ffprobe.html), [FFmpeg](https://ffmpeg.org/ffmpeg.html)). Add only the task-specific backend needed to fill an observed gap. Separation and full transcription are not prerequisites for every chord/BPM request.

[Music AI](../skills/auto-music-analysis/references/tools/music-ai.md) and [Klangio](../skills/auto-music-analysis/references/tools/klangio.md) are hosted alternatives. Confirm actual account workflows, outputs, local-change support, data retention, and costs; public pages alone do not establish access or accuracy. Do not infer API coverage from a consumer application.

## Promote only validated capabilities

Follow [setup authorization](../skills/auto-music-analysis/references/tasks/setup.md) before installing, loading missing weights, uploading, or paying. Record the selected runtime/checkpoint footprint, not just a package name. Check current platform and Python/NumPy compatibility before choosing an environment.

Use short, representative, authorized passages before a full run. Separate successful execution, useful outputs, musical correctness, and performance. Where annotated references exist, assess chord and beat/downbeat tasks independently with compatible vocabularies and time origins. Preserve unsupported/no-event/failure outcomes and unresolved cases.

Do not bundle third-party programs, checkpoints, private recordings, credentials, or unvalidated recording-specific scripts. Implement reusable adapters only after their real interface and benefit are established, and record the verification in [tool-integration.md](tool-integration.md).
