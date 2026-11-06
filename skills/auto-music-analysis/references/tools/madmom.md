# madmom downbeat/bar tracking

Status: 0.16.1 documentation reviewed 2026-11-06; no local installation or model validation. Candidate for constrained [meter analysis](../tasks/meter.md).

The documented `RNNDownBeatProcessor` produces beat/downbeat activations at 100 fps. `DBNDownBeatTrackingProcessor` accepts allowed beats-per-bar values and returns event time plus position within the bar, counted from 1. An upstream example is:

```python
from madmom.features.downbeats import RNNDownBeatProcessor, DBNDownBeatTrackingProcessor
activations = RNNDownBeatProcessor()(audio_path)
decoder = DBNDownBeatTrackingProcessor(beats_per_bar=[3, 4], fps=100)
beat_positions = decoder(activations)
```

This example restricts candidate bar lengths; it does not establish 3/4 or 4/4 as ground truth, handle all compound/odd meters, or prove the chosen processor permits within-piece meter changes. Inspect the installed implementation's transition model before using it for that purpose. Other bar-tracking processors have distinct interfaces; do not interchange them.

Record beat-count constraints, tempo bounds, fps, transition parameters, and model version. A strong preference for constant tempo or restrictive meter states can erase real transitions. Compare unconstrained events and section-local evidence rather than forcing a single global result.

Dependencies, native extensions, pretrained models, and Python/NumPy compatibility require an isolated environment and [setup consent](../tasks/setup.md). Do not assume compatibility with the basic DSP environment or silently install an unreleased fork.

Sources: [downbeat API](https://madmom.readthedocs.io/en/v0.16.1/modules/features/downbeats.html), [upstream implementation](https://github.com/CPJKU/madmom/blob/main/madmom/features/downbeats.py).
