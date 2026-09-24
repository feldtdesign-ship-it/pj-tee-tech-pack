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

## Add a style

1. Put the art through `python3 tools_split_art.py "art.ai" art02`.
2. Add the style to `STYLES` in `src/data.py`.
3. Load its layers in `build.py` and `ART` in the template.

## Copyright

© 2026 PJ O'Rourke II. All rights reserved. Public to view, not to reuse. See `LICENSE`.

## Styles

- 01 Citibike Gumbit: front print, signature at the back neck.
- 02 Next style: empty on purpose.
