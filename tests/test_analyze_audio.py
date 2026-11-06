"""Exercise the public CLI with known signals, without network access or models."""

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import wave

import numpy as np


SCRIPT = Path(__file__).resolve().parents[1] / "skills/auto-music-analysis/scripts/analyze_audio.py"
SR = 22050


class AudioAnalysisTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def audio_file(self, name, samples):
        path = self.root / name
        with wave.open(str(path), "wb") as audio:
            audio.setnchannels(1)
            audio.setsampwidth(2)
            audio.setframerate(SR)
            audio.writeframes((np.clip(samples, -1, 1) * 32767).astype("<i2").tobytes())
        return path

    def run_cli(self, *args, success=True):
        result = subprocess.run([sys.executable, "-X", "utf8", str(SCRIPT), *map(str, args)],
                                capture_output=True, text=True, encoding="utf-8")
        if success:
            self.assertEqual(result.returncode, 0, result.stderr)
            return json.loads(result.stdout)
        self.assertNotEqual(result.returncode, 0)
        return result

    def test_silence_does_not_invent_tempo_or_key(self):
        audio = self.audio_file("静音.wav", np.zeros(SR * 2))
        output = self.root / "silence"
        self.run_cli("analyze", audio, "--output", output)
        report = json.loads((output / "analysis.json").read_text(encoding="utf-8"))
        self.assertIsNone(report["rhythm"]["bpm"])
        self.assertEqual(report["rhythm"]["onset_times_seconds"], [])
        self.assertEqual(report["tonality"]["candidates"], [])
        plot_output = self.root / "silent-plot"
        failure = self.run_cli("analyze", audio, "--spectrogram", "--output", plot_output, success=False)
        self.assertIn("No usable beat grid", failure.stderr)
        self.assertFalse(plot_output.exists())

    def test_known_click_tempo_crop_alignment_and_source_preservation(self):
        samples = np.zeros(SR * 16)
        click = np.hanning(441) * np.sin(2 * np.pi * 2000 * np.arange(441) / SR)
        for position in np.arange(0.25, 16, 0.5):
            start = round(position * SR)
            samples[start:start + len(click)] += click
        audio = self.audio_file("节拍 sample.wav", samples)
        original = hashlib.sha256(audio.read_bytes()).digest()
        output = self.root / "crop"
        self.run_cli("analyze", audio, "--start", "2", "--duration", "12", "--output", output,
                     "--spectrogram", "--plot-bpm", "120", "--beats-per-bar", "4", "--first-downbeat", "0")
        report = json.loads((output / "analysis.json").read_text(encoding="utf-8"))
        self.assertAlmostEqual(report["rhythm"]["bpm"], 120, delta=3)
        self.assertGreater(len(report["rhythm"]["beat_times_seconds"]), 12)
        for event in report["rhythm"]["onset_times_seconds"]:
            self.assertGreaterEqual(event, 2)
            self.assertLess(event, 14)
            # Click maxima occur 0.01s after known onsets; spectral flux can lag slightly.
            distance = abs(((event - 0.25 + 0.25) % 0.5) - 0.25)
            self.assertLess(distance, 0.1)
        with np.load(output / "features.npz", allow_pickle=False) as features:
            self.assertEqual(features["chroma_power"].shape[1], len(features["frame_times_seconds"]))
            self.assertAlmostEqual(float(features["frame_times_seconds"][0]), 2)
            # At 120 BPM in four-beat bars, file time 2s is the start of bar 2.
            self.assertAlmostEqual(float(features["frame_bar_positions"][0]), 2)
            self.assertTrue(np.all(np.diff(features["frame_bar_positions"]) > 0))
        self.assertFalse(report["visualization"]["has_assumptions"])
        self.assertEqual(hashlib.sha256(audio.read_bytes()).digest(), original)
        self.run_cli("analyze", audio, "--output", output, success=False)
        self.assertEqual(hashlib.sha256(audio.read_bytes()).digest(), original)

    def test_probe_and_invalid_regions(self):
        audio = self.audio_file("probe.wav", np.zeros(SR))
        probe = self.run_cli("probe", audio)
        self.assertEqual(probe["streams"][0]["sample_rate"], str(SR))
        for options in [("--start", "2"), ("--start", "nan"), ("--duration", "0")]:
            output = self.root / "invalid"
            self.run_cli("analyze", audio, *options, "--output", output, success=False)
            self.assertFalse(output.exists())

    def test_tonal_progression_and_spectrogram(self):
        # I-vi-IV-V-I in C major, with simple harmonics and a smooth note envelope.
        progression = [(48, 52, 55), (45, 48, 52), (41, 45, 48), (43, 47, 50), (48, 52, 55)]
        time = np.arange(SR * 2) / SR
        envelope = np.minimum(time / 0.05, 1) * np.minimum((2 - time) / 0.05, 1)
        chords = []
        for chord in progression:
            samples = np.zeros(len(time))
            for pitch in chord:
                frequency = 440 * 2 ** ((pitch - 69) / 12)
                samples += np.sin(2 * np.pi * frequency * time)
                samples += 0.3 * np.sin(4 * np.pi * frequency * time)
            chords.append(samples * envelope / 5)
        audio = self.audio_file("和声.wav", np.concatenate(chords))
        output = self.root / "tonal"
        self.run_cli("analyze", audio, "--spectrogram", "--output", output)
        report = json.loads((output / "analysis.json").read_text(encoding="utf-8"))
        leading = report["tonality"]["candidates"][0]
        self.assertEqual((leading["tonic"], leading["mode"]), ("C", "major"))
        self.assertTrue(report["visualization"]["has_assumptions"])
        self.assertTrue((output / "spectrogram.png").read_bytes().startswith(b"\x89PNG\r\n\x1a\n"))
        with np.load(output / "features.npz", allow_pickle=False) as features:
            self.assertEqual(features["spectrogram_power"].shape,
                             (len(features["frequency_hz"]), len(features["frame_times_seconds"])))
            self.assertTrue(np.isfinite(features["spectrogram_power"]).all())

    def test_corrupt_media_fails_without_outputs(self):
        audio = self.root / "broken.mp3"
        audio.write_bytes(b"not an audio file")
        output = self.root / "invalid"
        self.run_cli("analyze", audio, "--output", output, success=False)
        self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
