"""Local DSP baseline. No network calls, model weights, or automatic installation."""

import argparse
import importlib.metadata
import json
import math
from pathlib import Path
import shutil
import subprocess
import sys


SAMPLE_RATE = 22050
HOP_LENGTH = 512
N_FFT = 4096
PITCH_CLASSES = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
# Krumhansl-Kessler pitch-class profiles, also documented by music21's
# analysis.discrete.KrumhanslSchmuckler. Correlations are NOT probabilities.
PROFILES = {
    "major": [6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88],
    "minor": [6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17],
}


def run_process(command):
    result = subprocess.run(command, capture_output=True, check=False)
    if result.returncode:
        raise ValueError(result.stderr.decode("utf-8", errors="replace")[-3000:])
    return result.stdout


def executable(name):
    path = shutil.which(name)
    if path is None:
        raise ValueError(f"{name} is missing from PATH; see the tool's official installation guide.")
    return path


def probe_audio(source):
    raw = run_process([
        executable("ffprobe"), "-v", "error", "-select_streams", "a:0",
        "-show_entries", "format=duration,size:stream=index,codec_name,sample_rate,channels,duration",
        "-of", "json", str(source),
    ])
    metadata = json.loads(raw)
    if not metadata.get("streams"):
        raise ValueError("No audio stream found.")
    return metadata


def decode_audio(source, start, duration, np):
    # Output-side seeking keeps crop positions in the decoded source time domain.
    command = [executable("ffmpeg"), "-v", "error", "-nostdin", "-i", str(source)]
    command += ["-ss", str(start)]
    if duration is not None:
        command += ["-t", str(duration)]
    command += ["-map", "0:a:0", "-vn", "-ac", "1", "-ar", str(SAMPLE_RATE),
                "-f", "f32le", "pipe:1"]
    audio = np.frombuffer(run_process(command), dtype="<f4").copy()
    if audio.size < N_FFT:
        raise ValueError("The requested region has less than 0.19 seconds of decoded audio.")
    if not np.all(np.isfinite(audio)):
        raise ValueError("Decoded audio contains non-finite samples.")
    return audio


def key_candidates(chroma, np):
    # Average unnormalized harmonic power: quiet/silent frames cannot vote equally.
    vector = chroma.mean(axis=1)
    centered = vector - vector.mean()
    if np.linalg.norm(centered) <= 1e-8 * max(float(np.linalg.norm(vector)), 1e-20):
        return []
    candidates = []
    for mode, profile in PROFILES.items():
        for tonic, name in enumerate(PITCH_CLASSES):
            template = np.roll(np.asarray(profile), tonic)
            correlation = float(np.corrcoef(vector, template)[0, 1])
            candidates.append({"tonic": name, "mode": mode, "profile_correlation": correlation})
    return sorted(candidates, key=lambda item: item["profile_correlation"], reverse=True)[:5]


def bar_coordinates(times, beats, args, np):
    """Map original-file seconds onto bars without claiming downbeat detection."""
    beats_per_bar = args.beats_per_bar if args.beats_per_bar is not None else 4
    if args.plot_bpm is not None:
        origin = args.first_downbeat if args.first_downbeat is not None else 0.0
        positions = (times - origin) * args.plot_bpm / 60 / beats_per_bar + 1
        grid_source = "provided_constant_bpm"
        origin_source = "provided" if args.first_downbeat is not None else "assumed_file_start"
    else:
        if len(beats) < 2:
            raise ValueError("No usable beat grid for a bar axis. Provide --plot-bpm, "
                             "--beats-per-bar and --first-downbeat for a known grid.")

        def beat_coordinate(values):
            coordinate = np.interp(values, beats, np.arange(len(beats)))
            coordinate = np.where(values < beats[0], (values - beats[0]) / (beats[1] - beats[0]), coordinate)
            return np.where(values > beats[-1], len(beats) - 1 + (values - beats[-1]) / (beats[-1] - beats[-2]), coordinate)

        origin = args.first_downbeat if args.first_downbeat is not None else float(beats[0])
        origin_beat = float(beat_coordinate(np.array([origin]))[0])
        positions = (beat_coordinate(times) - origin_beat) / beats_per_bar + 1
        grid_source = "tracked_beat_interpolation_with_edge_extrapolation"
        origin_source = "provided" if args.first_downbeat is not None else "assumed_first_tracked_beat"
    grouping_source = "provided" if args.beats_per_bar is not None else "assumed"
    return positions, {
        "x_axis": "bar_number", "y_axis": "log_pitch_note_names", "tuning_reference": "12-TET, A4=440Hz",
        "beats_per_bar": beats_per_bar, "grouping_source": grouping_source,
        "bar_1_downbeat_seconds": origin, "origin_source": origin_source,
        "grid_source": grid_source, "provided_plot_bpm": args.plot_bpm,
        "has_assumptions": grouping_source == "assumed" or origin_source != "provided",
    }


def analyze(source, metadata, args):
    try:
        import numpy as np
        import librosa
    except ImportError as error:
        raise ValueError("Missing analysis dependencies. Install scripts/requirements-basic.txt "
                         "in a separate environment after reviewing its footprint.") from error

    output = args.output.resolve()
    if output.exists():
        raise ValueError("Output directory already exists; choose a new directory.")
    if args.spectrogram:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
            from matplotlib.ticker import LogLocator, MaxNLocator, NullFormatter
            import librosa.display
        except ImportError as error:
            raise ValueError("Plotting requires matplotlib; see scripts/requirements-plot.txt.") from error

    audio = decode_audio(source, args.start, args.duration, np)
    actual_duration = len(audio) / SAMPLE_RATE
    rms = float(np.sqrt(np.mean(audio.astype(np.float64) ** 2)))
    warnings = [
        "Global tempo may be half/double the perceived pulse; beats do not establish meter or downbeats.",
        "Key candidates compare only major/minor profiles; other modes and key changes are not resolved.",
        "Profile correlations are not calibrated confidence scores.",
        "Onsets have no instrument labels and are not a percussion transcription.",
    ]
    tempo = None
    beat_times = np.array([], dtype=float)
    onset_times = np.array([], dtype=float)
    candidates = []
    power = np.abs(librosa.stft(audio, n_fft=N_FFT, hop_length=HOP_LENGTH)) ** 2
    times = librosa.frames_to_time(np.arange(power.shape[1]), sr=SAMPLE_RATE, hop_length=HOP_LENGTH)
    chroma = np.zeros((12, power.shape[1]), dtype=np.float32)
    envelope = np.zeros(power.shape[1], dtype=np.float32)
    if rms > 1e-6:
        harmonic, _ = librosa.decompose.hpss(np.sqrt(power))
        chroma = librosa.feature.chroma_stft(
            S=harmonic ** 2, sr=SAMPLE_RATE, n_fft=N_FFT, hop_length=HOP_LENGTH, norm=None,
        )
        candidates = key_candidates(chroma, np)
        envelope = librosa.onset.onset_strength(y=audio, sr=SAMPLE_RATE, hop_length=HOP_LENGTH)
        onset_times = librosa.onset.onset_detect(
            onset_envelope=envelope, sr=SAMPLE_RATE, hop_length=HOP_LENGTH, units="time",
        )
        if len(onset_times) >= 3:
            bpm, beat_times = librosa.beat.beat_track(
                onset_envelope=envelope, sr=SAMPLE_RATE, hop_length=HOP_LENGTH, units="time",
            )
            value = float(np.asarray(bpm).reshape(-1)[0])
            if value > 0 and len(beat_times) >= 3:
                tempo = value
            else:
                beat_times = np.array([], dtype=float)
        if not candidates or candidates[0]["profile_correlation"] < 0.5:
            warnings.append("Weak tonal profile match; no reliable key conclusion is established.")
        elif candidates[0]["profile_correlation"] - candidates[1]["profile_correlation"] < 0.05:
            warnings.append("The leading key candidates are close; resolve by listening or stronger evidence.")
    else:
        warnings.append("The region is silent or near-silent; no tempo or key estimate was produced.")

    # Centered frames at or after EOF are omitted. All stored times use the original file origin.
    frame_mask = times < actual_duration
    beat_times = np.asarray(beat_times)
    beat_times = beat_times[beat_times < actual_duration] + args.start
    onset_times = onset_times[onset_times < actual_duration] + args.start
    absolute_times = times[frame_mask] + args.start
    visualization = None
    if args.spectrogram:
        bars, visualization = bar_coordinates(absolute_times, beat_times, args, np)
        if visualization["has_assumptions"]:
            warnings.append("Plot bar grouping and/or bar-1 origin are assumed; see visualization metadata. "
                            "These are relative bars, not detected meter or downbeats.")
    report = {
        "schema_version": 1,
        "input": {"path": str(source), "probe": metadata},
        "region": {"start_seconds": args.start, "requested_duration_seconds": args.duration,
                   "analyzed_duration_seconds": actual_duration,
                   "time_origin": "seconds from the original file start"},
        "method": {"sample_rate_hz": SAMPLE_RATE, "channels": 1, "n_fft": N_FFT,
                   "hop_length": HOP_LENGTH, "rms": rms, "tempo": "librosa.beat.beat_track",
                   "key": "harmonic STFT chroma / Krumhansl-Kessler profile Pearson correlation",
                   "versions": {name: importlib.metadata.version(name) for name in ("librosa", "numpy", "scipy")}},
        "rhythm": {"status": "estimate" if tempo else "insufficient_evidence",
                   "bpm": tempo, "metrical_alternatives_bpm": [tempo / 2, tempo * 2] if tempo else [],
                   "beat_times_seconds": beat_times.tolist(),
                   "onset_times_seconds": onset_times.tolist(), "meter": None},
        "tonality": {"status": "candidates_only" if candidates else "insufficient_evidence",
                     "candidates": candidates},
        "warnings": warnings,
        "visualization": visualization,
        "artifacts": {"features": "features.npz", "spectrogram": "spectrogram.png" if args.spectrogram else None},
    }
    # Fail rather than overwrite outputs or touch the original audio.
    output.mkdir(parents=True, exist_ok=False)
    features = {"frame_times_seconds": absolute_times,
                "chroma_power": chroma[:, frame_mask],
                "onset_strength": envelope[:len(times)][frame_mask]}
    if args.spectrogram:
        features["frame_bar_positions"] = bars
        features["spectrogram_power"] = power[:, frame_mask]
        features["frequency_hz"] = librosa.fft_frequencies(sr=SAMPLE_RATE, n_fft=N_FFT)
        fig, ax = plt.subplots(figsize=(12, 5), constrained_layout=True)
        image = librosa.display.specshow(
            librosa.power_to_db(power[:, frame_mask], ref=np.max), x_coords=bars,
            sr=SAMPLE_RATE, hop_length=HOP_LENGTH, n_fft=N_FFT,
            y_axis="fft_note", x_axis=None, auto_aspect=False, unicode=False,
            ax=ax, cmap="magma", vmin=-80, vmax=0,
        )
        status = "assumed grouping/origin" if visualization["has_assumptions"] else "provided grouping/origin"
        # specshow's fft_note uses a linear region at low frequencies. Use a
        # true log2 scale throughout so every displayed octave has equal height.
        ax.set_yscale("log", base=2)
        octave_midi = np.arange(24, 121, 12)
        ax.set_yticks(librosa.midi_to_hz(octave_midi), labels=librosa.midi_to_note(octave_midi, unicode=False))
        ax.yaxis.set_minor_locator(LogLocator(base=2, subs=2 ** (np.arange(1, 12) / 12)))
        ax.yaxis.set_minor_formatter(NullFormatter())
        ax.set(xlabel="Bar", ylabel="Pitch",
               title=f"Music spectrogram | {visualization['beats_per_bar']} beats per bar | {status}",
               ylim=(librosa.note_to_hz("C1"), SAMPLE_RATE / 2), xlim=(bars[0], bars[-1]))
        ax.xaxis.set_major_locator(MaxNLocator(nbins=12, integer=True))
        ax.grid(axis="y", which="major", alpha=0.15)
        fig.colorbar(image, ax=ax, label="dB relative to maximum")
        fig.savefig(output / "spectrogram.png", dpi=150)
        plt.close(fig)
    np.savez_compressed(output / "features.npz", **features)
    (output / "analysis.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False) + "\n", encoding="utf-8")
    return {"report": str(output / "analysis.json"), "bpm_estimate": tempo,
            "key_candidates": candidates, "warnings": warnings}


def nonnegative(value):
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise argparse.ArgumentTypeError("must be finite and nonnegative")
    return number


def positive(value):
    number = nonnegative(value)
    if number == 0:
        raise argparse.ArgumentTypeError("must be positive")
    return number


def positive_integer(value):
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return number


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    probe = subparsers.add_parser("probe", help="Read metadata using ffprobe (no Python DSP dependencies)")
    probe.add_argument("audio", type=Path)
    analysis = subparsers.add_parser("analyze", help="Estimate tempo/key; save timed features, optionally a spectrogram")
    analysis.add_argument("audio", type=Path)
    analysis.add_argument("--output", type=Path, required=True, help="New output directory; existing directories are refused")
    analysis.add_argument("--start", type=nonnegative, default=0.0, help="Crop start in original-file seconds")
    analysis.add_argument("--duration", type=positive, help="Crop duration in seconds; default: to EOF")
    analysis.add_argument("--spectrogram", action="store_true", help="Plot note names on a log pitch axis against bars (matplotlib required)")
    analysis.add_argument("--beats-per-bar", type=positive_integer, help="Tracked pulse beats per bar for plotting; default: 4, explicitly labeled assumed")
    analysis.add_argument("--first-downbeat", type=nonnegative, help="Bar-1 downbeat in original-file seconds; default: first tracked beat, labeled assumed")
    analysis.add_argument("--plot-bpm", type=positive, help="Use a provided constant BPM for the plot grid, instead of tracked beats; does not override the measured BPM")
    args = parser.parse_args()
    try:
        source = args.audio.resolve(strict=True)
        if not source.is_file():
            raise ValueError("Audio input must be a local file.")
        metadata = probe_audio(source)
        result = metadata if args.command == "probe" else analyze(source, metadata, args)
        print(json.dumps(result, ensure_ascii=False, allow_nan=False))
    except (OSError, ValueError, RuntimeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
