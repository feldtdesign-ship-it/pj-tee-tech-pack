"""Colourways for the tee. build.py reads this for the viewer and the PDF.

Source: Claude outputs/PJ_Sydney_Colour_Sheet.pdf (draft). Its own note: hex codes are starting
points, picked by us. Match them to the real ink and fabric before anything gets printed.
Pantone refs stay TBC until then.

How a colourway lands on the Citibike Gumbit tee (Michael, 2026-09-24):
  shirt  = body colour
  print  = front line ink (fills left open, so the shirt shows through)
  accent = PJ's signature at the back neck
"Classic" is the pack's original look: cream shirt, black line, signature in the line ink.
"""

SOURCE = "PJ Sydney Colour Sheet (draft). Hex are starting points: match to real ink and fabric. Pantone TBC."

COLOURWAYS = [
    {"key": "classic", "num": "00", "name": "Classic", "tag": "The original",
     "shirt": ["Cream", "#F3EFE4"], "print": ["Black", "#121212"], "accent": ["Black", "#121212"],
     "fill": "print", "line": "Cream tee, black line, white fills. The pack as first drawn."},
    {"key": "harbour", "num": "01", "name": "Harbour", "tag": "Hero",
     "shirt": ["Navy", "#14264A"], "print": ["Vanilla", "#F1E9D2"], "accent": ["Red", "#D8322B"],
     "fill": "open", "line": "Navy, vanilla, one red. The tee equivalent of a good haircut."},
    {"key": "jacaranda", "num": "02", "name": "Jacaranda", "tag": "The loud one",
     "shirt": ["Lilac", "#B9A6D6"], "print": ["Plum", "#4A2A5E"], "accent": ["Butter", "#F2D36B"],
     "fill": "open", "line": "Lilac, plum, butter. Purple, but with a reason."},
    {"key": "bush", "num": "03", "name": "Bush", "tag": "Outdoor style",
     "shirt": ["Eucalypt", "#5B6B45"], "print": ["Sand", "#D9C7A0"], "accent": ["Rust", "#B5532F"],
     "fill": "open", "line": "Eucalypt, sand, rust."},
    {"key": "sandstone", "num": "04", "name": "Sandstone", "tag": "The bridge",
     "shirt": ["Caramel", "#B98B5E"], "print": ["Espresso", "#3B2A20"], "accent": ["Seafoam", "#9FD6C3"],
     "fill": "open", "line": "Caramel, espresso, a dab of seafoam."},
]
