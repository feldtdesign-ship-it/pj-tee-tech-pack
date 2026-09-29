"""Turn a design's Illustrator file into the two layers the viewer and PDF use, and read its facts.

    python3 tools/split_art.py "path/to/design.ai" art02 [--width 2000]

Writes assets/<name>_ink.png (the line, as alpha: black = full ink, greys = partial) and assets/<name>_fill.png
(the white fills, as alpha), cropped to the file's ArtBox (the artwork itself, not the whole artboard), and prints
the file facts for data.py (artboard, art size, creator, dates, colour check).

No installs: an .ai saved with PDF compatibility is a PDF, and macOS `sips` renders it. (The older
tools_split_art.py needs pymupdf, which isn't installed on Michael's Mac.)
"""
import sys, re, os, subprocess, tempfile, shutil, datetime, pathlib
import numpy as np
from PIL import Image

ROOT = pathlib.Path(__file__).resolve().parent.parent

def boxes(pdf_bytes):
    out = {}
    for k in ("MediaBox", "ArtBox", "TrimBox"):
        m = re.search(rb"/" + k.encode() + rb"\s*\[\s*([-\d.\s]+)\]", pdf_bytes)
        if m: out[k] = [float(x) for x in m.group(1).split()]
    return out

def facts(path, b, bx, alpha, rgb):
    st = os.stat(path)
    mb, ab = bx["MediaBox"], bx.get("ArtBox", bx["MediaBox"])
    tool = re.search(rb"CreatorTool>([^<]+)<", b); mod = re.search(rb"xmp:ModifyDate>([^<]+)<", b)
    op = alpha > .04; px = rgb[op]
    sat = (px.max(1) - px.min(1)) if len(px) else np.array([0])
    greys = ((px.mean(1) > 40) & (px.mean(1) < 215)).mean() if len(px) else 0
    return {
        "file": os.path.basename(path),
        "saved": datetime.datetime.fromtimestamp(st.st_mtime).strftime("%b %-d, %Y"),
        "creator": tool.group(1).decode() if tool else None,
        "xmp_modified": mod.group(1).decode()[:10] if mod else None,
        "artboard_in": [round((mb[2] - mb[0]) / 72, 2), round((mb[3] - mb[1]) / 72, 2)],
        "art_in": [round((ab[2] - ab[0]) / 72, 2), round((ab[3] - ab[1]) / 72, 2)],
        "colour_pixels_share": round(float((sat > 40).mean()), 4),
        "grey_tone_share": round(float(greys), 3),
    }

def main(path, name, width=2000):
    b = open(path, "rb").read()
    assert b[:5] == b"%PDF-", "not a PDF-compatible .ai (save with 'Create PDF Compatible File' on)"
    bx = boxes(b); mb = bx["MediaBox"]; ab = bx.get("ArtBox", mb)
    full_w = int(round(width * (mb[2] - mb[0]) / (ab[2] - ab[0])))
    with tempfile.TemporaryDirectory() as d:
        pdf = os.path.join(d, "a.pdf"); shutil.copy(path, pdf)
        png = os.path.join(d, "a.png")
        subprocess.run(["sips", "-s", "format", "png", "--resampleWidth", str(full_w), pdf, "--out", png], check=True, capture_output=True)
        im = Image.open(png).convert("RGBA")
    s = im.width / (mb[2] - mb[0])
    box = (round((ab[0] - mb[0]) * s), round((mb[3] - ab[3]) * s), round((ab[2] - mb[0]) * s), round((mb[3] - ab[1]) * s))
    a = np.asarray(im.crop(box)).astype(float)
    lum = a[..., :3].mean(-1) / 255; al = a[..., 3] / 255
    for suffix, m in (("_ink.png", (1 - lum) * al), ("_fill.png", lum * al)):
        out = np.zeros(m.shape + (4,), np.uint8); out[..., 3] = (m * 255).clip(0, 255).astype(np.uint8)
        p = ROOT / "assets" / (name + suffix); Image.fromarray(out, "RGBA").save(p, optimize=True)
        print(p.relative_to(ROOT), f"{p.stat().st_size // 1024} KB", out.shape[1], "x", out.shape[0])
    f = facts(path, b, bx, al, a[..., :3]); print(f); return f

if __name__ == "__main__":
    w = int(sys.argv[sys.argv.index("--width") + 1]) if "--width" in sys.argv else 2000
    main(sys.argv[1], sys.argv[2], w)
