#!/usr/bin/env python3
"""
build_notes.py — Generate speaking notes markdown from slides_data.json

Usage: uv run python tools/build_notes.py <input_json> <output_md>
"""

import json
import sys
from pathlib import Path


def build(input_path: str, output_path: str) -> None:
    data = json.loads(Path(input_path).read_text(encoding='utf-8'))
    title = data.get('title', 'Presentation')
    slides = data.get('slides', [])
    total = len(slides)
    mins_per_slide = 45 // total if total else 3

    lines = []
    lines.append(f"# Speaking Notes — {title}")
    lines.append(f"### {total} slides | ~{mins_per_slide} min per slide | Live translation in progress")
    lines.append("")
    lines.append("> **Presenter guidance:** Speak slowly and clearly at all times. Pause after each bullet — the translator needs time. Never introduce ideas that are not on the slide. Read the headline first, then walk through each point.")
    lines.append("")
    lines.append("---")
    lines.append("")

    for i, slide in enumerate(slides, 1):
        stype = slide.get('type', 'principle')

        if stype == 'opening':
            lines.append(f"## Slide {i} — Opening")
            lines.append(f"**{slide.get('title', '')}**")
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("Welcome everyone.")
            lines.append("")
            lines.append(f"Today we are here to share the foundational principles behind our approach. This session establishes a shared understanding before we move to practical application.")
            lines.append("")
            lines.append("We will go through each principle, one at a time. Each one is short and clear.")
            lines.append("")
            lines.append("Let us begin.")
            lines.append("")
            lines.append("---")
            lines.append("")

        elif stype == 'principle':
            label = slide.get('label', f'Principle {i}')
            headline = slide.get('headline', '')
            intro_line = slide.get('intro_line')
            bullets = slide.get('bullets', [])

            lines.append(f"## Slide {i} — {label}")
            lines.append(f"**{headline}**")
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append(f"Read the title: *{headline}*")
            lines.append("")

            if intro_line:
                lines.append(intro_line)
                lines.append("")

            for j, bullet in enumerate(bullets, 1):
                lines.append(f"[Point {j}] {bullet}")
                lines.append("")

            lines.append("---")
            lines.append("")

        elif stype == 'summary':
            headline = slide.get('headline', 'Summary')
            items = slide.get('items', [])

            lines.append(f"## Slide {i} — {headline}")
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append(f"Read the title: *{headline}*")
            lines.append("")

            for item in items:
                lines.append(f"[{item['label']}] {item['text']}")
                lines.append("")

            lines.append("---")
            lines.append("")

        elif stype == 'closing':
            quote = slide.get('quote', '')
            lines.append(f"## Slide {i} — Close")
            lines.append("")
            lines.append("---")
            lines.append("")
            lines.append("I will leave you with the purpose of everything we have discussed today.")
            lines.append("")
            lines.append("[Read the quote slowly:]")
            lines.append("")
            lines.append(f"*\"{quote}\"*")
            lines.append("")
            lines.append("Thank you. We are happy to take questions.")
            lines.append("")
            lines.append("---")
            lines.append("")

    lines.append("> **End of speaking notes**")

    Path(output_path).write_text('\n'.join(lines), encoding='utf-8')
    print(f"Wrote {output_path} ({Path(output_path).stat().st_size} bytes)")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: build_notes.py <input.json> <output_md>")
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])
