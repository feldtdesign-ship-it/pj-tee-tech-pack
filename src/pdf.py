"""The paper tech pack. build.py calls make_pdf_html() and prints the result to dist/PJ_Tee_Tech_Pack.pdf
with headless Chrome. Same data as the page (data.py, sizes.py, colourways.py) and the same 3D renders,
so the PDF and the viewer can't disagree. Layout follows Cowork's v1 PDF: tabloid landscape, 17 x 11 in.
"""
import html

e = lambda s: html.escape("" if s is None else str(s), quote=True)
TBC = '<span class="tbc">TBC</span>'
PH = '<span class="ph">Placeholder</span>'


def frac8(v):
    w = int(v); n = round((v - w) * 8)
    if not n: return str(w)
    g = 4 if n % 4 == 0 else 2 if n % 2 == 0 else 1
    return f"{w} {n // g}/{8 // g}"


CSS = """
@page{size:17in 11in;margin:0}
*{box-sizing:border-box;margin:0}
:root{--ink:#121212;--y:#F2C200;--cream:#F0EDE5;--paper:#FBFAF6;--line:#cfcbc2;--blue:#497CB5;--orange:#F26A1B;--muted:#5b5850;
  --h:Oswald,Impact,sans-serif;--b:Inter,Helvetica,Arial,sans-serif;--m:"IBM Plex Mono",Menlo,monospace}
html,body{background:#fff;color:var(--ink);font:13px/1.4 var(--b);-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:17in;height:11in;position:relative;overflow:hidden;page-break-after:always;padding:30px 34px 44px;display:flex;flex-direction:column;gap:14px}
.mono{font-family:var(--m);font-size:10px;letter-spacing:.16em;text-transform:uppercase}
.h{font-family:var(--h);font-weight:700;text-transform:uppercase;line-height:.95;margin:0}
.tbc{font-family:var(--m);font-size:10px;letter-spacing:.12em;color:var(--orange);font-weight:500}
.ph{display:inline-block;font-family:var(--m);font-size:8.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--orange);border:1px solid var(--orange);padding:1px 4px;margin-left:6px;vertical-align:1px}
.foot{position:absolute;left:34px;right:34px;bottom:16px;display:flex;justify-content:space-between;color:#8a867d}
.grid{background-color:#fff;background-image:linear-gradient(rgba(73,124,181,.13) 1px,transparent 1px),linear-gradient(90deg,rgba(73,124,181,.13) 1px,transparent 1px);background-size:22px 22px}
/* cover */
.cover{background:var(--ink);color:#fff;padding:80px 90px}
.cover img{width:640px;height:auto;margin-top:40px}
.cover .t{font-size:150px;margin-top:60px}.cover .t span{color:var(--y)}
.cover p{font-size:26px;max-width:1050px;margin-top:34px;color:#eee}
.cover .bar{position:absolute;left:0;right:0;bottom:90px;height:40px;background:var(--y)}
.cover .foot{color:#9a9a9a}
/* read me */
.readme{background:var(--y)}
.readme .big{font-size:110px;margin-top:40px}
.cols{display:grid;grid-template-columns:1fr 1fr 1fr;gap:54px;margin-top:70px}
.cols .mono{margin-bottom:14px}
.cols p{font-size:16px;margin-bottom:14px}
.toc div{display:flex;gap:16px;align-items:baseline;border-bottom:1px solid rgba(0,0,0,.35);padding:9px 0;font-size:16px}
.toc b{font:700 20px/1 var(--h);width:34px}
.link{background:var(--ink);color:var(--y);font:500 14px/1.3 var(--m);padding:12px 14px;margin:6px 0 10px;word-break:break-all}
/* sheet header */
.band{background:var(--ink);color:#fff;display:grid;grid-template-columns:auto 1fr 520px;gap:30px;align-items:center;padding:14px 26px;border-bottom:8px solid var(--y)}
.band img{height:70px}
.band .t{font-size:54px}.band .t span{color:var(--y)}
.band .sub{color:#bdbdbd;margin-top:8px;font-size:9.5px}
.meta{display:grid;grid-template-columns:1fr 1fr;gap:6px 28px;font-size:13px}
.meta div{border-bottom:1px solid #3a3a3a;padding-bottom:3px}
.meta b{display:block;font:500 8.5px/1.4 var(--m);letter-spacing:.18em;color:var(--y);text-transform:uppercase}
/* panels */
.row{display:flex;gap:14px;flex:1;min-height:0}
.panel{border:2px solid var(--ink);display:flex;flex-direction:column;min-height:0;background:#fff}
.bar{background:var(--y);display:flex;justify-content:space-between;align-items:baseline;padding:8px 12px;border-bottom:2px solid var(--ink)}
.bar.dark{background:var(--ink);color:var(--y)}
.bar .h{font-size:26px}.bar .mono{font-size:8.5px}
.cap{font-size:11.5px;color:var(--muted);font-style:italic;padding:6px 12px;border-bottom:1px solid var(--line)}
.shot{flex:1;min-height:0;display:flex;align-items:center;justify-content:center;position:relative}
.shot img{max-width:100%;max-height:100%;object-fit:contain}
.shot .lab{position:absolute;bottom:8px;left:0;right:0;text-align:center;color:var(--muted);font-size:9px}
.tba{font:700 40px/1 var(--h);color:#b9b5ab}
/* spec list */
.spec{width:390px;flex:none;background:var(--cream)}
.spec{overflow:hidden}
.spec .head{padding:8px 14px 4px}
.spec .nm{font-size:26px;margin-top:3px}
.spec .ln{border-left:5px solid var(--y);padding-left:10px;margin-top:6px;font-weight:600;font-size:11px}
.spec ol{list-style:none;padding:2px 14px 6px}
.spec li{display:grid;grid-template-columns:26px 1fr;gap:6px;padding:2.5px 0;border-bottom:1px solid var(--line)}
.spec .no{font:700 15px/1 var(--h);color:var(--blue)}
.spec .k{font:700 11px/1.1 var(--h);text-transform:uppercase}
.spec .v{font-size:9.5px;line-height:1.25}
/* printer rules */
.rules{background:var(--ink);color:#fff;display:grid;grid-template-columns:340px 1fr;gap:18px;align-items:center;padding:14px 22px}
.rules .h{color:var(--y);font-size:30px}.rules p{font-size:11px;color:#cfcfcf;margin-top:4px}
.pills{display:grid;grid-template-columns:repeat(6,1fr);gap:10px}
.pill{border:2px solid var(--y);border-radius:6px;padding:9px 6px;text-align:center}
.pill b{display:block;font:700 16px/1 var(--h);text-transform:uppercase;color:var(--y)}.pill span{font-size:10px;color:#cfcfcf}
/* tables */
table{border-collapse:collapse;width:100%}
th{font:500 8.5px/1.3 var(--m);letter-spacing:.14em;text-transform:uppercase;color:var(--muted);text-align:left;padding:6px 6px;border-bottom:2px solid var(--ink)}
td{padding:4px 6px;border-bottom:1px solid var(--line);font-size:11.5px;vertical-align:top}
td.k{font:700 12.5px/1.15 var(--h);text-transform:uppercase;white-space:nowrap}
td.n{font-family:var(--m);font-size:12px;text-align:center;white-space:nowrap}
th.n{text-align:center}
.pad{padding:12px 16px}
.note{font-size:11px;color:var(--muted);margin-top:8px}
.dec{border-left:5px solid var(--orange);padding-left:10px;margin-bottom:10px}
.dec b{font:700 14px/1.1 var(--h);text-transform:uppercase;display:block}.dec p{font-size:11px}
.art{flex:1;display:flex;align-items:center;justify-content:center;padding:14px}
.art img{max-width:100%;max-height:100%;border:1px solid var(--line);background:#fff}
/* colourways */
.cws{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;flex:1;min-height:0}
.cw{border:2px solid var(--ink);display:flex;flex-direction:column;min-height:0}
.cw .bar .h{font-size:22px}
.cw .pair{flex:1;min-height:0;display:grid;grid-template-rows:1fr .78fr}
.cw .pair div{display:flex;align-items:center;justify-content:center;min-height:0}
.cw .pair img{max-height:100%;max-width:100%}
.chips{padding:8px 10px;border-top:2px solid var(--ink);background:var(--cream)}
.chip{display:flex;align-items:center;gap:8px;font-size:11px;padding:2px 0}
.chip i{width:26px;height:16px;border:1px solid var(--ink);flex:none}
.chip em{font-style:normal;font-family:var(--m);font-size:10px;color:var(--muted);margin-left:auto}
.cw .ln{font-size:10.5px;font-style:italic;color:var(--muted);padding:6px 10px 8px}
/* measurements */
.pom td.n{width:62px}
.check td:first-child{width:22px}
.box{display:inline-block;width:13px;height:13px;border:1.5px solid var(--ink)}
.sign{display:grid;grid-template-columns:repeat(3,1fr);gap:26px;padding:34px 16px 16px}
.sign div{border-bottom:1.5px solid var(--ink);padding-top:30px;font:500 9.5px/1.4 var(--m);letter-spacing:.16em;text-transform:uppercase}
"""


def header(s, sheet, of, title, blank_line):
    return f"""<header class="band">
  <img src="SIG_CREAM" alt="">
  <div><div class="h t">Style {e(s['num'])} <span>{e(s['name'])}</span></div>
    <div class="mono sub">Tee tech pack v1.2 · sheet {sheet} of {of}, {e(title)} · existing blank · screen print</div></div>
  <div class="meta">
    <div><b>Style number</b>{TBC}</div><div><b>Pack</b>v1.2, {e(DATE)}</div>
    <div><b>Artist</b>PJ O'Rourke II</div><div><b>Approved by</b>{TBC}</div>
    <div><b>Blank</b>{blank_line}</div><div><b>2.0 viewer</b>see page 2</div>
  </div></header>"""


def shot(R, key, label=""):
    if key and key in R:
        return f'<div class="shot grid"><img src="{R[key]}" alt=""><div class="mono lab">{e(label)}</div></div>'
    return f'<div class="shot grid"><div class="tba">TBA</div><div class="mono lab">{e(label)}</div></div>'


def panel(title, tag, cap, body, extra=""):
    capd = f'<div class="cap">{cap}</div>' if cap else ""
    return f'<section class="panel" style="flex:1{extra}"><div class="bar"><div class="h">{e(title)}</div><div class="mono">{e(tag)}</div></div>{capd}{body}</section>'


def spec_col(s):
    items = "".join(f'<li><span class="no">{i+1:02d}</span><div><div class="k">{e(k)}</div><div class="v">{e(v) if v else TBC}</div></div></li>' for i, (k, v) in enumerate(s["spec"]))
    return f"""<section class="panel spec"><div class="bar dark"><div class="h">Spec</div><div class="mono">From the file, or TBC</div></div>
  <div class="head"><div class="mono">Style {e(s['num'])} · {e(s['kind'])}</div><div class="h nm">{e(s['name'])}</div><div class="ln">{e(s['line'])}</div></div>
  <ol>{items}</ol></section>"""


def rules_bar(rules):
    pills = "".join(f'<div class="pill"><b>{e(a)}</b><span>{e(b)}</span></div>' for a, b in rules)
    return f'<section class="rules"><div><div class="h">Rules for the printer</div><p>TBC means ask. Nothing on this sheet is a guess. If a field is empty, it is empty on purpose.</p></div><div class="pills">{pills}</div></section>'


def foot(left, n):
    return f'<div class="foot mono"><span>PJ O\'Rourke II / Tee tech pack v1.2 / {e(left)}</span><span>{n:02d}</span></div>'


def pom_table(fit, run, poms):
    heads = "".join(f'<th class="n">{z}</th>' for z in run)
    rows = []
    for p in poms:
        if p.startswith("Body length"):
            cells = "".join(f'<td class="n">{frac8(v)}</td>' for v in fit["length"])
        elif p.startswith("Chest"):
            cells = "".join(f'<td class="n">{frac8(v)}</td>' for v in fit["chest"])
        else:
            cells = f'<td class="n" colspan="{len(run)}">{TBC}</td>'
        rows.append(f'<tr><td class="k">{e(p)}</td>{cells}<td class="n">{TBC}</td></tr>')
    return f"""<table class="pom"><tr><th>Measurement (in, laid flat)</th>{heads}<th class="n">Tol +/-</th></tr>{''.join(rows)}</table>
<div class="note">{PH} {e(fit['label'])}: {e(fit['blank'])}, published measurement report ({e(fit['source'])}). It lists chest and length only. PJ's blank is TBC: swap these when it is confirmed.</div>"""


def make_pdf_html(styles, rules, poms, size_sets, run, colourways, cw_source, R, site, date):
    global DATE
    DATE = date
    blank_line = "Placeholder: B+C 3010 / 6110"
    pages = []
    n = 1
    # 1 cover
    pages.append(f"""<div class="page cover"><div class="mono">Production / graphic tees / tech pack</div>
  <img src="SIG_CREAM" alt=""><div class="h t">Tee <span>Tech Pack</span></div>
  <p>Two styles. One drawn, one waiting. Every number came from a file or it says TBC. Sizes are placeholders from Bella+Canvas until PJ's blank is confirmed.</p>
  <div class="bar"></div><div class="foot mono"><span>PJ O'Rourke II / New York</span><span>Tech pack v1.2 / {e(date)}</span></div></div>""")
    # contents
    toc, p = [], 3
    for s in styles:
        sheets = [("the turnaround", 1), ("print and placement", 1)] + ([("colourways", 1)] if s["art"] else []) + [("measurements, finishing, sign off", 1)]
        for t, _ in sheets:
            toc.append((p, f"Style {s['num']} {s['name']}: {t}")); p += 1
    tocs = "".join(f'<div><b>{pg:02d}</b>{e(t)}</div>' for pg, t in toc)
    n = 2
    pages.append(f"""<div class="page readme"><div class="mono">Read me / how this pack works</div>
  <div class="h big">If it says TBC, ask.<br>Don't guess.</div>
  <div class="cols">
    <div><div class="mono">The rules</div>
      <p><b>Every value came from a file, or it says TBC.</b> The art facts are read straight from PJ's Illustrator file. Everything else waits for the blank maker, the printer, or PJ.</p>
      <p><b>Print from the vector.</b> The pictures in this pack are for reference. Films come from the .ai.</p>
      <p><b>His line stays his line.</b> No cleanup, no redraws, no smoothing. The signature is his real signature file.</p>
      <p><b>PJ signs every strike-off.</b> Nothing runs without the three signatures on the last sheet of each style.</p></div>
    <div class="toc"><div class="mono">Contents</div>{tocs}</div>
    <div><div class="mono">The 2.0 version</div>
      <p>Same pack, in 3D. Spin the tee, switch Unisex / Women's and XS to 3XL, try the colourways, tap a number to jump to its spec line.</p>
      <div class="link">{e(site)}</div>
      <p style="font-size:12px">The 3D tees are stand-ins sized to Bella+Canvas 3010 (unisex) and 6110 (women's), chest and length only, until PJ's blank is confirmed. This PDF is built from the same data and renders as the page.</p></div>
  </div>{foot('Read me', n)}</div>""")
    n = 3
    for s in styles:
        art = s["art"]
        pre = s["key"]
        of = 4 if art else 3
        # sheet 1: turnaround
        if art:
            panels = (panel("Front", "3D render · unisex M", "The side the factory prints. Starting placement shown, numbers TBC.", shot(R, f"{pre}_front", "Facing you"))
                      + panel("Back", "3D render · unisex M", "PJ's real signature, center back neck.", shot(R, f"{pre}_back", "Facing away"))
                      + panel("3/4 vanity", "3D render", "For the humans. Not a spec view.", shot(R, f"{pre}_q", "3/4"))
                      + panel("Women's", "3D render · women's M", "Same print on the women's tee. 9 in wide on every size.", shot(R, f"{pre}_w_front", "Facing you")))
        else:
            panels = (panel("Front", "3D render", "Art TBA. Placement TBC.", shot(R, f"{pre}_front", "Facing you"))
                      + panel("Back", "3D render", "Signature: TBC.", shot(R, f"{pre}_back", "Facing away"))
                      + panel("3/4 vanity", "3D", "Drop the art into the 2.0 viewer.", shot(R, None, "3/4"))
                      + panel("Women's", "3D", "When the art lands.", shot(R, None, "")))
        pages.append(f'<div class="page">{header(s, 1, of, "the turnaround", blank_line)}<div class="row">{panels}{spec_col(s)}</div>{rules_bar(rules)}{foot("Style " + s["num"] + " " + s["name"], n)}</div>')
        n += 1
        # sheet 2: print and placement
        inks = "".join(f'<tr><td class="k">{e(a)}</td><td>{e(b) if b else TBC}</td><td>{e(c) if c else TBC}</td><td class="n">{TBC}</td><td class="n">{TBC}</td></tr>' for a, b, c in s["inks"])
        facts = "".join(f'<tr><td class="k">{e(a)}</td><td>{e(b) if b else TBC}</td></tr>' for a, b in s["art_facts"])
        decs = "".join(f'<div class="dec"><b>{e(a)}</b><p>{e(b)}</p></div>' for a, b in s["decisions"]) or '<p class="note">None yet. Add them when the art lands.</p>'
        art_body = '<div class="art grid"><img src="ART_INK" alt=""></div><div class="cap">Artboard 9 × 12 in, straight from the .ai. Print from the .ai, never from this picture.</div>' if art else '<div class="art grid"><div class="tba">Art TBA</div></div>'
        backs = (panel("Women's back", "3D render · women's M", "Signature at the back neck on the women's tee.", shot(R, f"{pre}_w_back", "Facing away")) if art else panel("Back", "3D", "Signature: TBC.", shot(R, None, "")))
        pages.append(f"""<div class="page">{header(s, 2, of, "print and placement", blank_line)}<div class="row">
  {panel("Print at size", "The art", "", art_body)}
  {backs}
  <div style="flex:1.55;display:flex;flex-direction:column;gap:14px;min-height:0">
    <section class="panel"><div class="bar dark"><div class="h">Inks</div><div class="mono">Screen print</div></div><div class="pad"><table><tr><th>Ink</th><th>What</th><th>Note</th><th class="n">Pantone</th><th class="n">Mesh</th></tr>{inks}</table>
      {'<div class="note">Colourways (next sheet) set the line and signature colours. Hex are starting points; Pantone TBC.</div>' if art else ''}</div></section>
    <section class="panel"><div class="bar dark"><div class="h">Art file</div><div class="mono">Read from the file</div></div><div class="pad"><table>{facts}</table></div></section>
    <section class="panel" style="flex:1"><div class="bar"><div class="h">Open decisions</div><div class="mono">Settle before films</div></div><div class="pad">{decs}</div></section>
  </div></div>{foot("Style " + s["num"] + " " + s["name"], n)}</div>""")
        n += 1
        # sheet 3: colourways (styles with art only)
        if art:
            cards = []
            for c in colourways:
                chips = "".join(f'<div class="chip"><i style="background:{h}"></i>{k}: {e(nm)}<em>{h}</em></div>' for k, (nm, h) in [("Shirt", c["shirt"]), ("Line", c["print"]), ("Signature", c["accent"])])
                cards.append(f"""<section class="cw"><div class="bar"><div class="h">{e(c['num'])} {e(c['name'])}</div><div class="mono">{e(c['tag'])}</div></div>
  <div class="pair grid"><div><img src="{R.get(f"cw_{c['key']}_front", '')}" alt=""></div><div><img src="{R.get(f"cw_{c['key']}_back", '')}" alt=""></div></div>
  <div class="chips">{chips}</div><div class="ln">{e(c['line'])}</div></section>""")
            pages.append(f"""<div class="page">{header(s, 3, of, "colourways", blank_line)}
  <div class="cws">{''.join(cards)}</div>
  <div class="note" style="font-size:12px"><b>How a colourway lands on this tee:</b> shirt = body colour, print = front line (white fills left open so the shirt shows), accent = PJ's signature at the back neck. Classic keeps white fills and a black signature. Source: {e(cw_source)}</div>
  {foot("Style " + s["num"] + " " + s["name"], n)}</div>""")
            n += 1
        # sheet 4: measurements, finishing, sign off
        tables = "".join(f'<div class="h" style="font-size:20px;margin:10px 0 4px">{e(f["label"])} · {e(f["blank"])}</div>{pom_table(f, run, poms)}' for f in size_sets.values())
        place = "".join(f'<tr><td class="k">{e(k)}</td><td class="n">{e(v)}</td><td>{e(nt)}</td></tr>' for k, v, nt in [
            ("Print width", "9 in", "Viewer starting point (artboard at 100%). Same on every size until screen tiers are set."),
            ("Print down from collar", "3 in", "Starting point, center front from the collar seam."),
            ("Signature width", "3 1/2 in", "Starting point."),
            ("Signature down from back collar", "1 1/2 in", "Starting point.")]) if art else f'<tr><td class="k">Print and signature</td><td class="n">{TBC}</td><td>When the art lands.</td></tr>'
        checks = "".join(f'<tr><td><span class="box"></span></td><td><b>{e(a)}</b> {e(b)} {TBC}</td></tr>' for a, b in [
            ("Neck label", "Printed or woven. Content and placement."), ("Hang tag", "Artwork, string, placement."), ("Folding", "Fold method and size."),
            ("Poly bag", "Size, warning text, sticker."), ("Carton", "Units per carton, marks."), ("Care and content", "From the blank maker.")])
        proof = "".join(f'<tr><td class="k">R{i}</td><td></td><td></td><td></td><td></td></tr>' for i in (1, 2, 3))
        pages.append(f"""<div class="page">{header(s, of, of, "measurements, finishing, sign off", blank_line)}<div class="row">
  <section class="panel" style="flex:1.35"><div class="bar"><div class="h">Points of measure</div><div class="mono">From the blank maker's spec sheet</div></div><div class="pad">{tables}
    <div class="note">Tolerances TBC with the printer. Screen sizes by size range: TBC.</div></div></section>
  <div style="flex:1;display:flex;flex-direction:column;gap:14px;min-height:0">
    <section class="panel"><div class="bar"><div class="h">Placement</div><div class="mono">Viewer starting points</div></div><div class="pad"><table><tr><th>Placement</th><th class="n">Start</th><th>Note</th></tr>{place}</table></div></section>
    <section class="panel"><div class="bar dark"><div class="h">Labels and packaging</div><div class="mono">Check when confirmed</div></div><div class="pad"><table class="check">{checks}</table></div></section>
    <section class="panel" style="flex:1"><div class="bar"><div class="h">Proof log</div><div class="mono">Strike-offs and samples</div></div><div class="pad"><table><tr><th>Round</th><th>Date</th><th>From</th><th>OK?</th><th>Notes</th></tr>{proof}</table></div></section>
    <section class="panel"><div class="bar dark"><div class="h">Sign off</div><div class="mono">Nothing runs without all three</div></div><div class="sign"><div>PJ O'Rourke II</div><div>Michael, Feldt Design</div><div>Printer</div></div></section>
  </div></div>{foot("Style " + s["num"] + " " + s["name"], n)}</div>""")
        n += 1
    return f"""<!doctype html><html><head><meta charset="utf-8"><title>PJ O'Rourke II Tee Tech Pack v1.2</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;700&family=Inter:wght@400;600;700&family=IBM+Plex+Mono:wght@400;500&display=block">
<style>{CSS}</style></head><body>{''.join(pages)}</body></html>"""
