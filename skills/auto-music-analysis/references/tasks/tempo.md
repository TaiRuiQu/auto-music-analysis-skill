# Build a local tempo map

Deliver local beat times and tempo regions with an explicit pulse unit where known. Keep actual speed change, half/double counting, subdivision change, and uncertain tracking as separate interpretations.

The [local DSP helper](../tools/local-dsp.md) returns one global BPM. It does not detect tempo-change boundaries. For variable-tempo questions or bar-aligned harmony, use [librosa local rhythm functions](../tools/librosa-rhythm.md) or evaluate [Beat This!](../tools/beat-this.md); an authorized [hosted beat service](../tools/music-ai.md) is another candidate.

Compare adjacent windows and retain alternative pulse levels. A switch between autocorrelation peaks at 60, 90, 120, or 180 does not by itself prove a musical tempo change. Window centers/edges are not exact change timestamps. Inspect the transition with overlapping context and check event continuity, missed/doubled beats, and frequency-band disagreement.

For beat times b[i], `60 / (b[i+1] - b[i])` gives interval BPM relative to the tracked pulse, not an independently identified quarter note. Omit invalid or duplicate intervals. Summarize locally with the smoothing window recorded, preserve raw events, and do not smooth across a supported discontinuity. Local detectors may require different assumptions across passages; retain uncertainty instead of forcing one global count.

Export regions with start/end seconds, BPM candidate(s), pulse unit or unknown, method, and review status. For a transition record its estimated time range and before/after interpretation. Do not convert a local spectral peak into a confirmed metronome marking without beat-level support.

Include a preferred [time-signature candidate](meter-classification.md) with a rhythm report. Follow [meter mapping](meter.md) for bars or suspected changes. Use [review](review.md) to refine transitions; the present skill contains no bundled local-tempo or meter CLI, so classify heuristically when an external backend is unavailable and make assumptions explicit.
