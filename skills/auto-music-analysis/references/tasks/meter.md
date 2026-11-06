# Map meter and changes

Start with a preferred [time-signature candidate](meter-classification.md), then deliver candidate bar boundaries, grouping, and transition ranges. The user prefers a usable provisional classification to withholding a meter label. A beat tracker, a user-supplied grouping, and a heuristic notated signature are different evidence; keep the basis visible.

Obtain local beats and downbeats with [Beat This!](../tools/beat-this.md), a suitable [madmom](../tools/madmom.md) decoder, or an authorized [Klangio](../tools/klangio.md) analysis. Use [tempo mapping](tempo.md) for changing speeds. The bundled helper detects neither downbeats nor meter.

Count tracked beats between consecutive downbeats, checking missed/doubled beats where feasible. Preserve that count as `pulses_per_bar`. It does not determine the denominator: two pulses could be half notes in 2/2 or dotted quarters in 6/8. Choose a plausible denominator using accents, subdivisions, phrasing, and beat unit; mark unsupported choices assumed rather than leaving the classification empty.

When a decoder accepts `[3, 4]`, those are allowed model states, not proof that the recording uses only 3/4 and 4/4. Record all constraints. Do not force every segment through one fixed meter or use the default four-pulse plotting grid to diagnose a change. Check whether the selected decoder actually allows within-recording meter transitions; otherwise compare sections and keep transition inference external.

For a suspected change, propose before/after signatures and an approximate boundary with candidate status. When a review interface is available, inspect several bars on both sides with [Sonic Visualiser](../tools/sonic-visualiser.md) or another tool. Compare accents and, when available, a trusted score; log corrections. If listening or a score is unavailable, retain the provisional signatures and disclose that basis. A different winning window alone is not a confirmed transition, but can motivate a candidate change for the user to adjust.

For each proposed section record start/end seconds, candidate numerator/denominator, tracked or assumed beat unit, pulses per bar where available, first downbeat if known, method, alternatives, and status. Leave unobserved event positions null; record the signature as a hypothesis. A sequence of downbeats can support changing bar lengths without proving every notated signature.

Reviewed, estimated, or explicitly defaulted regions may drive bar-based [plots](spectrograms.md) and [score exports](score-export.md) with their status visible. Keep a revisable map and original seconds so a user correction can update the grid.
