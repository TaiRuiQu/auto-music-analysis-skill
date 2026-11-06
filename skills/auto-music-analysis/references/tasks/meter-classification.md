# Classify time signatures with a usable first candidate

The user prioritizes having a candidate they can adjust over waiting for a verified answer. For chord/rhythm analysis, deliver a preferred time signature even when evidence is incomplete. Provide a short alternative where useful. State whether the choice is model-derived, heuristic, an explicit default, or reviewed; uncertainty should qualify the candidate rather than remove it.

## Get evidence without blocking the first answer

Use available beats/downbeats, accents, subdivisions, phrase lengths, and repeated harmonic boundaries. [Beat This!](../tools/beat-this.md) supplies events; [madmom](../tools/madmom.md) can compare allowed groupings; [Klangio](../tools/klangio.md) advertises meter output. [librosa rhythm features](../tools/librosa-rhythm.md) offer a no-new-model fallback. Inspect only tools needed for this recording; absent models or an unavailable listening interface do not prevent a heuristic candidate.

If the beat unit is unknown, choose a plausible conventional one and mark it assumed. Do not confuse this musical hypothesis with a directly measured denominator. Record pulse-relative BPM and notated beat unit so the user can revise the count without losing original timestamps.

## Practical candidate rules

These are working hypotheses, not exhaustive classification rules or measured likelihoods. Use the pattern that best fits the available passage; do not force unusual music into this list.

| Observed or tentatively inferred organization | First candidate | Useful alternative / adjustment |
| --- | --- | --- |
| Four main pulses with mainly binary subdivision | 4/4 | 2/2 if a broader two-beat count fits phrasing |
| Three main pulses with binary subdivision | 3/4 | 6/8 if the apparent pulses are really three pairs of subdivisions and accents favor two groups of three |
| Two main pulses, each divided into three | 6/8 | 3/4 if accents favor three groups of two eighth notes |
| Two main pulses, binary subdivision | 2/4 | 4/4 when the pattern is half a bar; 2/2 for a broader beat unit |
| Three main pulses, each divided into three | 9/8 | 3/4 with triplets if that notation better fits the surrounding music |
| Four main pulses, each divided into three | 12/8 | 4/4 with triplets if that fits the surrounding notation |
| Repeating unequal groups such as 2+3 or 3+2 | 5/8 with the grouping stated | 5/4 if the grouped units function as quarter notes |
| Repeating unequal groups such as 2+2+3 | 7/8 with the grouping stated | 7/4 if the grouped units function as quarter notes |

For 3/4 versus 6/8, compare `2+2+2` versus `3+3` eighth-note accents, rather than just counting six events. Do not equate every triplet accompaniment with compound meter. Treat a model's allowed beat counts as constraints rather than known signatures.

When evidence is too weak to distinguish candidates, output **4/4 as an explicit working default**, with `status: assumed_default`, and name the unresolved alternative if there is one. This is a useful starting point, not a claim that four beats were detected. If the source is missing, unreadable, silent, or not meaningfully metrical, state that; a conventional editing default may still be offered, clearly separated from identification.

## Output the candidate so it is easy to change

For each useful region provide start/end seconds, `time_signature_candidate`, `status` (`estimated`, `assumed_default`, or `reviewed`), `basis` (model/heuristic/default), tracked or assumed beat unit, subdivision grouping when useful, and at most a few alternatives. Keep unknown event times/BPM null rather than inventing them. Do not assign numerical confidence unless a tool actually supplies a meaningful scale.

Explain briefly how to count the chosen candidate, for example “6/8, counted as two dotted-quarter beats, each split into three.” Flag candidate transitions and let the user adjust the signature, first downbeat, pulse level, or boundary. Use [meter mapping](meter.md) to refine boundaries and [review](review.md) to improve the candidate; listening or a trusted score is not a prerequisite for proposing it.

For plots, scores, and quantized chords, an inferred/default grid is allowed when its status is visible in both the artifact and report. Preserve the original seconds so a changed meter does not require rerunning audio recognition. Follow [spectrograms](spectrograms.md) and [score assembly](score-export.md) for export-specific handling.
