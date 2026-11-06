# Sonic Annotator

Status: official interface reviewed 2026-11-06; not installed or run. This is a batch Vamp host, not a chord model. Use it with [Chordino](chordino.md) or another explicitly chosen plugin.

For an existing installation, inspect help and enumerate plugin outputs:

```sh
sonic-annotator --help
sonic-annotator -l
```

The upstream CLI accepts `-d OUTPUT_ID AUDIO -w csv --csv-stdout` for a default transform; substitute an exact output ID returned by `-l`. Use `-s OUTPUT_ID` to inspect a default transform or `-t TRANSFORM_FILE` for recorded settings. Capture CSV and stderr separately into new result files; do not overwrite existing annotations.

Verify actual timestamp/duration/label columns before normalization, rather than assuming all Vamp outputs have one shape. Retain the raw CSV and transform parameters. Convert crop-relative times once, as required by [review](../tasks/review.md).

The host and plugins need compatible binary architecture and plugin search paths. Follow [setup](../tasks/setup.md) for new software. Source: [official CLI tutorial](https://github.com/sonic-visualiser/sonic-annotator#readme), [project](https://vamp-plugins.org/sonic-annotator/).
