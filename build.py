"""Builds dist/index.html (+ dist/m/ models), the PDF, dist/og-card.png, and the root index.html from src/ and assets/.
Run: python3 build.py          (everything)
     python3 build.py --page   (page only: skips the card, renders and PDF, for quick checks; never push after this alone)"""
import json, base64, sys, pathlib, shutil, subprocess, tempfile, html, os
ROOT = pathlib.Path(__file__).parent
PAGE_ONLY = "--page" in sys.argv
# Link preview (unfurl card) for iMessage, Slack, etc. The image URL must be absolute.
SITE = "https://feldtdesign-ship-it.github.io/pj-tee-tech-pack/"
OG_TITLE = "PJ Tee Tech Pack 3.1 (Beta)"
OG_DESC = "Spin PJ O'Rourke II's graphic tees in 3D: every Shaka Wear colour, any ink, chest, back or front placement, and the print spec."
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
sys.path.insert(0, str(ROOT / "src"))
from data import STYLES, PRINTER_RULES
A = ROOT / "assets"
b64 = lambda p, m="image/png": f"data:{m};base64," + base64.b64encode((A / p).read_bytes()).decode()
t = (ROOT / "src/viewer_template.html").read_text()
t = t.replace("__DATA__", json.dumps({"styles": STYLES, "rules": PRINTER_RULES}))
# Tee models: exported from blender/Shirts.blend. Origin = top of collar, centred, 1 unit = 1 in.
# The viewer stretches each one to the chest + length of the chosen blank and size (src/blanks.py).
from blanks import BLANKS, MODELS, DEFAULT_BLANK
t = t.replace("__BLANKS__", json.dumps({"blanks": BLANKS, "defaults": DEFAULT_BLANK,
    "models": {k: {"base": dict(v["base"]), "normal": v.get("normal", 0.9)} for k, v in MODELS.items()}}))
from colourways import COLOURWAYS
# Views the PDF needs, photographed by the viewer's render mode (#render). Same code as the page, so they match.
from artwork import ARTWORK
# Views the PDF needs, for every style with art (and front/back for styles still waiting on art).
# Photographed by the viewer's render mode (#render), so they match the page.
SHOTS = []
for s_ in STYLES:
    k = s_["key"]
    if s_["art"]:
        SHOTS += [{"id": f"{k}_front", "cw": "classic", "st": {"style": k, "meas": True, "view": "front"}},
                  {"id": f"{k}_back", "cw": "classic", "st": {"style": k, "meas": True, "view": "back"}},
                  {"id": f"{k}_q", "cw": "classic", "st": {"style": k, "view": "q"}},
                  {"id": f"{k}_w_front", "cw": "classic", "st": {"style": k, "blank": DEFAULT_BLANK["womens"], "meas": True, "view": "front"}},
                  {"id": f"{k}_w_back", "cw": "classic", "st": {"style": k, "blank": DEFAULT_BLANK["womens"], "meas": True, "view": "back"}}]
        SHOTS += [{"id": f"{k}_cw_{c['key']}_{v}", "cw": c["key"], "st": {"style": k, "view": v}} for c in COLOURWAYS for v in ("front", "back")]
    else:
        SHOTS += [{"id": f"{k}_front", "cw": "classic", "st": {"style": k, "meas": True, "view": "front"}},
                  {"id": f"{k}_back", "cw": "classic", "st": {"style": k, "meas": True, "view": "back"}}]
from trims import TRIMS as _T
_hero = {"style": "s01", "noArt": True, "trimsAll": True, "pocket": True}
SHOTS += [{"id": "tag_front", "cw": "classic", "st": {**_hero, "view": "front"}},
          {"id": "tag_back", "cw": "classic", "st": {**_hero, "view": "back"}}]
SHOTS += [{"id": f"tag_{x['key']}", "cw": "classic", "focus": x["key"], "st": dict(_hero)} for x in _T]
t = t.replace("__SHOTS__", json.dumps(SHOTS))
t = t.replace("__COLOURWAYS__", json.dumps(COLOURWAYS))
# Small branding (3.1): tag spots, pocket, label colours. PJ's logo line (from PJOR_Logo.ai via tools/render_pdf.swift).
from trims import TRIMS, POCKET, LABEL
t = t.replace("__TRIMS__", json.dumps({"trims": TRIMS, "pocket": POCKET, "label": LABEL}))
# Every 3D base model in src/blanks.py MODELS: tee (.glb), fold shading, garment-dye map. Embedded so the page is one file.
# Copied to dist/m/ and loaded on demand by the page (only the models a blank needs), so the page stays light.
(ROOT / "dist/m").mkdir(parents=True, exist_ok=True)
shutil.copy2(ROOT / "tools/qc.js", ROOT / "dist/qc.js")
shutil.copy2(A / "pjor_logo_line.png", ROOT / "dist/m/pjor_logo_line.png")   # QC helpers, loaded only with #qc
for a in ARTWORK.values():
    for f in (a["ink"], a["fill"]): shutil.copy2(A / f, ROOT / "dist/m" / f)
t = t.replace("__ART__", json.dumps({k: {"ink": "m/" + a["ink"], "fill": "m/" + a["fill"], "start_w": a["start_w"], "place": a.get("place", "front"),
    "chest_w": a.get("chest_w"), "back_w": a.get("back_w"), "one_colour": a.get("one_colour", False)} for k, a in ARTWORK.items()}))
for v in MODELS.values():
    for f in (v["glb"], v["shade"], v["wash"]): shutil.copy2(A / f, ROOT / "dist/m" / f)
t = t.replace("__TEE_GLB__", json.dumps({k: "m/" + v["glb"] for k, v in MODELS.items()}))
t = t.replace("__TEE_SHADE__", json.dumps({k: "m/" + v["shade"] for k, v in MODELS.items()}))
t = t.replace("__TEE_WASH__", json.dumps({k: "m/" + v["wash"] for k, v in MODELS.items()}))
t = t.replace("__SIGINK__", b64("PJ_Signature_ink_transparent.png")).replace("__SIG__", b64("PJ_Signature_cream_transparent.png"))
(ROOT / "dist").mkdir(exist_ok=True)

# Unfurl card: render src/og_card_template.html to a 1200x630 PNG with headless Chrome.
card = ROOT / "dist/og-card.png"
c = (ROOT / "src/og_card_template.html").read_text()
c = c.replace("__SIG__", b64("PJ_Signature_cream_transparent.png"))
if PAGE_ONLY:
    print("dist/og-card.png skipped (--page)")
elif pathlib.Path(CHROME).exists() or shutil.which(CHROME):
    card.unlink(missing_ok=True)
    with tempfile.TemporaryDirectory() as d:
        (pathlib.Path(d) / "card.html").write_text(c)
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                        "--virtual-time-budget=6000", "--window-size=1200,630", f"--screenshot={card}",
                        (pathlib.Path(d) / "card.html").as_uri()], capture_output=True, timeout=90)
    print("dist/og-card.png", "ok" if card.exists() else "FAILED")
else:
    print("dist/og-card.png skipped: Chrome not found (set CHROME=/path/to/chrome). Keeping the old card if there is one.")

e = lambda s: html.escape(s, quote=True)
og = "\n".join([
    f'<meta name="description" content="{e(OG_DESC)}">',
    f'<meta property="og:type" content="website">',
    f'<meta property="og:site_name" content="PJ O\'Rourke II">',
    f'<meta property="og:title" content="{e(OG_TITLE)}">',
    f'<meta property="og:description" content="{e(OG_DESC)}">',
    f'<meta property="og:url" content="{SITE}">',
    f'<meta property="og:image" content="{SITE}dist/og-card.png">',
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    f'<meta property="og:image:alt" content="{e(OG_TITLE)}: PJ O\'Rourke II signature">',
    '<meta name="twitter:card" content="summary_large_image">',
    f'<meta name="twitter:title" content="{e(OG_TITLE)}">',
    f'<meta name="twitter:description" content="{e(OG_DESC)}">',
    f'<meta name="twitter:image" content="{SITE}dist/og-card.png">',
])
t = t.replace("__OG__", og)
(ROOT / "dist/index.html").write_text(t)
print("dist/index.html", round(len(t) / 1e6, 2), "MB")

# ---------- renders for the PDF ----------
# Serve dist/ on a local port, open the page in headless Chrome with #render, and wait for the page
# to POST its pictures back. The page decides when it is done, so there is no timing guesswork.
def render_views(timeout=360):
    import http.server, socketserver, threading
    got = {}
    done = threading.Event()
    class H(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k): super().__init__(*a, directory=str(ROOT / "dist"), **k)
        def log_message(self, *a): pass
        def do_POST(self):
            if self.path == "/__renders":
                got.update(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
                self.send_response(204); self.end_headers(); done.set()
    srv = socketserver.ThreadingTCPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_address[1]}/index.html#render"
    with tempfile.TemporaryDirectory() as prof:
        ch = subprocess.Popen([CHROME, "--headless=new", "--use-angle=swiftshader", "--enable-unsafe-swiftshader",
                               "--hide-scrollbars", f"--user-data-dir={prof}", "--window-size=1200,900", url],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            ok = done.wait(timeout)
        finally:
            ch.terminate()
            try: ch.wait(10)
            except subprocess.TimeoutExpired: ch.kill()
            srv.shutdown()
    return got if ok else None

RENDERS = render_views() if not PAGE_ONLY and (pathlib.Path(CHROME).exists() or shutil.which(CHROME)) else None
print("renders:", "skipped (--page)" if PAGE_ONLY else len(RENDERS) if RENDERS else "FAILED")
# Tag heroes as image files too, to study each position (dist/heroes/tag_*.png)
if RENDERS:
    (ROOT / "dist/heroes").mkdir(exist_ok=True)
    for k, v in RENDERS.items():
        if k.startswith("tag_"): (ROOT / "dist/heroes" / f"{k}.png").write_bytes(base64.b64decode(v.split(",", 1)[1]))

# ---------- the paper tech pack ----------
# Same data and renders as the page, printed to PDF by headless Chrome. Skipped (old PDF kept) if renders failed.
PDF = ROOT / "dist/PJ_Tee_Tech_Pack.pdf"
if RENDERS:
    import datetime
    from pdf import make_pdf_html
    from colourways import SOURCE as CW_SOURCE
    from data import SIZE_POMS
    ph = make_pdf_html(STYLES, PRINTER_RULES, SIZE_POMS, BLANKS, DEFAULT_BLANK, COLOURWAYS, CW_SOURCE, RENDERS, SITE, ARTWORK,
                       datetime.date.today().strftime("%b %-d, %Y"), trims=__import__("trims").__dict__)
    ph = ph.replace("SIG_CREAM", b64("PJ_Signature_cream_transparent.png"))
    for k, a in ARTWORK.items(): ph = ph.replace(f"ART_INK_{k}", b64(a["ink"]))
    import numpy as _np; from PIL import Image as _Im; import io as _io   # logo line in white for the dark label panel
    _lg = _np.asarray(_Im.open(A / "pjor_logo_line.png")).copy(); _lg[..., :3] = 247; _bf = _io.BytesIO(); _Im.fromarray(_lg).save(_bf, "PNG")
    ph = ph.replace("ART_LOGO", "data:image/png;base64," + base64.b64encode(_bf.getvalue()).decode())
    with tempfile.TemporaryDirectory() as d:
        src = pathlib.Path(d) / "pack.html"; src.write_text(ph)
        PDF.unlink(missing_ok=True)
        # Chrome's --print-to-pdf hangs on Chrome 153 (Mac), so print over the DevTools connection (tools/print_pdf.mjs, needs Node 22+).
        r = subprocess.run(["node", str(ROOT / "tools/print_pdf.mjs"), CHROME, str(src), str(PDF)], capture_output=True, text=True, timeout=360)
        if r.returncode: print("PDF print error:", r.stderr.strip()[-300:])
    print("dist/PJ_Tee_Tech_Pack.pdf", f"{PDF.stat().st_size/1e6:.1f} MB" if PDF.exists() else "FAILED")
else:
    print("dist/PJ_Tee_Tech_Pack.pdf skipped: no renders. Keeping the old PDF if there is one.")

# Root page: the short link. Preview bots don't follow redirects, so it carries the same tags.
(ROOT / "index.html").write_text(f"""<!doctype html>
<meta charset="utf-8">
<title>{e(OG_TITLE)}</title>
{og}
<meta http-equiv="refresh" content="0; url=dist/">
<a href="dist/">Open the PJ Tee Tech Pack</a>
""")
print("index.html (short link)")
