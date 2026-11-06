# audio-separator

Status: audio-separator 0.48.0 with UVR-MDX-NET-Inst_HQ_3.onnx was executed locally on CPU and its WAV outputs checked. This was one vocals/accompaniment trial, not an accuracy benchmark or a bundled backend. Other models/stems remain documentation-only. Check the current host for an existing environment and approved model before installing. Useful for [chords](../tasks/chords.md), [notes](../tasks/notes.md), and [drums](../tasks/drums.md).

Choose the checkpoint by required stems. A vocals/accompaniment model does not isolate guitar/bass/drums. Do not assume every supported architecture exposes the same instruments. Compare the mix with the selected stems; leakage or separation artifacts may worsen recognition.

After installation consent, inspect the installed interface/model list. Before inference obtain explicit weight consent, including any first-use download, and name the chosen model/cache:

```sh
audio-separator --help
audio-separator --list_models
audio-separator "/absolute/path/song.mp3" --model_filename "APPROVED_MODEL_FILENAME" --model_file_dir "/absolute/path/approved-model-cache" --output_dir "/absolute/path/new-stems" --output_format WAV
```

Inference fetches missing model files. Inspect selected download size, runtime, GPU/CPU support, and storage under [setup](../tasks/setup.md). Preserve actual stem names and validate durations/start alignment before passing data onward. Cache reusable stems instead of rerunning separation for every task.

## Prevent expensive export retries

In the tested Windows combination, a missing `audioread` import required a dependency repair. Import the selected backend before full inference and check resolved dependencies; do not assume package installation proves runtime readiness.

With `use_soundfile=True`, the tested version propagated an MP3 input subtype (`MPEG_LAYER_III`) into WAV output and failed after inference. Decode to PCM WAV first, test the selected output encoder with a tiny signal, and specify a supported WAV subtype such as `PCM_16`. A local output adapter can preserve sample arrays before file encoding so an export failure does not force model inference again. This is a version-specific observed failure, not a claim about every export path.

Compare a quiet instrumental opening, clear solo voice, and ending using the same downstream pitch settings. Fewer instrumental pitch detections demonstrate changed interference, not transcription accuracy. A vocal stem may retain backing voices, lose weak lead syllables, or contain artifacts.

Source, reviewed 2026-11-06: [official repository](https://github.com/nomadkaraoke/python-audio-separator).
