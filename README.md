# PJ Tee Tech Pack

Tech pack 2.0 for PJ O'Rourke II graphic tees. A single web page with a 3D tee you can spin, print and signature placement, colors, and the spec.

## Rule

Every value is read from a file or marked TBC. Nothing is guessed.

## What's here

- `src/data.py`: the spec. One source of truth for every style, field, ink, and open decision. Edit this, not the HTML.
- `src/viewer_template.html`: the page (Three.js r147 from jsDelivr).
- `assets/`: art layers, PJ's signature files, and the tee model.
- `build.py`: puts it all together into `dist/index.html` (one self-contained file).
- `tools_split_art.py`: turns a new black and white .ai into the two art layers.

## Build

```
python3 build.py
```

Then open `dist/index.html` in a browser.

The build also makes the link preview (unfurl card): `dist/og-card.png` from `src/og_card_template.html`, drawn with headless Google Chrome, plus the preview tags on `dist/index.html` and the short-link `index.html`. Title and description live at the top of `build.py`.

Live page: https://feldtdesign-ship-it.github.io/pj-tee-tech-pack/

## The tee model

- `assets/tee_viewer_model_v1.glb` was exported from the "Comfortable T-Shirt" in Blender (a BlenderKit model: check its license before public use).
- It's scaled to a **placeholder** 29 in body length until the blank spec lands. When it does, change the scale in Blender, re-export, and update `bbox` and `frontDrop` in `build.py`.
- Origin is the top of the back collar. 1 unit = 1 in.

## Sizes

- Pick **Unisex / Women's** and **XS to 3XL** above the 3D view. The tee stretches to that size's chest and body length.
- Numbers live in `src/sizes.py` (not `data.py`). They are a **placeholder**: Bella+Canvas 3010 (unisex) and 6110 (women's), 6 oz heavyweight, from their published measurement reports. Those list chest and length only, so sleeves, shoulder and neck stretch with the body.
- The two base tees come from `blender/Shirts.blend` in the main PJ folder (kept off GitHub): `assets/tee_viewer_model_v1.glb` (unisex) and `assets/tee_viewer_model_womens_v1.glb` (women's fitted, exported 2026-09-24). Export rules: 1 unit = 1 in, centred, top of collar at 0, front facing forward, about 40k points, normal map only.
- When PJ's real blank is confirmed, swap the numbers in `src/sizes.py` and rebuild.

## Add a style

1. Put the art through `python3 tools_split_art.py "art.ai" art02`.
2. Add the style to `STYLES` in `src/data.py`.
3. Load its layers in `build.py` and `ART` in the template.

## Copyright

© 2026 PJ O'Rourke II. All rights reserved. Public to view, not to reuse. See `LICENSE`.

## Styles

- 01 Citibike Gumbit: front print, signature at the back neck.
- 02 Next style: empty on purpose.
