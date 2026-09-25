"""Size sets for the 3D tee. build.py reads this; the viewer stretches each base model to a size's chest and length.

PLACEHOLDER: PJ's blank is TBC. Numbers are Bella+Canvas's published Measurement Specification Reports
for their 6 oz heavyweight tees, the closest public match to a structured tee. They list chest and body
length only, so the 3D tee is true at those two points; sleeves, shoulder and neck stretch with it.

Units: inches, laid flat. Chest is measured 1 in below the armhole. Length is from the high point shoulder (HPS).

base = the viewer model as exported from blender/Shirts.blend, measured in Blender:
  chest  = half the distance around the body just below the armhole
  length = top of collar to hem
  front_drop / back_drop = top of collar down to the front / back neck seam at centre
  W, H   = model width (sleeve to sleeve) and height
"""

SIZE_RUN = ["XS", "S", "M", "L", "XL", "2XL", "3XL"]

SIZE_SETS = {
    "unisex": {
        "label": "Unisex",
        "blank": "Bella+Canvas 3010, Unisex 6 oz Heavyweight",
        "source": "https://www.bellacanvas.com/spec/3010_specs.pdf",
        "glb": "tee_viewer_model_v1.glb",
        "base": {"chest": 20.81, "length": 29.0, "front_drop": 1.69, "back_drop": 0.0, "W": 23.5, "H": 29.0},
        "chest": [19.125, 20.125, 21.125, 23.125, 25.125, 27.125, 29.125],
        "length": [26.5, 27.5, 28.0, 29.0, 30.25, 31.75, 32.75],
    },
    "womens": {
        "label": "Women's",
        "blank": "Bella+Canvas 6110, Women's 6 oz Heavyweight",
        "source": "https://www.bellacanvas.com/spec/6110_specs.pdf",
        "glb": "tee_viewer_model_womens_v1.glb",
        # Fitted women's model from Shirts.blend. The 6110 itself is boxy and cropped: size is right, silhouette is slimmer.
        "base": {"chest": 15.7, "length": 22.98, "front_drop": 2.35, "back_drop": 0.06, "W": 16.73, "H": 22.98},
        "chest": [18.25, 19.0, 20.5, 22.5, 24.5, 26.5, 28.5],
        "length": [22.25, 22.5, 23.5, 24.5, 25.5, 26.5, 27.5],
    },
}
