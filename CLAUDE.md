# slide-agent

Turn any document into a clean HTML slide deck + speaking notes using Claude Code.

## Usage

```bash
/make-slides path/to/document.txt
# or
/make-slides  # then paste content when prompted
```

Output is written to `output/`.

## Commands

| Command | Description |
|---|---|
| `/make-slides` | Orchestrates full pipeline: parse → build → validate → output |

## Sub-Agents

| Agent | Model | Role |
|---|---|---|
| `slide-builder` | sonnet | Parses document, generates slide JSON, builds HTML + speaking notes |
| `slide-validator` | sonnet | Verifies output completeness and quality |

## Output

- `output/slides.html` — self-contained HTML slide deck (keyboard navigable)
- `output/speaking-notes.md` — presenter speaking notes with translator guidance

## Engineering Protocol

- Orchestrator (Opus) delegates — never implements
- Builder/Validator pairing on every run
- Filesystem as state: JSON intermediate written to output/slides_data.json
