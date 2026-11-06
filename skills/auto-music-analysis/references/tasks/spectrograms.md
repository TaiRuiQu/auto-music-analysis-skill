# Plot musical spectrograms

Use the [local DSP helper](../tools/local-dsp.md) with `--spectrogram`. The plot uses note names on a true logarithmic pitch axis (12-TET, A4=440 Hz) and bar numbers horizontally. Spectral energy includes overtones; it is not recognized note events.

`--beats-per-bar` counts tracked pulses, not a full signature. Four quarter-note pulses can describe a 4/4 grouping; two dotted-quarter pulses can describe 6/8 when that is the tracked pulse. `--first-downbeat` is bar 1 in original-file seconds, including for crops. Specify these from actual evidence or keep their assumed status visible.

Without those inputs the helper assumes four pulses and the first tracked beat as bar 1. Its beat interpolation and edge extrapolation do not detect meter or a true first downbeat. `--plot-bpm` supplies a constant plotting grid and does not replace measured tempo. A silent/no-grid case needs an explicitly supplied known grid or no bar plot.

For varying meter, make separate section plots with the candidate grouping/origin or use an explicit piecewise map outside the current helper. A provisional map is allowed; label estimated/default sections and transition uncertainty rather than implying a confirmed alignment. Follow [classification](meter-classification.md), [tempo](tempo.md), and [meter mapping](meter.md) when choosing the grid. Save numeric features and assumptions with the image.
