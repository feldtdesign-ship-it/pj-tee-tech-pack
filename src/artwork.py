"""Artwork per style (keys match data.py STYLES). The page, the PDF renders and the PDF 'print at size' read from here.
Adding a design: run tools/split_art.py on its .ai, add an entry here, fill its style in data.py, build.

  ink, fill    layers made by tools/split_art.py (alpha PNGs in assets/)
  start_w      starting print width on the tee, inches (TBC until PJ signs off)
  note         caption for the PDF's 'print at size' panel
"""
ARTWORK = {
    "s01": {"ink": "art01_ink.png", "fill": "art01_fill.png", "start_w": 9,
            "note": "Artboard 9 × 12 in, straight from the .ai. Print from the .ai, never from this picture."},
    "s02": {"ink": "art02_ink.png", "fill": "art02_fill.png", "start_w": 12,
            "note": "Art is 62 × 70 in in the .ai; starting print 12 in wide (about 12 × 13.6 in). Print from the .ai, never from this picture."},
}
