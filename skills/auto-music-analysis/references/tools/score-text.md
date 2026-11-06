# Score Text: program, CLI, and plain-text notation

## Purpose and scope

The user's [score-text npm package](https://www.npmjs.com/package/score-text) is a multi-part text score CLI for agents. The model manually authors every musical event in YAML; the program validates musical structure, builds the timeline, engraves the score, and exports files. Use it for numbered notation, guitar accompaniment, piano, drums, and small ensembles. Follow the mandatory [manual score authoring workflow](../tasks/score-export.md); analysis outputs are evidence for the agent's decisions, not events to import or generate with a script.

Input is UTF-8 `.score.yaml` with notation `version: 1`. Outputs are PDF, SVG, PNG, offline HTML, MIDI, MusicXML, and normalized JSON. The program does not call a model API or infer notes from audio or images. Original composition can start directly; for recordings, first reconcile notes, beats, meter, and uncertainty using [score assembly](../tasks/score-export.md).

This chapter targets the published `score-text@0.1.0` interface. The skill distributes instructions and an example, without bundling the program, fonts, or Node dependencies. Check availability on the current host; maintainer execution records live in the repository's `docs/tool-integration.md`.

## Setup and tool interface

Requires Node.js 20+. Check `node --version` and `score-text --version` first. Reuse an existing installation or built source checkout with `node /path/to/score-text/dist/cli.js` when available. Fonts are included in the package; no browser, LilyPond, model weights, or model credentials are required. Installation still downloads npm packages and dependencies; follow [setup guidance](../tasks/setup.md).

If installation is needed, choose a pinned global install or use the npx form for each command:

```sh
npm install -g score-text@0.1.0
score-text --version
# Alternatively, run without a global install; first use downloads to npm's cache.
npx --yes score-text@0.1.0 guide
```

The remaining commands assume an available `score-text` executable:

```sh
score-text guide
score-text schema
score-text init song.score.yaml --template ensemble
# Edit song.score.yaml to match the user's request.
score-text validate song.score.yaml --json
score-text inspect song.score.yaml --json
score-text render song.score.yaml -o preview.png --json
# Inspect the preview, then export the requested formats.
score-text render song.score.yaml -o song.pdf --json
score-text render song.score.yaml -o song.mid --json
score-text render song.score.yaml -o song.musicxml --json
```

`init` accepts `reference` (default), `strum`, or `ensemble` templates and refuses to overwrite existing files by default. `guide` returns the packaged notation guide; `schema` returns JSON Schema. Use those outputs as the field authority for the installed version.

`validate` checks semantics and page capacity. `--syntax-only` skips layout checks, so it cannot establish that final pages fit. `render` infers format from the output extension; `--format midi` overrides inference. Other extensions include `.svg`, `.html`, and `.json`. An input argument of `-` reads stdin. In PowerShell, for example: `Get-Content -Raw -Encoding utf8 song.score.yaml | score-text validate - --json`.

Exit code `0` means success and `1` means failure. With `--json`, successful `validate` / `render` results go to stdout with `ok: true`; failures go to stderr with `ok: false` and `diagnostics`. Each diagnostic has `code`, `path`, and `message`; `BAR_DURATION`, for example, identifies a voice with an incorrect duration. Repair the target and revalidate, preserving requested parts and lyrics. Successful `inspect` directly returns the normalized score and event `start` / `ticks` fields, without an `ok` wrapper.

## Score structure and runnable examples

A minimal score requires `version`, `title`, `tracks`, and `bars`. This is a complete original one-bar score:

```yaml
version: 1
title: First Light Motif
key: C
meter: 4/4
tempo: 96
tracks:
  vocal: { type: numbered, name: Vocal, lyrics: true }
bars:
  - chords: C
    vocal:
      notes: "1/4 2/8 3/8 5/4 3/4"
      lyrics: [Soft, light, falls, on, me]
```

The [complete arrangement example](../../assets/score-text/ensemble.score.yaml) combines voice, guitar, piano grand staff, and two drum voices across 4/4, 6/8, and 3/4 bars. Copy it to the working directory before editing.

`tracks` declares parts; each `bars` item is one measure and uses track IDs to assign events. Track order controls vertical layout. IDs begin with an English letter and contain letters, digits, underscores, or hyphens; avoid control names such as `meter` and `tempo`.

| Track type | Purpose and event notation |
| --- | --- |
| `numbered` | Movable-do numbered notation, such as `3/8`; lyrics enabled by default |
| `staff` | Absolute pitches such as `C#4/4`; optional `clef: bass` |
| `tab` | Six-string guitar; `mode: frets`, `cross`, or `strum` |
| `piano` | Grand staff using `right` / `left` or voices with explicit `staff` |
| `drums` | Drum names such as `kick/4` on a percussion staff |

Optional top-level fields include `subtitle`, `artist`, `composer`, `lyricist`, `arranger`, `note`, `capo`, `fingering`, `layout`, `patterns`, and `chordShapes`. Defaults are C major, 4/4, and quarter note = 100 BPM; explicitly write the user's intended musical parameters. Unknown fields and duplicate YAML keys are errors.

## Pitches, durations, and events

Compact notation is `event/duration`, with space-separated events and an explicit duration on each event. `/4` means a quarter note; in 6/8 it occupies two eighth-note counts. Denominators are `1 2 4 8 16 32 64`, optionally followed by one or two dots.

| Notation | Meaning |
| --- | --- |
| `3/8` | Numbered scale degree 3, eighth note |
| `6v/8`, `1^/4.` | Degree 6 one octave down; degree 1 one octave up, dotted quarter |
| `#4/8`, `b7/8`, `n4/8` | Raise a scale degree, lower it, or restore its unaltered in-key pitch |
| `0/4` or `r/4` | Quarter rest |
| `C4/4`, `F#5/8` | Absolute pitches |
| `[1,3,5]/4`, `[C4,E4,G4]/2` | Simultaneous pitches sharing one duration |
| `3/8~ 3/8` | Tie between identical pitches; both events retain their durations |
| `1/8*3:2` | One eighth-note triplet event; three such events total one quarter note |

Numbered notation is movable-do: the tonic of Am is `6`, with `1` taken from its relative major, C. Unmarked `1` uses octave 4 of the corresponding major tonic, such as C4 or E4. Up to three `^` or three `v` markers are allowed; do not mix them. Accidentals apply only to their explicit event; the next unmarked degree returns to its in-key pitch. Staff pitch names always represent absolute pitches.

Objects support lyrics, dynamics, and connections. Arrays may mix objects and compact strings. This voice-content fragment fills 4/4:

```yaml
notes:
  - { pitch: 3, duration: 8, lyric: Soft }
  - { pitch: 5, duration: "4.", lyric: light, tie: true, dynamic: mf }
  - { pitch: 5, duration: 2, lyric: _ }
```

Each object requires `duration` and exactly one event content field: `pitch`, `pitches`, `rest: true`, `strings`, `drums`, or `strum`. Examples: `{strings: {"5": 3, "2": 1}, duration: 8}` and `{drums: [kick, hat], duration: 8}`. Quote dotted and tuplet durations, such as `"4."` and `"8*3:2"`.

Modifiers are `lyric`, `tie: true`, `slur: start|stop`, `dynamic`, and `accent: true`. Dynamics support `ppp pp p mp mf f ff fff sfz`. Ties require identical pitches or chords and may cross bars. Slurs may cross bars and systems; nesting within one voice is unsupported.

## Bars, lyrics, and independent voices

Every explicit voice must independently fill its bar. In quarter-note units, bar length is `numerator * 4 / denominator`: 4/4 totals 4; 6/8 and 3/4 each total 3 but group differently. Do not sum durations across parallel voices. An entirely omitted track becomes a full-bar rest; an explicitly written voice is not padded automatically.

Prefer lyric arrays with one item per event, including one item per simultaneous chord event. Use `_` for rests and tied continuations. Separate syllables explicitly, including when writing Chinese lyrics; English syllables may use trailing hyphens such as `Sing-`, `ing`. `~` extends the previous lyric within the same bar; use a tie plus `_` across bars. Do not align lyrics with text-column spacing. Outer `lyrics` overrides event-level `lyric` values.

These are encoding rules, not an alignment procedure. Follow [manual lyric verification and placement](../tasks/score-export.md#manually-verify-and-place-lyrics): verify every character/syllable and its event correspondence, then explicitly write each item. Do not invoke lyric-alignment models, forced alignment, or scripts to populate `lyrics`/`lyric`, or distribute text by counts or order. Choose `_` and `~` only after reviewing the actual rest/continuation; a cross-bar tie is valid only when the pitch is sustained unchanged. Do not change pitches or introduce ties merely to carry a lyric. If the notation format cannot express a verified text setting, preserve that mapping in the review table and disclose the limitation.

Use a `voices` array with stable, unique voice IDs across bars. This is the `vocal` content of a 4/4 bar:

```yaml
vocal:
  voices:
    - { id: lead, notes: "1/4 2/4 3/2", lyrics: [We, all, sing] }
    - { id: harmony, notes: "3/4 4/4 5/2", lyrics: [We, all, sing] }
```

## Guitar, chords, piano, and drums

Guitar string 1 is the high, thin string; string 6 is the low string. In `frets` mode, `5:3/8` means string 5, fret 3, eighth note; `[3:0,2:1,1:0]/4` plucks three strings together. `cross` takes the same input but displays cross noteheads. `strum` uses `down/8 up/8 mute/8 r/8`. `down` describes the hand moving from low to high strings, so its TAB arrow points upward. Dead notes use `3:x/8`; frets range from 0 to 36.

Default tuning is standard guitar. Custom `tuning: [E4, B3, G3, D3, A2, E2]` is ordered **string 1 to 6**. Chord shapes such as `chordShapes: { Cadd9: [x, 3, 2, 0, 3, 0] }` are ordered **string 6 to 1**: `x` means muted and `0` means open. A chord object can specify `baseFret` for its diagram. These two array orders are opposite.

`chords: C` labels the start of a bar. Position multiple chords explicitly: `chords: [{name: C, beat: 1}, {name: G, beat: 3}]`. Common shapes are built in; unknown names still print, but diagrams need `chordShapes` or a chord object's `diagram`. Chord labels do not automatically create accompaniment or rhythm; write guitar/piano events separately.

`key` is the melody's sounding key; `fingering` can label a shape key. `capo` raises guitar MIDI by that many semitones without changing numbered pitches. The tool does not infer the relationship between labels and sounding key. `frets` MIDI uses the written frets; `cross` prefers the current chord diagram's string pitches and falls back to written frets. `strum` is silent without a usable shape and does not simulate string-to-string delay.

Piano uses `right` / `left` for treble and bass staves, for example `right: "[C4,E4,G4]/1"` and `left: "C3/2 G2/2"`. An omitted hand becomes a full-bar rest. Multiple voices on one hand use `voices` with `staff: right` / `staff: left`.

Drum names are `kick snare hat openhat pedal crash ride tom1 tom2 floor`. `[kick,hat]/8` plays both together. Use independent full-bar voices for separate kick and cymbal patterns, as in the complete example. MIDI uses GM percussion mapping and channel 10.

## Key, meter, tempo, and pickups

Bar-level `key`, `meter`, and `tempo` persist until changed. BPM ranges from 10 to 400. Numeric `tempo: 108` always means quarter note = 108; a dotted-quarter pulse in 6/8 requires `tempo: {bpm: 72, unit: "4."}`.

For chords and `tempoChanges`, `beat` starts at 1 and counts the current meter's **denominator note**. In 6/8, `beat: 4` is the fourth eighth note, the start of the second dotted-quarter pulse. An intra-bar change can use `tempoChanges: [{beat: 4, bpm: 80, unit: "4."}]`; fractional positions are allowed, such as `beat: 2.5` in 4/4.

`ramp: {to: 120, bars: 2, text: accel.}` starts at the current bar's initial tempo, spans two bars, and reaches its target at the following bar's start. Ramps cannot overlap, exceed the score, or contain separate `tempo` / `tempoChanges` settings. MIDI samples linear BPM every eighth note and retains the starting tempo unit.

Bar-level `pickup: 4` creates a one-quarter-note pickup; every explicit voice must fill that shortened duration. The value is a note duration, not a beat count, and cannot exceed the normal bar length. Convert audio seconds through the [tempo](../tasks/tempo.md) and [meter](../tasks/meter.md) maps before assigning `beat` positions.

## Reusable patterns and layout

Top-level `patterns` defines named bar content; a bar references it with `use`. Merge this fragment into a score with declared `guitar` and `vocal` tracks:

```yaml
patterns:
  groove:
    chords: C
    guitar: "5:3/4 3:0/4 2:1/4 1:0/4"
bars:
  - use: groove
    vocal: "1/4 2/4 3/2"
  - use: groove
    chords: Am
    guitar: "5:0/4 3:2/4 2:1/4 1:0/4"
    vocal: "3/4 2/4 1/2"
```

`use` performs a shallow merge: explicit fields replace the entire matching pattern field, without concatenating notes or deep-merging voices. Patterns cannot contain nested `use`. After changing chord labels, also check accompaniment pitches.

`section` prints a section label and starts a new system. `expression` prints performance text without changing tempo. `break: true` / `pageBreak: true` starts a system/page before that bar. `repeatStart` / `repeatEnd` draws repeat barlines and `final: true` draws a final barline. MIDI plays bars in written order and **does not expand repeats**; explicitly duplicate bars when playback must repeat them.

`layout` supports `barsPerSystem`, `width`, `height`, `margin`, `systemGap`, `lyricSize`, `lyricFont`, `noteSize`, `titleSize`, `showBarNumbers`, `showTrackNames`, `chordDiagrams`, and `justifyLast`. `barsPerSystem` is an upper limit; wide lyrics can reduce the count. Adjust layout parameters while preserving musical durations. PNG accepts `--scale 2`. Resolve page-capacity diagnostics without deleting required music.

## Model workflow and delivery

1. Establish parts, key, meter, tempo, ranges, and form from the request. Arrange supplied notes directly. For recordings, cross-check every event against complementary evidence and keep the event review table required by [score assembly](../tasks/score-export.md). Label original additions; keep uncertainty outside unsupported YAML fields.
2. Manually write each note, rest, tie, and individually verified lyric character/syllable into editable YAML by bar and voice. Do not script event generation, import detector MIDI, automatically fill gaps, or use models/scripts to map lyrics onto notes. Check each voice's duration, lyric correspondence as well as count, guitar strings/frets, sounding harmony, and tempo units after meter changes. Review each occurrence before reusing material through `patterns`/`use` or copying bars.
3. After `validate --json` succeeds, use `inspect` to check the event timeline. Duration diagnostics use quarter-note units: a 6/8 bar should total 3. Repair the identified target by reviewing the source and notation decisions; do not insert automatic rests or stretch notes just to pass validation.
4. Render PNG and inspect part alignment, lyrics, chord diagrams, ties/slurs, meter changes, and pagination. Multi-page SVG/PNG may create `name-1.png` and similar files; inspect every page using the returned `files` list.
5. Export the requested formats and deliver YAML plus actual generated files. PDF/HTML includes all pages. MIDI supports pitch/rhythm checking; file generation is not listening validation. MusicXML converts numbered notation into sounding pitches on a staff, and external editors re-engrave it.

Limits are 5 MB input, 32 tracks, and 10000 bars. MIDI supports at most 15 independent pitched tracks, with percussion on channel 10. Grace notes, cross-staff beams, nested slurs, microtones, and guitar bends are outside the supported scope. For more demanding engraving, continue with MusicXML in a suitable editor and identify any unchecked layout or musical content.

## Official sources

- [npm package](https://www.npmjs.com/package/score-text) and [source repository](https://github.com/TaiRuiQu/score-text).
- [v0.1.0 notation specification](https://github.com/TaiRuiQu/score-text/blob/v0.1.0/docs/notation.md) and [agent guide](https://github.com/TaiRuiQu/score-text/blob/v0.1.0/docs/agent-guide.md).
- [v0.1.0 JSON Schema](https://github.com/TaiRuiQu/score-text/blob/v0.1.0/schema/score-text.schema.json), [CLI implementation](https://github.com/TaiRuiQu/score-text/blob/v0.1.0/src/cli.ts), and [complete examples](https://github.com/TaiRuiQu/score-text/tree/v0.1.0/examples).
