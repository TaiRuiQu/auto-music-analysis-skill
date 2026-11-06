# Review and deliver analysis

Check original-file coverage, monotonically increasing timestamps, crop/stem alignment, gaps/overlaps, and actual file readability. Keep the source unchanged and raw backend output alongside any normalized table.

Prioritize passages where methods disagree, bass changes, rhythm transitions, quiet intros/fades, and abrupt label changes. Use [Sonic Visualiser](../tools/sonic-visualiser.md) or another available interface for playback/annotation when possible. State exactly what was reviewed. A plot, a file-open action, or plausible theory does not mean audio was heard or the transcription validated.

Keep measured outputs separate from interpretation. Template margins, profile correlation, decoder activations, and cross-method agreement are different scales; preserve their meanings and do not rename them confidence probabilities. With only related feature pipelines, report agreement as a diagnostic. For weak harmony, retain alternatives or unknown spans as appropriate. For meter, prioritize a usable [preferred candidate](meter-classification.md), explicitly marking weak evidence or a conventional default rather than withholding the classification.

For chord tables, preserve raw label, normalized label if any, start/end seconds, method/version, alternatives, and review status. Add chord vocabulary and coverage. For rhythm, retain raw beats/downbeats, pulse unit, preferred time-signature candidates, alternatives, region status, and change-time uncertainty. Unknown measured event fields can be null; the proposed signature can still be supplied as a labeled hypothesis. Put assumptions in the data as well as the prose.

Summarize findings in the user's language, with limitations and links to checked artifacts. State when a result is a provisional automatic estimate. Do not promise listening validation, a full transcription, arbitrary chord extensions, or correct bar lines beyond the actual evidence. If a new backend is needed, use [tool selection](tool-selection.md) and [setup](setup.md), without claiming the unexecuted integration exists.
