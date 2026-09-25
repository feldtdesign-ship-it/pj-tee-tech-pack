"""Builds dist/index.html, dist/og-card.png, and the root index.html from src/ and assets/. Run: python3 build.py"""
import json, base64, sys, pathlib, shutil, subprocess, tempfile, html, os
ROOT = pathlib.Path(__file__).parent
# Link preview (unfurl card) for iMessage, Slack, etc. The image URL must be absolute.
SITE = "https://feldtdesign-ship-it.github.io/pj-tee-tech-pack/"
OG_TITLE = "PJ Tee Tech Pack 2.0 (Beta)"
OG_DESC = "Spin PJ O'Rourke II's graphic tee in 3D: print placement, colors, and the print spec."
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
sys.path.insert(0, str(ROOT / "src"))
from data import STYLES, PRINTER_RULES
A = ROOT / "assets"
b64 = lambda p, m="image/png": f"data:{m};base64," + base64.b64encode((A / p).read_bytes()).decode()
t = (ROOT / "src/viewer_template.html").read_text()
t = t.replace("__DATA__", json.dumps({"styles": STYLES, "rules": PRINTER_RULES}))
# Tee models: exported from blender/Shirts.blend. Origin = top of collar, centred, 1 unit = 1 in.
# The viewer stretches each one to the chest + length of the chosen size (src/sizes.py, PLACEHOLDER numbers).
from sizes import SIZE_SETS, SIZE_RUN
t = t.replace("__SIZES__", json.dumps({"run": SIZE_RUN, "sets": {k: {kk: vv for kk, vv in v.items() if kk != "glb"} for k, v in SIZE_SETS.items()}}))
t = t.replace("__GLB_UNISEX__", b64(SIZE_SETS["unisex"]["glb"], "model/gltf-binary"))
t = t.replace("__GLB_WOMENS__", b64(SIZE_SETS["womens"]["glb"], "model/gltf-binary"))
t = t.replace("__INK__", b64("art01_ink.png")).replace("__FILL__", b64("art01_fill.png"))
t = t.replace("__SIGINK__", b64("PJ_Signature_ink_transparent.png")).replace("__SIG__", b64("PJ_Signature_cream_transparent.png"))
(ROOT / "dist").mkdir(exist_ok=True)

# Unfurl card: render src/og_card_template.html to a 1200x630 PNG with headless Chrome.
card = ROOT / "dist/og-card.png"
c = (ROOT / "src/og_card_template.html").read_text()
c = c.replace("__SIG__", b64("PJ_Signature_cream_transparent.png"))
if pathlib.Path(CHROME).exists() or shutil.which(CHROME):
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

# Root page: the short link. Preview bots don't follow redirects, so it carries the same tags.
(ROOT / "index.html").write_text(f"""<!doctype html>
<meta charset="utf-8">
<title>{e(OG_TITLE)}</title>
{og}
<meta http-equiv="refresh" content="0; url=dist/">
<a href="dist/">Open the PJ Tee Tech Pack</a>
""")
print("index.html (short link)")
