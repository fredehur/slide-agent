#!/usr/bin/env python3
"""
build_slides.py — Generate self-contained HTML slide deck from slides_data.json

Usage: uv run python tools/build_slides.py <input_json> <output_html>
"""

import json
import sys
from pathlib import Path


VISUAL_CSS = """
    /* ─── Dial ─── */
    .dial-track { width:220px; height:10px; background:#eee; border-radius:10px; position:relative; margin:0 auto 12px; }
    .dial-fill { position:absolute; left:0; top:0; bottom:0; width:55%; background:linear-gradient(to right,#ccc,#555); border-radius:10px; }
    .dial-dot { position:absolute; top:50%; left:55%; transform:translate(-50%,-50%); width:20px; height:20px; background:#1a1a1a; border-radius:50%; border:3px solid #fff; box-shadow:0 0 0 2px #1a1a1a; }
    .dial-labels { display:flex; justify-content:space-between; font-size:0.75rem; color:#aaa; margin-top:6px; }
    .dial-caption { text-align:center; font-size:0.78rem; color:#888; margin-top:14px; font-style:italic; }

    /* ─── Cost ladder ─── */
    .cost-ladder { display:flex; flex-direction:column; gap:8px; width:220px; }
    .cost-bar-fill { height:28px; background:#e8e8e8; border-radius:4px; display:flex; align-items:center; padding:0 10px; font-size:0.78rem; color:#555; white-space:nowrap; }
    .cost-bar-fill.dark { background:#1a1a1a; color:#fff; }
    .cost-caption { text-align:center; font-size:0.75rem; color:#888; margin-top:10px; font-style:italic; }

    /* ─── Scenario cards ─── */
    .scenario-cards { display:flex; flex-direction:column; gap:10px; width:220px; }
    .scenario-card { border:1px solid #e0e0e0; border-radius:6px; padding:10px 14px; font-size:0.82rem; color:#333; line-height:1.4; }
    .scenario-card span { font-weight:600; display:block; margin-bottom:2px; }

    /* ─── Flow ─── */
    .flow { display:flex; flex-direction:column; align-items:center; gap:0; width:200px; }
    .flow-box { width:100%; text-align:center; padding:10px 14px; border:1px solid #ddd; border-radius:6px; font-size:0.82rem; color:#333; line-height:1.4; }
    .flow-box.highlight { background:#1a1a1a; color:#fff; border-color:#1a1a1a; }
    .flow-arrow { font-size:1.2rem; color:#bbb; line-height:1; padding:4px 0; }

    /* ─── Layers ─── */
    .layers { display:flex; flex-direction:column; gap:8px; width:220px; }
    .layer { padding:10px 16px; border-radius:6px; font-size:0.8rem; line-height:1.4; color:#555; border-left:3px solid #ccc; }
    .layer.l1 { border-color:#bbb; background:#fafafa; }
    .layer.l2 { border-color:#888; background:#f3f3f3; }
    .layer.l3 { border-color:#444; background:#eee; color:#222; font-weight:500; }

    /* ─── Equation ─── */
    .equation { text-align:center; width:220px; }
    .eq-box { border:1px solid #ddd; border-radius:6px; padding:12px; font-size:0.82rem; color:#333; margin-bottom:8px; line-height:1.5; }
    .eq-arrow { font-size:1.4rem; color:#bbb; margin-bottom:8px; display:block; }
    .eq-box.highlight { background:#1a1a1a; color:#fff; border-color:#1a1a1a; font-weight:600; }
    .eq-sub { margin-top:12px; font-size:0.75rem; color:#888; line-height:1.8; }

    /* ─── Distribution ─── */
    .dist { display:flex; flex-direction:column; gap:10px; width:220px; }
    .dist-row { display:flex; align-items:center; gap:8px; }
    .dist-label { font-size:0.72rem; color:#888; width:72px; text-align:right; flex-shrink:0; }
    .dist-bar { height:22px; background:#1a1a1a; border-radius:3px; }
    .dist-caption { font-size:0.72rem; color:#aaa; text-align:center; margin-top:6px; font-style:italic; }

    /* ─── Grid 2x2 ─── */
    .grid2x2 { display:grid; grid-template-columns:1fr 1fr; gap:8px; width:220px; }
    .grid-cell { border:1px solid #e0e0e0; border-radius:6px; padding:10px; font-size:0.75rem; color:#444; line-height:1.4; text-align:center; }
    .grid-cell span { font-size:1.1rem; display:block; margin-bottom:4px; }

    /* ─── Chain ─── */
    .chain { display:flex; flex-direction:column; align-items:flex-start; gap:0; width:200px; }
    .chain-item { display:flex; align-items:center; gap:10px; padding:8px 12px; border:1px solid #e0e0e0; border-radius:6px; width:100%; font-size:0.78rem; color:#333; background:#fafafa; }
    .chain-item.end { background:#1a1a1a; color:#fff; border-color:#1a1a1a; }
    .chain-dot { width:8px; height:8px; background:#bbb; border-radius:50%; flex-shrink:0; }
    .chain-dot.dark { background:#fff; }
    .chain-line { width:2px; height:14px; background:#ddd; margin-left:15px; }

    /* ─── Cycle ─── */
    .cycle { text-align:center; width:220px; }
    .cycle-ring { width:44px; height:44px; border:3px solid #1a1a1a; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.1rem; margin:0 auto 12px; }
    .cycle-items { display:flex; flex-direction:column; gap:0; }
    .cycle-item { display:flex; align-items:center; gap:10px; padding:9px 14px; font-size:0.8rem; color:#333; }
    .cycle-item:not(:last-child) { border-bottom:1px dashed #e8e8e8; }
    .cycle-arrow { font-size:0.9rem; color:#bbb; }
"""

BASE_CSS = """
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
    section.opening p  { font-size: 1.5rem; color: #555; font-weight: 400; }
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
"""

JS = """
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
    if (e.key === 'ArrowLeft')  move(-1);
  });
"""


def esc(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def render_visual(visual: str, slide: dict) -> str:
    if visual == 'dial':
        return """<div>
          <div class="dial-track"><div class="dial-fill"></div><div class="dial-dot"></div></div>
          <div class="dial-labels"><span>Low</span><span>High</span></div>
          <div class="dial-caption">Risk moves along a spectrum —<br>it never reaches zero</div>
        </div>"""

    if visual == 'cost_ladder':
        return """<div>
          <div class="cost-ladder">
            <div><div class="cost-bar-fill" style="width:80px">Low defences</div></div>
            <div><div class="cost-bar-fill" style="width:130px">Medium defences</div></div>
            <div><div class="cost-bar-fill dark" style="width:190px">Strong defences</div></div>
          </div>
          <div class="cost-caption">Stronger defences raise<br>the cost of attack</div>
        </div>"""

    if visual == 'scenario_cards':
        bullets = slide.get('bullets', [])
        cards = bullets[:3] if bullets else ['Scenario A', 'Scenario B', 'Scenario C']
        html = '<div class="scenario-cards">'
        for b in cards:
            parts = b.split('—', 1)
            title = parts[0].strip()
            desc = parts[1].strip() if len(parts) > 1 else ''
            html += f'<div class="scenario-card"><span>{esc(title)}</span>{esc(desc)}</div>'
        html += '</div>'
        return html

    if visual == 'flow':
        bullets = slide.get('bullets', [])
        items = bullets[:3] if bullets else ['Step 1', 'Step 2', 'Result']
        html = '<div class="flow">'
        for i, item in enumerate(items):
            cls = 'flow-box highlight' if i == len(items) - 1 else 'flow-box'
            label = item.split('—')[0].strip()[:40]
            html += f'<div class="{cls}">{esc(label)}</div>'
            if i < len(items) - 1:
                html += '<div class="flow-arrow">↓</div>'
        html += '</div>'
        return html

    if visual == 'layers':
        bullets = slide.get('bullets', [])
        items = bullets[:3] if bullets else ['Layer 1', 'Layer 2', 'Result']
        labels = ['l1', 'l2', 'l3']
        html = '<div class="layers">'
        for i, item in enumerate(items[:3]):
            label = item.split('—')[0].strip()[:50]
            html += f'<div class="layer {labels[i]}">{esc(label)}</div>'
        html += '</div>'
        return html

    if visual == 'equation':
        bullets = slide.get('bullets', [])
        sub = ' &nbsp;·&nbsp; '.join([b.split('—')[0].strip()[:20] for b in bullets[:3]])
        return f"""<div class="equation">
          <div class="eq-box">Input / Risk</div>
          <span class="eq-arrow">↓</span>
          <div class="eq-box highlight">Financial Impact (€)</div>
          <div class="eq-sub">{sub}</div>
        </div>"""

    if visual == 'distribution':
        return """<div class="dist">
          <div class="dist-row"><div class="dist-label">Expected</div><div class="dist-bar" style="width:80px"></div></div>
          <div class="dist-row"><div class="dist-label">Bad year</div><div class="dist-bar" style="width:130px"></div></div>
          <div class="dist-row"><div class="dist-label">Worst case</div><div class="dist-bar" style="width:180px"></div></div>
          <div class="dist-caption">Financial loss →</div>
        </div>"""

    if visual == 'grid2x2':
        items = slide.get('bullets', [])[:4]
        html = '<div class="grid2x2">'
        for i, item in enumerate(items):
            html += f'<div class="grid-cell"><span>{"①②③④"[i]}</span>{esc(item[:40])}</div>'
        html += '</div>'
        return html

    if visual == 'chain':
        bullets = slide.get('bullets', [])
        items = bullets[:4] if bullets else ['Source', 'Definition', 'Context', 'Output']
        html = '<div class="chain">'
        for i, item in enumerate(items):
            cls = 'chain-item end' if i == len(items) - 1 else 'chain-item'
            dot_cls = 'chain-dot dark' if i == len(items) - 1 else 'chain-dot'
            label = item.split('—')[0].strip()[:40]
            html += f'<div class="{cls}"><div class="{dot_cls}"></div>{esc(label)}</div>'
            if i < len(items) - 1:
                html += '<div class="chain-line"></div>'
        html += '</div>'
        return html

    if visual == 'cycle':
        bullets = slide.get('bullets', [])
        items = [b.split('.')[0].strip()[:30] for b in bullets[:4]]
        html = '<div class="cycle"><div class="cycle-ring">↻</div><div class="cycle-items">'
        for item in items:
            html += f'<div class="cycle-item"><span class="cycle-arrow">→</span>{esc(item)}</div>'
        html += '</div></div>'
        return html

    return ''


def render_slide(slide: dict) -> str:
    stype = slide.get('type', 'principle')

    if stype == 'opening':
        title = esc(slide.get('title', ''))
        subtitle = esc(slide.get('subtitle', ''))
        return f'  <section class="opening">\n    <h1>{title}</h1>\n    <p>{subtitle}</p>\n  </section>\n'

    if stype == 'closing':
        quote = esc(slide.get('quote', ''))
        return f'  <section class="closing">\n    <blockquote>{quote}</blockquote>\n  </section>\n'

    if stype == 'summary':
        headline = esc(slide.get('headline', ''))
        items = slide.get('items', [])
        bullets_html = '\n      '.join(
            f'<li><strong>{esc(it["label"])}</strong> — {esc(it["text"])}</li>'
            for it in items
        )
        return (
            f'  <section class="summary">\n'
            f'    <h2>{headline}</h2>\n'
            f'    <div class="divider"></div>\n'
            f'    <ul>\n      {bullets_html}\n    </ul>\n'
            f'  </section>\n'
        )

    # principle
    label = esc(slide.get('label', ''))
    headline = esc(slide.get('headline', ''))
    intro_line = slide.get('intro_line')
    bullets = slide.get('bullets', [])
    visual = slide.get('visual', 'none')

    bullets_html = '\n          '.join(f'<li>{esc(b)}</li>' for b in bullets)
    visual_html = render_visual(visual, slide)

    text_block = (
        f'      <div class="slide-text">\n'
        f'        <div class="label">{label}</div>\n'
        f'        <h2>{headline}</h2>\n'
        f'        <div class="divider"></div>\n'
        + (f'        <p class="intro-line">{esc(intro_line)}</p>\n' if intro_line else '')
        + f'        <ul>\n          {bullets_html}\n        </ul>\n'
        f'      </div>\n'
    )

    if visual_html:
        visual_block = f'      <div class="slide-visual">\n        {visual_html}\n      </div>\n'
        return (
            f'  <section>\n'
            f'    <div class="slide-inner">\n'
            + text_block
            + visual_block
            + f'    </div>\n  </section>\n'
        )
    else:
        return (
            f'  <section>\n'
            + text_block.replace('      ', '    ')
            + f'  </section>\n'
        )


def build(input_path: str, output_path: str) -> None:
    data = json.loads(Path(input_path).read_text(encoding='utf-8'))
    title = data.get('title', 'Presentation')
    slides_html = '\n'.join(render_slide(s) for s in data.get('slides', []))

    # Mark first slide active
    slides_html = slides_html.replace('<section class="opening">', '<section class="opening active">', 1)
    if 'active' not in slides_html:
        slides_html = slides_html.replace('<section>', '<section class="active">', 1)

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{esc(title)}</title>
  <style>
{BASE_CSS}
{VISUAL_CSS}
  </style>
</head>
<body>

<div class="slides">
{slides_html}
</div>

<button class="nav-btn" id="btn-prev" onclick="move(-1)" disabled>← Prev</button>
<span class="counter" id="counter">1 / {len(data.get('slides', []))}</span>
<button class="nav-btn" id="btn-next" onclick="move(1)">Next →</button>

<script>
{JS}
</script>

</body>
</html>"""

    Path(output_path).write_text(html, encoding='utf-8')
    print(f"Wrote {output_path} ({Path(output_path).stat().st_size} bytes)")


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: build_slides.py <input.json> <output.html>")
        sys.exit(1)
    build(sys.argv[1], sys.argv[2])
