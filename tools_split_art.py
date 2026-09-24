"""Splits a black and white Illustrator file into an ink layer and a white-fill layer for the viewer.
Run: python3 tools_split_art.py "path/to/art.ai" art02   (needs: pip install pymupdf pillow numpy)"""
import sys, numpy as np, pymupdf
from PIL import Image
doc = pymupdf.open(sys.argv[1]); pix = doc[0].get_pixmap(dpi=144, alpha=True)
a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 4).astype(float)
lum = a[..., :3].mean(-1) / 255; al = a[..., 3] / 255
for name, m in ((sys.argv[2] + "_ink.png", (1 - lum) * al), (sys.argv[2] + "_fill.png", lum * al)):
    out = np.zeros(m.shape + (4,), np.uint8); out[..., 3] = (m * 255).clip(0, 255).astype(np.uint8)
    Image.fromarray(out, "RGBA").save("assets/" + name, optimize=True); print("assets/" + name)
