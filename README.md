# slide-agent

Turn any document into a clean, self-contained HTML slide deck and presenter speaking notes using Claude Code.

## What it does

Give it any document that contains principles, sections, or structured ideas — a spec, a briefing, a framework doc. It parses the structure, maps each section to a slide with an appropriate visual, and produces a keyboard-navigable HTML deck alongside speaker notes formatted for live translation contexts.

Input: any plain-text or markdown document.
Output: `output/slides.html` (open in any browser) + `output/speaking-notes.md`.

## Usage

Open the `slide-agent` folder in Claude Code, then run:

```
/make-slides path/to/document.txt
```

Or run `/make-slides` with no argument — Claude will prompt you to paste the document content.

When the pipeline completes you will see:

```
Pipeline complete.
- Slides: output/slides.html
- Speaking notes: output/speaking-notes.md
Open slides.html in a browser. Use arrow keys to navigate.
```

## Output

| File | Description |
|---|---|
| `output/slides.html` | Self-contained HTML slide deck. No external dependencies. Open in any browser and use `←` / `→` arrow keys to navigate. Includes a slide counter. |
| `output/speaking-notes.md` | Presenter script with translator guidance at the top. One section per slide, with each bullet cued as a numbered point. |
| `output/slides_data.json` | Intermediate structured slide data (JSON). Not needed for presentation — useful for debugging or re-generating output. |

## How it works

```
/make-slides (Opus orchestrator)
  └── slide-builder (Sonnet)
        ├── Parses document → output/slides_data.json
        ├── uv run python tools/build_slides.py  → output/slides.html
        └── uv run python tools/build_notes.py   → output/speaking-notes.md
  └── slide-validator (Sonnet)
        └── Checks completeness and quality → APPROVED or ISSUES
              └── On ISSUES: builder re-runs once with specific feedback
```

The orchestrator delegates everything — it never writes slide content itself. The builder and validator are separate agents; output is not accepted until the validator passes.

### Visual types

The builder assigns one of 10 built-in visuals per slide based on the principle's core idea:

| Visual | Used for |
|---|---|
| `dial` | Risk as a spectrum |
| `cost_ladder` | Effort or deterrence scaling |
| `scenario_cards` | List of concrete scenario types |
| `flow` | Sequential steps or derivation |
| `layers` | Stacking inputs to reach a result |
| `equation` | Input → output transformation |
| `distribution` | Loss ranges at different severity levels |
| `grid2x2` | Exactly four components or quadrants |
| `chain` | Traceability or linked steps |
| `cycle` | Ongoing or repeating process |

## Requirements

- [Claude Code](https://claude.ai/code)
- [uv](https://github.com/astral-sh/uv) (Python package manager)

No API keys, no external CDN dependencies, no build step. The HTML output is fully self-contained.
