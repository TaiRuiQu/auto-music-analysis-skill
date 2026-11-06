# Beat This!

Status: official repository/interface reviewed 2026-11-06; not installed, run, or benchmarked here. Candidate for [tempo](../tasks/tempo.md) and [meter evidence](../tasks/meter.md).

Produces beat and downbeat timestamps; optional framewise outputs are available. Prefer evaluating its default non-DBN path for changing passages before adding constraints. It does not directly output a notated time-signature change map.

Inference can automatically download missing checkpoints, even when a supplied path is mistyped. Follow [setup](../tasks/setup.md) before model loading. Upstream lists main checkpoints at about 78 MB each and small checkpoints at about 8.1 MB; these exclude PyTorch, audio dependencies, cache overhead, and memory. CPU is supported; GPU availability affects runtime. Measure the selected setup rather than promising real-time speed.

After approved setup, use a verified existing local checkpoint to avoid implicit downloads:

```python
from pathlib import Path
from beat_this.inference import File2Beats

checkpoint = Path(approved_local_checkpoint)
if not checkpoint.is_file():
    raise FileNotFoundError(checkpoint)
tracker = File2Beats(checkpoint_path=str(checkpoint), device="cpu", dbn=False)
beats, downbeats = tracker(audio_path)
```

Confirm return ordering and units against the installed version. Preserve raw events and checkpoint/postprocessor identity. Derive local interval BPM relative to the model pulse; count pulses between downbeats as candidates, then follow the [meter task](../tasks/meter.md) for notation and changes. Optional DBN postprocessing adds [madmom](madmom.md) dependencies and assumptions.

Sources: [repository and inference examples](https://github.com/CPJKU/beat_this), [checkpoint-loading implementation](https://github.com/CPJKU/beat_this/blob/main/beat_this/inference.py), [paper](https://arxiv.org/abs/2407.21658).
