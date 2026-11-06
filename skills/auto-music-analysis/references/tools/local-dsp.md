# Bundled local DSP helper

Status: implemented and executed. See repository maintainer records for validation scope; this is not a trained transcription backend.

Requires Python 3.11+, FFmpeg/ffprobe on PATH, and installed numerical packages for analysis. Probe needs no Python DSP packages. Inspect the environment before using `scripts/requirements-basic.txt`; plotting additionally uses `scripts/requirements-plot.txt`. Follow [setup](../tasks/setup.md) for changes. The script itself never installs or downloads anything.

Run from the skill directory:

```sh
python scripts/analyze_audio.py probe "/absolute/path/song.mp3"
python scripts/analyze_audio.py analyze "/absolute/path/song.mp3" --output "/absolute/path/new-results"
python scripts/analyze_audio.py analyze "/absolute/path/song.mp3" --start 30 --duration 20 --spectrogram --output "/absolute/path/new-excerpt"
```

The destination must be new. The decoder loads the requested region into memory; crop long files when needed. Output times already include the crop offset.

| Artifact | Contents |
| --- | --- |
| `analysis.json` | Input/probe, analyzed region, method/versions, global BPM/beat/onset estimates, major/minor key candidates, warnings, plotting assumptions |
| `features.npz` | `frame_times_seconds`, harmonic `chroma_power`, `onset_strength`; optional STFT power/frequencies and frame bar positions |
| `spectrogram.png` | Optional [musical-coordinate plot](../tasks/spectrograms.md) |

For a known plotting grid, add `--beats-per-bar`, `--first-downbeat`, and optionally `--plot-bpm`. These supply grouping/origin/constant plot tempo; they do not detect them. Read [spectrogram guidance](../tasks/spectrograms.md) before using bar numbers.

Limitations: global tempo with half/double alternatives; no local tempo map, downbeat/meter detection, chord labels, melody/instrument transcription, or drum classes. Major/minor correlations are not probabilities. Silence yields no key/BPM estimate. Use [tempo](../tasks/tempo.md), [meter](../tasks/meter.md), or [chords](../tasks/chords.md) for missing tasks.
