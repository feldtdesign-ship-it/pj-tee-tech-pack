"""Blank profiles. One entry per blank; the site's Blank picker and the PDF read from here.
Adding a blank = adding an entry (plus a colour list and sizes). No page code changes.

Fields
  label, maker, style, name   what it is
  status       "confirmed" (PJ prints on it) or "placeholder" (stand-in until a real blank is picked)
  fit          "unisex" or "womens": which Fit switch it appears under
  model        which 3D base tee it uses (see MODELS)
  finish       "garment_dyed" or "standard": the default Finish on the site
  source       where the numbers came from (URL)
  fabric, fit_note, construction, note      spec text for the PDF
  run          sizes it comes in
  chest        flat chest, 1 in below armhole, inches, per size
  length       body length from HPS, inches, per size
  sleeve       published sleeve length, inches, per size (or None). Measuring method TBC.
  colours      [name, Pantone, hex] per colour. Hex = average of the maker's swatch image (approximate).
"""

MODELS = {
    # 3D base tees exported from blender/Shirts.blend. Measured in Blender: chest = half the distance
    # around the body just below the armhole; length = top of collar to hem; drops from the top of collar.
    "unisex": {"glb": "tee_viewer_model_v1.glb", "shade": "tee_fabric_shade_unisex.jpg", "wash": "tee_gd_wash_unisex.jpg",
               "base": {"chest": 20.81, "length": 29.0, "front_drop": 1.69, "back_drop": 0.0, "W": 23.5, "H": 29.0}},
    "womens": {"glb": "tee_viewer_model_womens_v1.glb", "shade": "tee_fabric_shade_womens.jpg", "wash": "tee_gd_wash_womens.jpg",
               "base": {"chest": 15.7, "length": 22.98, "front_drop": 2.35, "back_drop": 0.06, "W": 16.73, "H": 22.98}},
    # Boxy / structured (SHGD, 7.5 oz): the unisex tee reshaped by tools/blender_boxy_tee.py. v2 (2026-09-29, Michael's
    # notes): natural chest, straight sides widening toward the hem, small shoulder drop, flat sleeves (no fullness:
    # it's a bust form), folds smoothed for a heavy knit. v1 files kept (tee_viewer_model_boxy_v1.glb,
    # tee_fabric_shade_boxy.jpg, tee_gd_wash_boxy.jpg). Measured by tools/blender_export_viewer_tee.py.
    # normal = strength of the crease texture (1 = as the stand-in tee has it); a heavy knit creases less.
    "boxy": {"glb": "tee_viewer_model_boxy_v2.glb", "shade": "tee_fabric_shade_boxy_v2.jpg", "wash": "tee_gd_wash_boxy_v2.jpg",
             "normal": 0.35,
             "base": {"chest": 13.03, "length": 17.9, "front_drop": 1.05, "back_drop": 0.0, "W": 15.79, "H": 17.9}},
}

BLANKS = {
    "shaka_shgd": {
        "label": "Shaka Wear SHGD", "maker": "Shaka Wear", "style": "SHGD",
        "name": "Unisex Max Heavyweight Garment-Dyed Tee",
        "status": "confirmed", "fit": "unisex", "finish": "garment_dyed",
        # Shape: the Bella tee, in SHGD sizes, colours and the garment-dyed look (Michael, 2026-09-29). Boxy models kept, unused.
        "model": "unisex",
        "source": "https://www.ssactivewear.com/p/shaka_wear/shgd",
        "fabric": "7.5 oz./yd², 100% USA cotton, 16 singles. 3.5% Lycra ribbing.",
        "fit_note": "Slightly oversized fit.",
        "construction": "Garment-dyed for a retro vintage look. Densely knit for clean printing. Shoulder-to-shoulder neck tape. "
                        "Double-needle stitching throughout. Reinforced seams. Satin label.",
        "note": "Maker's note: each garment is uniquely crafted and will vary in color, design, and spec. OEKO-TEX certified facility.",
        "run": ["XS", "S", "M", "L", "XL", "2XL", "3XL", "4XL", "5XL"],
        "chest": [17.5, 18.5, 20.5, 22.5, 24.5, 26.5, 28, 30, 32],
        "length": [26.5, 29, 30, 31, 31.5, 33, 35, 37, 39],
        "sleeve": [16, 17, 18.25, 20, 21.25, 22.5, 23.5, 24.5, 25.5],
        "colours": [
            ["White", "WHITE", "#E9E9E9"], ["Black", "BLACK 6 C", "#262626"], ["Cement", "2333 C", "#B0B0B0"],
            ["Cherry Tomato", "2035 C", "#FC3532"], ["Clay Red", "1955 C", "#ED617C"], ["Cream", "7506 C", "#F2DFC0"],
            ["Midnight Navy", "289 C", "#304766"], ["Mocha", "17-1230", "#76514B"], ["Moss", "3435 C", "#4C605E"],
            ["Mustard", "7405 C", "#FAD49D"], ["Oatmeal", "7529 C", "#DAC7BA"], ["Pastel Purple", "264 C", "#EDD0EF"],
            ["Peach", "805 C", "#FEA580"], ["Powder Blue", "317 C", "#DEF4F2"], ["Royal", "287 C", "#015DD1"],
            ["Shadow", "419 C", "#575757"], ["Washed Denim", "2138 C", "#7797BE"], ["Wine", "19-3921", "#683E4C"],
        ],
    },
    "bc_3010": {
        "label": "Bella+Canvas 3010", "maker": "Bella+Canvas", "style": "3010",
        "name": "Unisex 6 oz Heavyweight Tee",
        "status": "placeholder", "fit": "unisex", "model": "unisex", "finish": "standard",
        "source": "https://www.bellacanvas.com/spec/3010_specs.pdf",
        "fabric": "6.0 oz, 20 singles, Airlume combed and ring-spun cotton.", "fit_note": "", "construction": "", "note": "",
        "run": ["XS", "S", "M", "L", "XL", "2XL", "3XL"],
        "chest": [19.125, 20.125, 21.125, 23.125, 25.125, 27.125, 29.125],
        "length": [26.5, 27.5, 28.0, 29.0, 30.25, 31.75, 32.75],
        "sleeve": None, "colours": [],
    },
    "bc_6110": {
        "label": "Bella+Canvas 6110", "maker": "Bella+Canvas", "style": "6110",
        "name": "Women's 6 oz Heavyweight Tee",
        "status": "placeholder", "fit": "womens", "model": "womens", "finish": "standard",
        "source": "https://www.bellacanvas.com/spec/6110_specs.pdf",
        "fabric": "6.0 oz, Airlume combed and ring-spun cotton.", "fit_note": "Boxy, cropped.", "construction": "", "note": "",
        "run": ["XS", "S", "M", "L", "XL", "2XL", "3XL"],
        "chest": [18.25, 19.0, 20.5, 22.5, 24.5, 26.5, 28.5],
        "length": [22.25, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5],
        "sleeve": None, "colours": [],
    },
}

# Which blank each Fit switch opens on. Placeholders stay pickable until PJ confirms a women's blank.
DEFAULT_BLANK = {"unisex": "shaka_shgd", "womens": "bc_6110"}
