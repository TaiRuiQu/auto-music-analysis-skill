# Tool interfaces

## Local basic analysis

Run paths relative to this skill's directory. Python 3.11+ and FFmpeg/ffprobe on PATH are required. Inspect installed dependencies first. The script never downloads or installs anything. For a new environment, review the dependency resolver's download/storage impact and obtain any required setup consent before installing `scripts/requirements-basic.txt`; `scripts/requirements-plot.txt` adds optional plotting. Neither includes neural model weights.

```sh
python scripts/analyze_audio.py probe "/absolute/path/song.mp3"
python scripts/analyze_audio.py analyze "/absolute/path/song.mp3" --output "/absolute/path/new-results"
python scripts/analyze_audio.py analyze "/absolute/path/song.mp3" --start 30 --duration 20 --spectrogram --output "/absolute/path/new-excerpt-results"
# If the pulse grouping and bar-1 downbeat are known (the downbeat below is only an example):
python scripts/analyze_audio.py analyze "/absolute/path/song.mp3" --spectrogram --beats-per-bar 4 --first-downbeat 1.25 --output "/absolute/path/aligned-plot"
```

Read `analysis.json` for estimates, alternatives, methods, versions, and limitations. `features.npz` contains harmonic chroma power, onset strength, and frame times. With `--spectrogram`, it also contains STFT power/frequencies and frame bar positions, and a `spectrogram.png` is written. Stored times include the crop offset and use seconds from the original file start. Existing output directories are refused. Analysis decodes the requested region into memory; crop very long recordings.

The spectrogram uses note names on a logarithmic pitch axis (12-TET, A4=440 Hz) and bar numbers horizontally. It displays spectral energy, including overtones; recognized note events require transcription. Bar coordinates interpolate the detected beats, with linear extrapolation at the edges. `--beats-per-bar` specifies tracked pulses per bar, not a full time signature: four quarter-note pulses for 4/4, or two dotted-quarter pulses for 6/8 when that is the tracker's pulse. `--first-downbeat` is the bar-1 start in original-file seconds, including for cropped plots. Without these inputs, the plot explicitly labels its assumptions: four tracked beats per bar and the first tracked beat as bar 1. These are relative bars, not detected meter/downbeats. Provide `--plot-bpm` to use a known constant-tempo plot grid, especially when no usable beats are detected; it does not replace the measured BPM. Its default bar origin is the original file start, labeled assumed unless specified. Without a usable grid or provided plotting tempo, plotting fails clearly instead of inventing a bar axis.

Tempo is a global estimate with half/double pulse alternatives; it does not establish meter/downbeats. Key matching returns major/minor candidates, not arbitrary modes or key changes. Correlations are not probabilities. Silent regions produce no key/BPM estimate. Onsets do not identify drum instruments.

## Source separation (external)

[audio-separator](https://github.com/nomadkaraoke/python-audio-separator) provides local CLI/Python inference. After installation and weight-download consent, check the installed version's model list/help, then use an explicitly approved model filename and cache directory:

```sh
audio-separator --help
audio-separator --list_models
audio-separator "/absolute/path/song.mp3" --model_filename "APPROVED_MODEL_FILENAME" --model_file_dir "/absolute/path/approved-model-cache" --output_dir "/absolute/path/stems" --output_format WAV
```

The inference command automatically downloads missing model files. Do not run it before consent. For guitar/vocals/drums, use a model that actually exposes those stems; a vocals/accompaniment model cannot do this. Keep stem names, duration, and alignment from actual results; separation can leak other instruments.

Hosted entry points: [Music AI musical stems](https://music.ai/modules/stem-separation/musical-stems/) and [API quick start](https://music.ai/docs/getting-started/quick-start/). Confirm the account's workflow ID and parameter schema. Module pages and workflow APIs can use different input names; do not invent workflow IDs or translate fields by guesswork. The public quick-start's two-stem example is insufficient for guitar isolation.

## Pitched transcription (external)

[Basic Pitch](https://github.com/spotify/basic-pitch) transcribes pitched notes, preferably from one isolated instrument. Its package includes models, so installation itself requires weight consent. Check the release's supported Python/runtime versions in a separate environment; do not assume compatibility with the DSP environment.

After approved installation, its documented CLI is:

```sh
basic-pitch --help
basic-pitch "/absolute/path/notes" "/absolute/path/guitar.wav" --save-note-events --save-model-outputs
```

Preserve MIDI and raw note events. Run separately on the selected melody and guitar stems. Notes are not instrument assignments, a cleaned score, or recovered guitar fingering. Guitar tablature requires strings/frets and tuning; distinguish suggested playable fingering from the original performance.

[Klangio API](https://api-docs.klang.io/) exposes supported instrument transcription and MIDI/MusicXML/PDF/GP5 exports; request API access and verify instrument/format coverage before submitting audio. Obtain upload/cost approval and configure credentials securely. No hosted workflow or model backend is bundled or quality-validated by this skill.

## Drum events (external)

[Music AI drum stems](https://music.ai/modules/stem-separation/drum-stems/) returns kick, snare, hi-hat, toms, cymbals, and other audio stems. These are audio, not labeled note events. For sufficiently isolated component stems, local onset detection can propose hit times; validate leakage, rolls, and missed/duplicate hits before assembling percussion notation. The basic helper's onset times can be used as this timing baseline; the component label comes from the verified stem, not from the onset detector.

For direct local drum transcription, consult the [Omnizart drum API](https://music-and-culture-technology-lab.github.io/omnizart-doc/drum/api.html) only when needed, after checking environment/checkpoint impact. Its documentation describes 13 predicted classes but only 3 written to MIDI. Do not promise complete kit coverage from that export.

## Score export

Use temporary code with an available notation library such as [music21](https://music21.org/music21docs/usersGuide/usersGuide_08_installingMusicXML.html) to assemble verified events. Record tempo/meter/quantization assumptions and unresolved voices. MIDI alone is not a readable score. A MusicXML renderer is optional and subject to setup consent if heavyweight. Do not add a permanent helper for one-off formatting or conversion.
