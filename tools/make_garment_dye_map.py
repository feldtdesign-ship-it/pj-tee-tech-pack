"""Make the garment-dye 'wash' map for each 3D base tee.

Garment dye (e.g. Shaka Wear SHGD, Comfort Colors) reads as:
  R  frosted edges: seams, hem, cuffs and collar come out paler where the dye washes out at the stitching
  G  fold ridges: raised folds fade lighter than the valleys
  B  cloudy mottling: patchy, uneven colour across the body

Input: the full-size fold-shadow (AO) bakes from blender/Shirts_fabric_bake.blend, saved in
       <PJ folder>/blender/fabric_bake/ao_<model>_2048.png. Pattern pieces are the non-black areas;
       their borders are the seams, hems, cuffs and collar.
Output: assets/tee_gd_wash_<model>.jpg (RGB as above, 1024 px). The page mixes the shirt colour toward a
        faded version of itself by R, G and B, only when Finish = Garment-dyed.

Run: python3 tools/make_garment_dye_map.py [model ...]   (default: all; a few seconds each)
"""
import pathlib
import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = pathlib.Path(__file__).resolve().parent.parent
BAKES = ROOT.parent / "blender" / "fabric_bake"
OUT = ROOT / "assets"
UV_IN_PER_UNIT = 48.0          # measured: ~0.0207 UV per inch on both base tees
SIZE = 2048

def wash(model, seed):
    ao = np.asarray(Image.open(BAKES / f"ao_{model}_2048.png").convert("L"), dtype=np.float32) / 255
    inside = ao > 0.02                                   # pattern pieces (bake margin/background is black)
    inside = ndimage.binary_opening(inside, iterations=2)
    px_per_in = SIZE / UV_IN_PER_UNIT
    # R: distance to the edge of each piece, in inches -> strong within ~0.35 in, gone by ~1.2 in
    d_in = ndimage.distance_transform_edt(inside) / px_per_in
    edge = np.clip(1 - (d_in - 0.12) / 1.0, 0, 1) ** 1.6
    # G: fold ridges = locally brighter than the surroundings in the AO bake
    # blur only within the pieces (normalised), or the black background reads as a "ridge" at every border
    m = inside.astype(np.float32)
    blur = ndimage.gaussian_filter(ao * m, px_per_in * 1.2) / np.maximum(ndimage.gaussian_filter(m, px_per_in * 1.2), 1e-3)
    ridge = np.clip((ao - blur) * 9, 0, 1) * m
    ridge = ndimage.gaussian_filter(ridge, px_per_in * 0.12)
    # B: cloudy mottling, two scales (~3 in patches and ~0.8 in blotches), centred on 0.5
    rng = np.random.default_rng(seed)
    def cloud(scale_in):
        n = rng.random((SIZE, SIZE)).astype(np.float32)
        n = ndimage.gaussian_filter(n, px_per_in * scale_in, mode="wrap")
        return (n - n.mean()) / (n.std() + 1e-6)
    mottle = np.clip(0.5 + 0.16 * cloud(3.0) + 0.08 * cloud(0.8), 0, 1)
    rgb = np.stack([edge, ridge, mottle], -1)
    rgb[~inside] = [0, 0, 0.5]
    img = Image.fromarray((rgb * 255).astype(np.uint8)).resize((1024, 1024), Image.LANCZOS)
    p = OUT / f"tee_gd_wash_{model}.jpg"
    img.save(p, quality=88)
    return p

if __name__ == "__main__":
    import sys
    models = sys.argv[1:] or ["unisex", "womens", "boxy"]
    for i, m in enumerate(models):
        p = wash(m, 7 + i)
        print(p.name, p.stat().st_size // 1024, "KB")
