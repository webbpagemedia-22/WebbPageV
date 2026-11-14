# The Neuro Spicy Cookbook (formerly Cooking with OG): source

The recipe book at webbpageventura.co.uk/neuro-spicy-cookbook is built from these files.
Never edit `../index.html` or the PDF by hand; edit here and rebuild.

- `recipes.json`: the recipes, from OG's Apple Notes. Each step lists technique IDs in `tech`.
  A step's `check` note, or an `ingredientChecks` entry, marks something OG hasn't approved yet.
- `videos.json`: one YouTube video per technique ID (`id`, `start` seconds, `title`, `channel`, `short`).
  One video serves every step that uses that technique, so fixing it here fixes it everywhere.
- `labels.json`: plain names for each technique ("chopping an onion").

Build (from this folder):
- `python3 build.py` builds the DRAFT: yellow "OG to check" notes, noindex. This is what's live now.
- `python3 build.py --public` builds the final version, once OG has approved every check note.
- `python3 build_print.py --public` builds the print PDF, ../the-neuro-spicy-cookbook.pdf (needs `pip install segno playwright`).
  QR codes point at `/neuro-spicy-cookbook/#/<recipe-id>/<step>`, so swapping a video never needs a reprint.

Video rules: short (ideally under 4 mins), shows exactly that step, reputable channel, and it must
be allowed to embed: `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=ID&format=json`
returns 200 (401/403 = embedding off, 404 = gone).
