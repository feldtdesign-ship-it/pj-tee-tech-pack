"""Builds dist/index.html from src/ and assets/. Run: python3 build.py"""
import json, base64, sys, pathlib
ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT / "src"))
from data import STYLES, PRINTER_RULES
A = ROOT / "assets"
b64 = lambda p, m="image/png": f"data:{m};base64," + base64.b64encode((A / p).read_bytes()).decode()
t = (ROOT / "src/viewer_template.html").read_text()
t = t.replace("__DATA__", json.dumps({"styles": STYLES, "rules": PRINTER_RULES}))
# Tee model: exported from Blender, scaled to a PLACEHOLDER 29 in body length. Origin = top of back collar, 1 unit = 1 in.
t = t.replace("__MESH__", json.dumps({"bbox": {"minx": -11.75, "W": 23.5, "H": 29.0}, "frontDrop": 1.69, "backDrop": 0.0}))
t = t.replace("__GLB__", b64("tee_viewer_model_v1.glb", "model/gltf-binary"))
t = t.replace("__INK__", b64("art01_ink.png")).replace("__FILL__", b64("art01_fill.png"))
t = t.replace("__SIGINK__", b64("PJ_Signature_ink_transparent.png")).replace("__SIG__", b64("PJ_Signature_cream_transparent.png"))
(ROOT / "dist").mkdir(exist_ok=True)
(ROOT / "dist/index.html").write_text(t)
print("dist/index.html", round(len(t) / 1e6, 2), "MB")
