"""
Adds accessible text colors to every league colors.json.

For each mode (light / dark) we need readable text on four surfaces:
  - on_background  : text on the page background (#FFFFFF or #0D1117)
  - on_primary     : text on the primary-colored card / element
  - on_secondary   : text on the secondary-colored element
  - on_accent      : text on the accent-colored element

Strategy:
  1. Try white (#FFFFFF) and black (#000000) against the surface.
  2. Pick whichever gives the higher contrast ratio.
  3. If neither hits AA normal text (4.5:1), try a softened alternative
     (light cream or dark charcoal) and pick the best of all four candidates.
  4. Record the chosen color AND the final contrast ratio so it's auditable.
"""

import json
from pathlib import Path

# ── WCAG helpers ──────────────────────────────────────────────────────────────

def linearize(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def luminance(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b)

def contrast(fg, bg):
    l1, l2 = luminance(fg), luminance(bg)
    lighter, darker = max(l1, l2), min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def best_text(bg_hex):
    """
    Return (text_hex, ratio) — the text color that maximises contrast on bg_hex.
    Candidates: pure white, pure black, soft off-white, dark charcoal.
    """
    candidates = ["#FFFFFF", "#000000", "#F0F4F8", "#1A1A2E"]
    best_color, best_ratio = "#FFFFFF", 0.0
    for c in candidates:
        r = contrast(c, bg_hex)
        if r > best_ratio:
            best_ratio, best_color = r, c
    return best_color, round(best_ratio, 2)

# ── page backgrounds used by the app ─────────────────────────────────────────

LIGHT_BG = "#FFFFFF"
DARK_BG  = "#0D1117"   # near-black navy used in the screenshots

# ── league paths ──────────────────────────────────────────────────────────────

BASE = Path("/Users/sekun/leagues")

LEAGUES = [
    "North_America/NHL",
    "Canada/AHL",
    "Canada/CHL",
    "Canada/OHL",
    "Canada/WHL",
    "Canada/QMJHL",
    "USA/ECHL",
    "USA/NCAA",
    "Sweden/SHL",
    "Germany/DEL",
    "Russia_Belarus_China_Kazakhstan/KHL",
    "Finland/LIIGA",
    "Switzerland/NL",
    "Switzerland/SL",
    "Austria_Italy_Slovenia/Alps_HL",
    "Czech_Republic/Czech_Extraliga",
    "United_Kingdom/EIHL",
]

# ── process each league ───────────────────────────────────────────────────────

for rel in LEAGUES:
    path = BASE / rel / "colors.json"
    with open(path) as f:
        data = json.load(f)

    for mode, bg in [("light", LIGHT_BG), ("dark", DARK_BG)]:
        colors = data[mode]
        p, s, a = colors["primary"], colors["secondary"], colors["accent"]

        bg_text,  bg_ratio  = best_text(bg)
        p_text,   p_ratio   = best_text(p)
        s_text,   s_ratio   = best_text(s)
        a_text,   a_ratio   = best_text(a)

        colors["text"] = {
            "on_background": {
                "color": bg_text,
                "contrast_ratio": bg_ratio
            },
            "on_primary": {
                "color": p_text,
                "contrast_ratio": p_ratio
            },
            "on_secondary": {
                "color": s_text,
                "contrast_ratio": s_ratio
            },
            "on_accent": {
                "color": a_text,
                "contrast_ratio": a_ratio
            }
        }

    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    league_name = rel.split("/")[-1]
    lm = data["light"]["text"]
    dm = data["dark"]["text"]
    print(
        f"{league_name:<20} "
        f"light → bg:{lm['on_background']['color']}({lm['on_background']['contrast_ratio']:>5.2f})  "
        f"pri:{lm['on_primary']['color']}({lm['on_primary']['contrast_ratio']:>5.2f})  "
        f"sec:{lm['on_secondary']['color']}({lm['on_secondary']['contrast_ratio']:>5.2f})  "
        f"acc:{lm['on_accent']['color']}({lm['on_accent']['contrast_ratio']:>5.2f})"
    )
    print(
        f"{'':20} "
        f" dark → bg:{dm['on_background']['color']}({dm['on_background']['contrast_ratio']:>5.2f})  "
        f"pri:{dm['on_primary']['color']}({dm['on_primary']['contrast_ratio']:>5.2f})  "
        f"sec:{dm['on_secondary']['color']}({dm['on_secondary']['contrast_ratio']:>5.2f})  "
        f"acc:{dm['on_accent']['color']}({dm['on_accent']['contrast_ratio']:>5.2f})"
    )
    print()

print("Done — all colors.json updated.")
