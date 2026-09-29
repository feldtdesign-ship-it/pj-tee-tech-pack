"""Small branding: woven labels and tags on the tee (3.1). The page's Branding tab and the PDF's branding sheet read
from here. Placements follow Michael's reference sheet (2026-09-29): A neck, B bottom hem, C sleeve, D pocket,
E outer side hem, F inner side hem.

Every size and position here is a STARTING POINT (common for woven labels), not from PJ or a label maker: TBC.

  kind     "flag"  = a folded tab sewn into a seam, sticking out of it (side seam, sleeve)
           "patch" = sewn flat on the fabric (hem, neck, pocket)
  w, h     finished size showing, inches (a flag: how far it sticks out x how tall)
  where    plain-words position for the spec
  on       shown when the page opens
  needs    "pocket": only on a tee with a pocket (SHGD has none; the page can add a pocket to try it)
"""
TRIMS = [
    {"key": "A", "name": "Neck", "kind": "patch", "w": 0.9, "h": 0.4, "on": False,
     "where": "On the collar rib, wearer's left front, centred 2 in from center front"},
    {"key": "B", "name": "Bottom hem", "kind": "patch", "w": 2.0, "h": 0.8, "on": True,
     "where": "Front, wearer's right, sewn on just above the hem stitch, 2 in in from the side seam"},
    {"key": "C", "name": "Sleeve", "kind": "patch", "w": 0.9, "h": 0.45, "on": True,
     "where": "Wearer's left sleeve, outer face, sewn into the sleeve hem"},
    {"key": "D", "name": "Pocket", "kind": "flag", "w": 0.6, "h": 0.4, "on": False, "needs": "pocket",
     "where": "Sewn into the pocket's side seam at the top, wearer's left pocket"},
    {"key": "E", "name": "Outer side hem", "kind": "flag", "w": 0.75, "h": 0.5, "on": True,
     "where": "Wearer's left side seam, outside, 2 in above the hem, pointing forward"},
    {"key": "F", "name": "Inner side hem", "kind": "flag", "w": 0.75, "h": 0.5, "on": False,
     "where": "Wearer's right side seam, inside, 2 in above the hem"},
]

# Patch pocket for trying placement D (not on the SHGD; a pocket blank is TBC). Inches.
POCKET = {"w": 4.5, "h": 5.0, "top": 7.5, "over": 4.0,
          "where": "Wearer's left chest, top 7 1/2 in below the HPS, middle 4 in from center front"}

# What goes on the labels. Art: PJ's real signature file (never redrawn), or his name set in type.
LABEL = {
    "art": ["Signature", "Name"],
    "grounds": [["Black", "#161616"], ["White", "#F4F2EC"], ["Cream", "#EDE3CC"], ["Red", "#B3261E"], ["Navy", "#1F2E4A"]],
    "threads": [["White", "#F7F5EF"], ["Black", "#141414"], ["Cream", "#E9DDBF"], ["Gold", "#C9A24B"], ["Red", "#C7342B"]],
    "default": {"art": "Signature", "ground": "#161616", "thread": "#F7F5EF"},
}

DECISIONS = [
    ("What the label says", "PJ's signature, his name, a mark, or a line like NEW YORK. Same on every tag, or different per spot."),
    ("Woven, printed or patch", "Woven damask labels (like the references), printed satin, or a heat-transfer print (tagless). Sets the label maker and the cost."),
    ("Which spots", "One outer mark (side hem or sleeve) is the usual; the neck and inside tags carry size and care. Pick the set."),
    ("Colours", "Label ground and thread per shirt colour, or one label for every colour."),
    ("Pocket", "The SHGD has no pocket. A pocket tee needs its own blank, or a sewn-on pocket at the factory."),
    ("Care and content", "Size, fibre, care and country of origin are required on a label somewhere. Printed inside the neck, or on the inner side-seam tag (F)."),
]
