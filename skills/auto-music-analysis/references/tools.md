# Tool Registry and Integration Contract

## Registered tools

Integrated tools: none.

There is currently no executable audio analysis, source separation, transcription, or score export implementation, and no runtime dependencies to install. The host language model reads this skill and coordinates tools integrated later.

## Adding a tool

After the user selects a tool, add its record here. Move lengthy instructions to a dedicated document in this directory and link to it from this registry. Verify the real documentation and executable interface rather than guessing commands or parameters from the tool's name.

Each record should contain:

| Field | Information to record |
| --- | --- |
| Identity and status | Tool name; planned, integrated, or unavailable; verified version |
| Capabilities and limitations | Supported analysis tasks, instruments or parts, and conclusions the tool cannot establish |
| Source and distribution | Official source, license, checkpoint source, and separate restrictions on use or redistribution |
| Environment and installation | Dependency versions, supported platforms, CPU or GPU requirements, and necessary installation steps |
| Invocation | CLI, Python API, MCP, or HTTP; exact entry point, arguments, and success or failure indicators |
| Input | Formats, sample rate, channels, duration limits, and required preprocessing |
| Output | Files or return structures, time units and origin, pitch representation, label vocabulary, and meaning of confidence scores |
| Operating conditions | Local or remote execution, audio uploads, fees, and configuration variable names; keep credentials out of the skill |
| Verification evidence | Characteristics of the verification input, actual invocation, observed artifacts, and known failure cases |

Documentation alone leaves a tool in the planned state. Mark it integrated only after executing it and checking valid output. Install checkpoints and third-party programs under their own licenses; distributing this skill does not establish permission to redistribute those dependencies.

## Passing data between tools

- Preserve raw tool outputs where possible. Add small adapter scripts only when needed to bridge incompatible interfaces, and document the conversion.
- Identify audio files, sample rate, channels, and transformations relative to the original input. For timed events, record units, time origin, and analyzed region.
- Preserve original representations for pitches, notes, drums, and chords. When normalization is needed, document mappings and retain values that cannot be mapped.
- Record missing confidence as not provided. Unsupported capability, execution failure, and no detected events are distinct outcomes.
- Keep tool outputs separate from language model interpretations. Choose export formats based on integrated tools when the user requests an export.
