"""Artwork per style (keys match data.py STYLES). The page, the PDF renders and the PDF 'print at size' read from here.
Adding a design: run tools/split_art.py on its .ai, add an entry here, fill its style in data.py, build.

  ink, fill    layers made by tools/split_art.py (alpha PNGs in assets/)
  start_w      starting print width on the tee, inches (TBC until PJ signs off)
  note         caption for the PDF's 'print at size' panel
  place        starting placement (3.0): "front" = one print, center front
                                         "chest_back" = small print over the left chest + big print center back
               Any design can be switched to either on the page; this is only where it opens.
  chest_w, back_w   starting widths for "chest_back", inches
  one_colour   True = one ink, knocked out: the shirt shows through everywhere the ink isn't (no white fills)
"""
ARTWORK = {
    "s01": {"ink": "art01_ink.png", "fill": "art01_fill.png", "start_w": 9,
            "note": "Artboard 9 × 12 in, straight from the .ai. Print from the .ai, never from this picture."},
    "s02": {"ink": "art02_ink.png", "fill": "art02_fill.png", "start_w": 12,
            "note": "Art is 62 × 70 in in the .ai; starting print 12 in wide (about 12 × 13.6 in). Print from the .ai, never from this picture."},
    # New York Fuckery: one sheet (11 x 17 in) with the art at print size: a 10 1/8 in circle for the back and
    # two small ones (3 3/8 and 2 3/4 in) for the chest. art03 is the big circle, cut out with split_art.py --box.
    "s03": {"ink": "art03_ink.png", "fill": "art03_fill.png", "start_w": 10.125,
            "place": "chest_back", "chest_w": 3.375, "back_w": 10.125, "one_colour": True,
            "note": "The back circle, 10 1/8 in, at 100% from the file. The chest print is the same art at 3 3/8 in (the file also has a 2 3/4 in one). Print from the vector, never from this picture."},
}
