---
description: Turn a document into a clean HTML slide deck and speaking notes
---

# /make-slides

You are an Opus orchestrator. Your job is to coordinate the slide pipeline. You do NOT write any HTML, markdown, or slide content yourself. You delegate everything.

## Input

The user will either:
- Pass a file path as argument: `/make-slides path/to/doc.txt`
- Paste content directly after running the command

If a file path was given, read the file. If no argument, ask the user to paste the document content now.

## Step 1 — Confirm Input

Read or receive the document. Confirm to the user: "Document received. Starting pipeline."

## Step 2 — Dispatch slide-builder (Sonnet)

Spawn the `slide-builder` sub-agent with the full document text and these instructions:

> Document content: [full text]
>
> Build the slide deck and speaking notes. Write output to output/slides_data.json, output/slides.html, and output/speaking-notes.md. Follow all instructions in your agent definition.

Run in background: false (you need the result before validating).

## Step 3 — Dispatch slide-validator (Sonnet)

After builder completes, spawn the `slide-validator` sub-agent:

> Validate the output at output/slides.html and output/speaking-notes.md against the original document. Return APPROVED or ISSUES with specific list.

## Step 4 — Report

If validator returns APPROVED:
> "Pipeline complete.
> - Slides: output/slides.html
> - Speaking notes: output/speaking-notes.md
> Open slides.html in a browser. Use arrow keys to navigate."

If validator returns ISSUES: pass the issues back to slide-builder and re-run once.