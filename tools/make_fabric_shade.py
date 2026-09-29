"""Make the fabric shading image for a 3D base tee from its Blender fold-shadow (AO) bake.

Input:  <PJ folder>/blender/fabric_bake/ao_<model>_2048.png  (baked in blender/Shirts_fabric_bake.blend, scene Fabric Bake)
Output: assets/tee_fabric_shade_<model>.jpg (grey, 1024 px). The page multiplies colour and print by it.

Recipe (settled 2026-09-26):
  - hem and cuff turn-ups are two fabric layers ~1 mm apart and bake near black: lift anything under 172 to a soft band
  - add a fine cotton grain
  - downsize to 1024 (the shading is soft; half size barely shows and keeps the page light)

Run: python3 tools/make_fabric_shade.py boxy          (one or more model names)
     python3 tools/make_fabric_shade.py --all --force  (rebuild every model; grain is re-randomised)
Existing outputs are skipped unless --force, so the live images don't change by accident.
"""
import sys, pathlib
from PIL import Image, ImageFilter, ImageChops

ROOT = pathlib.Path(__file__).resolve().parent.parent
BAKES = ROOT.parent / "blender" / "fabric_bake"
OUT = ROOT / "assets"
FLOOR = 172

def make(model, force=False):
    out = OUT / f"tee_fabric_shade_{model}.jpg"
    if out.exists() and not force:
        print(f"{out.name} exists, skipped (use --force)"); return
    ao = Image.open(BAKES / f"ao_{model}_2048.png").convert("L")
    ao = ao.point(lambda v: v if v >= FLOOR else FLOOR - (FLOOR - v) * 0.12).resize((1024, 1024), Image.LANCZOS)
    n = Image.effect_noise((1024, 1024), 22).filter(ImageFilter.GaussianBlur(.5)).point(lambda v: int(128 + (v - 128) * .5))
    ImageChops.add(ao, n, scale=1, offset=-128).save(out, quality=84)
    print(out.name, out.stat().st_size // 1024, "KB")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    force = "--force" in sys.argv
    models = [p.stem[3:-5] for p in sorted(BAKES.glob("ao_*_2048.png"))] if "--all" in sys.argv else args
    for m in models: make(m, force)
