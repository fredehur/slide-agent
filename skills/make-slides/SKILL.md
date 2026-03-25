---
name: make-slides
description: Turn any document into a clean HTML slide deck with speaking notes. Use when the user wants to create presentation slides from a document, principles list, or structured text.
---

# Make Slides

Turn any document into a self-contained HTML slide deck + speaking notes markdown file.

**Announce at start:** "I'm using the make-slides skill to build your slide deck."

## Overview

You receive a document (principles, sections, headings, or structured text) and produce two files:
- `output/slides.html` — self-contained HTML, keyboard navigable, with simple visuals
- `output/speaking-notes.md` — presenter speaking notes

You write both files directly. No external tools required.

---

## Step 1 — Receive Input

If the user passed a file path, read it. If they pasted content, use that. If neither, ask:
> "Please paste the document content you want to turn into slides."

---

## Step 2 — Analyse Structure

Read the document and identify:
- **Title** and subtitle (or infer from content)
- **Principles / sections** — numbered items, bold headings, or clear paragraphs
- **Purpose statement** — opening paragraph (becomes opening slide speaker notes)
- **Summary section** — "how these are used" or equivalent (becomes summary slide)
- **Closing statement** — final paragraph or quote (becomes closing slide)
- **Audience** — non-technical unless stated otherwise

Count the principles/sections. Each becomes one slide. Total slides = 1 opening + N principles + 1 summary (if present) + 1 closing.

---

## Step 3 — Build Slide Data

Map the document into this structure (keep internally, don't write to disk):

```
Opening slide: title, subtitle
Principle slides (one per section): label ("Principle N of M"), headline, bullets (2-4), visual type
Summary slide: headline, 2-3 labelled items
Closing slide: quote or final statement
```

### Visual assignment — pick the best fit per principle:

| Visual | Use when the principle is about... |
|---|---|
| `dial` | Risk as a spectrum, not binary, continuous state |
| `cost_ladder` | Effort, cost, deterrence, or difficulty scaling |
| `scenario_cards` | Concrete examples, scenario types, incident categories |
| `flow` | Sequential steps, funnel, derivation (A → B → C) |
| `layers` | Stacking inputs to reach a result (Peer + Env = Likelihood) |
| `equation` | Transformation: input → financial output |
| `distribution` | Ranges, severity levels, multiple metric views |
| `grid2x2` | Exactly four components or items |
| `chain` | Traceability, provenance, linked steps |
| `cycle` | Refresh, living process, repeat cadence |
| `none` | Summary and closing slides |

**Wording rule:** Keep bullet text as close to the source document as possible. Only simplify when essential for plain-language accessibility.

---

## Step 4 — Write output/slides.html

Write a complete self-contained HTML file. Use this exact template, replacing the `<!-- SLIDES -->` block with rendered slide sections:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}}</title>
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #fff; color: #1a1a1a; height: 100vh; overflow: hidden; }
    .slides { width: 100%; height: 100vh; position: relative; }
    section { display: none; position: absolute; inset: 0; padding: 80px 100px; flex-direction: column; justify-content: center; }
    section.active { display: flex; }
    .slide-inner { display: flex; align-items: center; gap: 80px; width: 100%; }
    .slide-text { flex: 1; min-width: 0; }
    .slide-visual { flex: 0 0 280px; display: flex; align-items: center; justify-content: center; }
    section.opening { align-items: center; text-align: center; }
    section.opening h1 { font-size: 3rem; font-weight: 700; line-height: 1.2; margin-bottom: 1.2rem; }
    section.opening p { font-size: 1.5rem; color: #555; font-weight: 400; }
    .label { font-size: 0.8rem; font-weight: 600; color: #999; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 1.4rem; }
    h2 { font-size: 2.1rem; font-weight: 700; line-height: 1.25; margin-bottom: 1.4rem; }
    .divider { width: 56px; height: 3px; background: #1a1a1a; margin-bottom: 2rem; }
    ul { list-style: none; display: flex; flex-direction: column; gap: 1.1rem; }
    ul li { font-size: 1.12rem; line-height: 1.65; padding-left: 1.6rem; position: relative; color: #222; }
    ul li::before { content: '—'; position: absolute; left: 0; color: #aaa; }
    .intro-line { font-size: 1.12rem; line-height: 1.65; color: #222; margin-bottom: 1.1rem; }
    section.summary ul li strong { font-weight: 700; color: #1a1a1a; }
    section.closing { align-items: center; text-align: center; justify-content: center; }
    section.closing blockquote { font-size: 1.5rem; line-height: 1.75; max-width: 740px; font-style: italic; color: #333; }
    .nav-btn { position: fixed; bottom: 28px; background: none; border: 1px solid #ccc; padding: 8px 22px; font-size: 0.88rem; cursor: pointer; border-radius: 4px; color: #333; transition: background 0.15s; }
    .nav-btn:hover { background: #f5f5f5; }
    .nav-btn:disabled { opacity: 0.22; cursor: default; background: none; }
    #btn-prev { left: 40px; }
    #btn-next { right: 40px; }
    .counter { position: fixed; bottom: 32px; right: 120px; font-size: 0.82rem; color: #bbb; letter-spacing: 0.04em; }
    /* Visuals */
    .dial-track { width:220px; height:10px; background:#eee; border-radius:10px; position:relative; margin:0 auto 12px; }
    .dial-fill { position:absolute; left:0; top:0; bottom:0; width:55%; background:linear-gradient(to right,#ccc,#555); border-radius:10px; }
    .dial-dot { position:absolute; top:50%; left:55%; transform:translate(-50%,-50%); width:20px; height:20px; background:#1a1a1a; border-radius:50%; border:3px solid #fff; box-shadow:0 0 0 2px #1a1a1a; }
    .dial-labels { display:flex; justify-content:space-between; font-size:0.75rem; color:#aaa; margin-top:6px; }
    .dial-caption { text-align:center; font-size:0.78rem; color:#888; margin-top:14px; font-style:italic; }
    .cost-ladder { display:flex; flex-direction:column; gap:8px; width:220px; }
    .cost-bar-fill { height:28px; background:#e8e8e8; border-radius:4px; display:flex; align-items:center; padding:0 10px; font-size:0.78rem; color:#555; white-space:nowrap; }
    .cost-bar-fill.dark { background:#1a1a1a; color:#fff; }
    .cost-caption { text-align:center; font-size:0.75rem; color:#888; margin-top:10px; font-style:italic; }
    .scenario-cards { display:flex; flex-direction:column; gap:10px; width:220px; }
    .scenario-card { border:1px solid #e0e0e0; border-radius:6px; padding:10px 14px; font-size:0.82rem; color:#333; line-height:1.4; }
    .scenario-card span { font-weight:600; display:block; margin-bottom:2px; }
    .flow { display:flex; flex-direction:column; align-items:center; gap:0; width:200px; }
    .flow-box { width:100%; text-align:center; padding:10px 14px; border:1px solid #ddd; border-radius:6px; font-size:0.82rem; color:#333; line-height:1.4; }
    .flow-box.highlight { background:#1a1a1a; color:#fff; border-color:#1a1a1a; }
    .flow-arrow { font-size:1.2rem; color:#bbb; line-height:1; padding:4px 0; }
    .layers { display:flex; flex-direction:column; gap:8px; width:220px; }
    .layer { padding:10px 16px; border-radius:6px; font-size:0.8rem; line-height:1.4; color:#555; border-left:3px solid #ccc; }
    .layer.l1 { border-color:#bbb; background:#fafafa; }
    .layer.l2 { border-color:#888; background:#f3f3f3; }
    .layer.l3 { border-color:#444; background:#eee; color:#222; font-weight:500; }
    .equation { text-align:center; width:220px; }
    .eq-box { border:1px solid #ddd; border-radius:6px; padding:12px; font-size:0.82rem; color:#333; margin-bottom:8px; line-height:1.5; }
    .eq-arrow { font-size:1.4rem; color:#bbb; margin-bottom:8px; display:block; }
    .eq-box.highlight { background:#1a1a1a; color:#fff; border-color:#1a1a1a; font-weight:600; }
    .eq-sub { margin-top:12px; font-size:0.75rem; color:#888; line-height:1.8; }
    .dist { display:flex; flex-direction:column; gap:10px; width:220px; }
    .dist-row { display:flex; align-items:center; gap:8px; }
    .dist-label { font-size:0.72rem; color:#888; width:72px; text-align:right; flex-shrink:0; }
    .dist-bar { height:22px; background:#1a1a1a; border-radius:3px; }
    .dist-caption { font-size:0.72rem; color:#aaa; text-align:center; margin-top:6px; font-style:italic; }
    .grid2x2 { display:grid; grid-template-columns:1fr 1fr; gap:8px; width:220px; }
    .grid-cell { border:1px solid #e0e0e0; border-radius:6px; padding:10px; font-size:0.75rem; color:#444; line-height:1.4; text-align:center; }
    .grid-cell span { font-size:1.1rem; display:block; margin-bottom:4px; }
    .chain { display:flex; flex-direction:column; align-items:flex-start; gap:0; width:200px; }
    .chain-item { display:flex; align-items:center; gap:10px; padding:8px 12px; border:1px solid #e0e0e0; border-radius:6px; width:100%; font-size:0.78rem; color:#333; background:#fafafa; }
    .chain-item.end { background:#1a1a1a; color:#fff; border-color:#1a1a1a; }
    .chain-dot { width:8px; height:8px; background:#bbb; border-radius:50%; flex-shrink:0; }
    .chain-dot.dark { background:#fff; }
    .chain-line { width:2px; height:14px; background:#ddd; margin-left:15px; }
    .cycle { text-align:center; width:220px; }
    .cycle-ring { width:44px; height:44px; border:3px solid #1a1a1a; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.1rem; margin:0 auto 12px; }
    .cycle-items { display:flex; flex-direction:column; gap:0; }
    .cycle-item { display:flex; align-items:center; gap:10px; padding:9px 14px; font-size:0.8rem; color:#333; }
    .cycle-item:not(:last-child) { border-bottom:1px dashed #e8e8e8; }
    .cycle-arrow { font-size:0.9rem; color:#bbb; }
  </style>
</head>
<body>
<div class="slides">
<!-- SLIDES -->
</div>
<button class="nav-btn" id="btn-prev" onclick="move(-1)" disabled>← Prev</button>
<span class="counter" id="counter">1 / {{TOTAL}}</span>
<button class="nav-btn" id="btn-next" onclick="move(1)">Next →</button>
<script>
  const slides = document.querySelectorAll('section');
  let current = 0;
  function show(n) {
    slides[current].classList.remove('active');
    current = Math.max(0, Math.min(n, slides.length - 1));
    slides[current].classList.add('active');
    document.getElementById('counter').textContent = (current + 1) + ' / ' + slides.length;
    document.getElementById('btn-prev').disabled = current === 0;
    document.getElementById('btn-next').disabled = current === slides.length - 1;
  }
  function move(dir) { show(current + dir); }
  document.addEventListener('keydown', e => {
    if (e.key === 'ArrowRight') move(1);
    if (e.key === 'ArrowLeft') move(-1);
  });
</script>
</body>
</html>
```

### Slide section templates

**Opening:**
```html
<section class="opening active">
  <h1>TITLE</h1>
  <p>SUBTITLE</p>
</section>
```

**Principle with visual (two-column):**
```html
<section>
  <div class="slide-inner">
    <div class="slide-text">
      <div class="label">Principle N of M</div>
      <h2>HEADLINE</h2>
      <div class="divider"></div>
      <!-- optional: <p class="intro-line">INTRO LINE</p> -->
      <ul>
        <li>BULLET</li>
        <li>BULLET</li>
        <li>BULLET</li>
      </ul>
    </div>
    <div class="slide-visual">
      <!-- VISUAL HTML — see visual blocks below -->
    </div>
  </div>
</section>
```

**Summary:**
```html
<section class="summary">
  <h2>HEADLINE</h2>
  <div class="divider"></div>
  <ul>
    <li><strong>LABEL</strong> — TEXT</li>
    <li><strong>LABEL</strong> — TEXT</li>
    <li><strong>LABEL</strong> — TEXT</li>
  </ul>
</section>
```

**Closing:**
```html
<section class="closing">
  <blockquote>QUOTE</blockquote>
</section>
```

### Visual HTML blocks

**dial:**
```html
<div>
  <div class="dial-track"><div class="dial-fill"></div><div class="dial-dot"></div></div>
  <div class="dial-labels"><span>Low</span><span>High</span></div>
  <div class="dial-caption">Risk moves along a spectrum —<br>it never reaches zero</div>
</div>
```

**cost_ladder:**
```html
<div>
  <div class="cost-ladder">
    <div><div class="cost-bar-fill" style="width:80px">Low defences</div></div>
    <div><div class="cost-bar-fill" style="width:130px">Medium defences</div></div>
    <div><div class="cost-bar-fill dark" style="width:190px">Strong defences</div></div>
  </div>
  <div class="cost-caption">Stronger defences raise<br>the cost of attack</div>
</div>
```

**scenario_cards** — use the first 3 bullets, split on "—" for title/description:
```html
<div class="scenario-cards">
  <div class="scenario-card"><span>TITLE</span>DESCRIPTION</div>
  <div class="scenario-card"><span>TITLE</span>DESCRIPTION</div>
  <div class="scenario-card"><span>TITLE</span>DESCRIPTION</div>
</div>
```

**flow** — use 3 bullets, last box gets class `highlight`:
```html
<div class="flow">
  <div class="flow-box">ITEM 1</div>
  <div class="flow-arrow">↓</div>
  <div class="flow-box">ITEM 2</div>
  <div class="flow-arrow">↓</div>
  <div class="flow-box highlight">RESULT</div>
</div>
```

**layers** — 3 items, l1/l2/l3:
```html
<div class="layers">
  <div class="layer l1">LAYER 1</div>
  <div class="layer l2">LAYER 2</div>
  <div class="layer l3">RESULT</div>
</div>
```

**equation:**
```html
<div class="equation">
  <div class="eq-box">INPUT</div>
  <span class="eq-arrow">↓</span>
  <div class="eq-box highlight">OUTPUT (€)</div>
  <div class="eq-sub">Objective &nbsp;·&nbsp; Auditable &nbsp;·&nbsp; Comparable</div>
</div>
```

**distribution:**
```html
<div class="dist">
  <div class="dist-row"><div class="dist-label">Expected</div><div class="dist-bar" style="width:80px"></div></div>
  <div class="dist-row"><div class="dist-label">Bad year</div><div class="dist-bar" style="width:130px"></div></div>
  <div class="dist-row"><div class="dist-label">Worst case</div><div class="dist-bar" style="width:180px"></div></div>
  <div class="dist-caption">Financial loss →</div>
</div>
```

**grid2x2** — use 4 bullets:
```html
<div class="grid2x2">
  <div class="grid-cell"><span>①</span>ITEM 1</div>
  <div class="grid-cell"><span>②</span>ITEM 2</div>
  <div class="grid-cell"><span>③</span>ITEM 3</div>
  <div class="grid-cell"><span>④</span>ITEM 4</div>
</div>
```

**chain** — use 3-4 bullets, last item gets class `end` and `chain-dot dark`:
```html
<div class="chain">
  <div class="chain-item"><div class="chain-dot"></div>ITEM 1</div>
  <div class="chain-line"></div>
  <div class="chain-item"><div class="chain-dot"></div>ITEM 2</div>
  <div class="chain-line"></div>
  <div class="chain-item"><div class="chain-dot"></div>ITEM 3</div>
  <div class="chain-line"></div>
  <div class="chain-item end"><div class="chain-dot dark"></div>OUTPUT</div>
</div>
```

**cycle:**
```html
<div class="cycle">
  <div class="cycle-ring">↻</div>
  <div class="cycle-items">
    <div class="cycle-item"><span class="cycle-arrow">→</span>STEP 1</div>
    <div class="cycle-item"><span class="cycle-arrow">→</span>STEP 2</div>
    <div class="cycle-item"><span class="cycle-arrow">→</span>STEP 3</div>
    <div class="cycle-item"><span class="cycle-arrow">→</span>Repeat</div>
  </div>
</div>
```

---

## Step 5 — Write output/speaking-notes.md

Write speaking notes for every slide using this format:

```markdown
# Speaking Notes — TITLE
### N slides | ~3 min per slide

> **Presenter guidance:** Speak slowly and clearly at all times. Pause after each bullet. Never introduce ideas that are not on the slide. Read the headline first, then walk through each point.

---

## Slide N — LABEL
**HEADLINE**

---

Read the title: *HEADLINE*

[Point 1] BULLET TEXT

[Point 2] BULLET TEXT

[Point 3] BULLET TEXT

---
```

For opening slides: write a short welcome + "Let us begin."
For summary slides: walk through each labelled item.
For closing slides: instruct presenter to read the quote slowly, then "Thank you."

---

## Step 6 — Verify and Report

Check both files exist and are non-empty. Then report:

```
make-slides complete.

Slides:  output/slides.html       (N slides)
Notes:   output/speaking-notes.md (N sections)

Open slides.html in a browser. Use ← → arrow keys to navigate.
```

---

## Output location

Always write to `output/` relative to the current working directory. Create the directory if it does not exist.
