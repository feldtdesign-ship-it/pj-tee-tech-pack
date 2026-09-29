"""Colourways for the tee. build.py reads this for the viewer and the PDF.

Source: Claude outputs/PJ_Sydney_Colour_Sheet.pdf (draft). Its own note: hex codes are starting
points, picked by us. Match them to the real ink and fabric before anything gets printed.
Pantone refs stay TBC until then.

Shirt colours are the nearest real Shaka Wear SHGD garment-dyed colour, with its Pantone (Michael, 2026-09-28).
"design" keeps the Sydney sheet's original hex. Sandstone: caramel has no SHGD match; Peach chosen (espresso line reads on it).

How a colourway lands on the Citibike Gumbit tee (Michael, 2026-09-24):
  shirt  = body colour
  print  = front line ink (fills left open, so the shirt shows through)
  accent = PJ's signature at the back neck
"Classic" is the pack's original look: cream shirt, black line, signature in the line ink.
"""

SOURCE = "PJ Sydney Colour Sheet (draft), shirts mapped to Shaka Wear SHGD colours (Pantone from the maker). Line and signature hex are starting points; ink Pantone TBC."

COLOURWAYS = [
    {"key": "classic", "num": "00", "name": "Classic", "tag": "The original",
     "shirt": ["Cream", "#F2DFC0"], "pms": "7506 C", "design": "#F3EFE4", "print": ["Black", "#121212"], "accent": ["Black", "#121212"],
     "fill": "print", "line": "Cream tee, black line, white fills. The pack as first drawn."},
    {"key": "harbour", "num": "01", "name": "Harbour", "tag": "Hero",
     "shirt": ["Midnight Navy", "#304766"], "pms": "289 C", "design": "#14264A", "print": ["Vanilla", "#F1E9D2"], "accent": ["Red", "#D8322B"],
     "fill": "open", "line": "Navy, vanilla, one red. The tee equivalent of a good haircut."},
    {"key": "jacaranda", "num": "02", "name": "Jacaranda", "tag": "The loud one",
     "shirt": ["Pastel Purple", "#EDD0EF"], "pms": "264 C", "design": "#B9A6D6", "print": ["Plum", "#4A2A5E"], "accent": ["Butter", "#F2D36B"],
     "fill": "open", "line": "Lilac, plum, butter. Purple, but with a reason."},
    {"key": "bush", "num": "03", "name": "Bush", "tag": "Outdoor style",
     "shirt": ["Moss", "#4C605E"], "pms": "3435 C", "design": "#5B6B45", "print": ["Sand", "#D9C7A0"], "accent": ["Rust", "#B5532F"],
     "fill": "open", "line": "Moss, sand, rust."},
    {"key": "sandstone", "num": "04", "name": "Sandstone", "tag": "The bridge",
     "shirt": ["Peach", "#FEA580"], "pms": "805 C", "design": "#B98B5E", "print": ["Espresso", "#3B2A20"], "accent": ["Seafoam", "#9FD6C3"],
     "fill": "open", "line": "Peach, espresso, a dab of seafoam."},
]
