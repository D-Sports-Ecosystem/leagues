"""
WCAG 2.1 Accessibility Audit for Hockey League Color Schemes
Checks contrast ratios for all color combinations in light and dark mode.

WCAG Thresholds:
  AA  normal text  : 4.5:1
  AA  large text   : 3.0:1
  AA  UI component : 3.0:1
  AAA normal text  : 7.0:1
  AAA large text   : 4.5:1
"""

import json
import os
import math
from pathlib import Path

# ── WCAG helpers ──────────────────────────────────────────────────────────────

def hex_to_rgb(hex_color):
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def linearize(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

def relative_luminance(hex_color):
    r, g, b = hex_to_rgb(hex_color)
    R, G, B = linearize(r), linearize(g), linearize(b)
    return 0.2126 * R + 0.7152 * G + 0.0722 * B

def contrast_ratio(hex1, hex2):
    l1 = relative_luminance(hex1)
    l2 = relative_luminance(hex2)
    lighter = max(l1, l2)
    darker  = min(l1, l2)
    return (lighter + 0.05) / (darker + 0.05)

def wcag_grade(ratio):
    """Return AA/AAA grades for normal text, large text, and UI components."""
    grades = {}
    grades["normal_text"] = (
        "AAA" if ratio >= 7.0 else
        "AA"  if ratio >= 4.5 else
        "FAIL"
    )
    grades["large_text"] = (
        "AAA" if ratio >= 4.5 else
        "AA"  if ratio >= 3.0 else
        "FAIL"
    )
    grades["ui_component"] = (
        "AA"  if ratio >= 3.0 else
        "FAIL"
    )
    return grades

def emoji_grade(grade):
    return {"AAA": "✅ AAA", "AA": "🟡 AA", "FAIL": "❌ FAIL"}[grade]

# ── league discovery ──────────────────────────────────────────────────────────

BASE = Path("/Users/sekun/leagues")

LEAGUES = [
    ("North_America/NHL",                    "NHL"),
    ("Canada/AHL",                           "AHL"),
    ("Canada/CHL",                           "CHL"),
    ("Canada/OHL",                           "OHL"),
    ("Canada/WHL",                           "WHL"),
    ("Canada/QMJHL",                         "QMJHL"),
    ("USA/ECHL",                             "ECHL"),
    ("USA/NCAA",                             "NCAA"),
    ("Sweden/SHL",                           "SHL"),
    ("Germany/DEL",                          "DEL"),
    ("Russia_Belarus_China_Kazakhstan/KHL",  "KHL"),
    ("Finland/LIIGA",                        "LIIGA"),
    ("Switzerland/NL",                       "NL"),
    ("Switzerland/SL",                       "SL"),
    ("Austria_Italy_Slovenia/Alps_HL",       "AlpsHL"),
    ("Czech_Republic/Czech_Extraliga",       "Czech Extraliga"),
    ("United_Kingdom/EIHL",                  "EIHL"),
]

# ── analysis ──────────────────────────────────────────────────────────────────

LIGHT_BG = "#FFFFFF"
DARK_BG  = "#000000"

def analyse_mode(colors, bg, mode_label):
    p = colors["primary"]
    s = colors["secondary"]
    a = colors["accent"]

    pairs = [
        (f"Primary on {mode_label} bg",   p, bg),
        (f"Secondary on {mode_label} bg", s, bg),
        (f"Accent on {mode_label} bg",    a, bg),
        ("Primary on Secondary",          p, s),
        ("Secondary on Primary",          s, p),
        ("Accent on Primary",             a, p),
        ("Accent on Secondary",           a, s),
    ]

    results = []
    for label, fg, bkg in pairs:
        ratio = contrast_ratio(fg, bkg)
        grades = wcag_grade(ratio)
        results.append({
            "pair":         label,
            "foreground":   fg,
            "background":   bkg,
            "ratio":        round(ratio, 2),
            "normal_text":  grades["normal_text"],
            "large_text":   grades["large_text"],
            "ui_component": grades["ui_component"],
        })
    return results

def score_mode(results):
    """Score 0-100 based on pass rates across all pairs."""
    total = len(results) * 3  # 3 checks per pair
    passes = sum(
        (1 if r["normal_text"]  != "FAIL" else 0) +
        (1 if r["large_text"]   != "FAIL" else 0) +
        (1 if r["ui_component"] != "FAIL" else 0)
        for r in results
    )
    return round(passes / total * 100)

def overall_verdict(score):
    if score >= 90: return "Excellent"
    if score >= 70: return "Good"
    if score >= 50: return "Needs Work"
    return "Poor"

# ── report generation ─────────────────────────────────────────────────────────

def render_table(results):
    lines = []
    lines.append(f"  {'Pair':<30} {'FG':<9} {'BG':<9} {'Ratio':>6}  {'Normal':>10}  {'Large':>10}  {'UI':>10}")
    lines.append("  " + "-" * 92)
    for r in results:
        lines.append(
            f"  {r['pair']:<30} {r['foreground']:<9} {r['background']:<9} "
            f"{r['ratio']:>6.2f}  "
            f"{emoji_grade(r['normal_text']):>15}  "
            f"{emoji_grade(r['large_text']):>15}  "
            f"{emoji_grade(r['ui_component']):>15}"
        )
    return "\n".join(lines)

reports = {}
summary_rows = []

for rel_path, name in LEAGUES:
    json_path = BASE / rel_path / "colors.json"
    with open(json_path) as f:
        data = json.load(f)

    light_results = analyse_mode(data["light"], LIGHT_BG, "light")
    dark_results  = analyse_mode(data["dark"],  DARK_BG,  "dark")

    light_score = score_mode(light_results)
    dark_score  = score_mode(dark_results)
    overall     = round((light_score + dark_score) / 2)

    reports[name] = {
        "data":          data,
        "light_results": light_results,
        "dark_results":  dark_results,
        "light_score":   light_score,
        "dark_score":    dark_score,
        "overall":       overall,
    }
    summary_rows.append((name, light_score, dark_score, overall, overall_verdict(overall)))

# ── write per-league report JSON ──────────────────────────────────────────────

for rel_path, name in LEAGUES:
    r = reports[name]
    report_data = {
        "league": name,
        "scores": {
            "light_mode": r["light_score"],
            "dark_mode":  r["dark_score"],
            "overall":    r["overall"],
            "verdict":    overall_verdict(r["overall"]),
        },
        "light_mode": r["light_results"],
        "dark_mode":  r["dark_results"],
    }
    out_path = BASE / rel_path / "accessibility_report.json"
    with open(out_path, "w") as f:
        json.dump(report_data, f, indent=2)

# ── write master text report ──────────────────────────────────────────────────

lines = []
lines.append("=" * 100)
lines.append("  HOCKEY LEAGUE COLOR ACCESSIBILITY AUDIT — WCAG 2.1")
lines.append("=" * 100)
lines.append("")
lines.append("  Scoring: % of color-pair checks that pass (normal text + large text + UI component)")
lines.append("  Thresholds: AA normal text ≥4.5:1 | AA large text ≥3:1 | UI component ≥3:1 | AAA normal ≥7:1")
lines.append("")

# summary table
lines.append("  SUMMARY")
lines.append("  " + "-" * 60)
lines.append(f"  {'League':<20} {'Light':>8}  {'Dark':>8}  {'Overall':>8}  {'Verdict'}")
lines.append("  " + "-" * 60)
for name, ls, ds, ov, verdict in sorted(summary_rows, key=lambda x: -x[3]):
    bar = "█" * (ov // 10) + "░" * (10 - ov // 10)
    lines.append(f"  {name:<20} {ls:>7}%  {ds:>7}%  {ov:>7}%  {bar}  {verdict}")
lines.append("")

# per-league details
for rel_path, name in LEAGUES:
    r = reports[name]
    d = r["data"]
    lines.append("=" * 100)
    lines.append(f"  {name}")
    lines.append(f"  Light mode colors → primary:{d['light']['primary']}  secondary:{d['light']['secondary']}  accent:{d['light']['accent']}")
    lines.append(f"  Dark  mode colors → primary:{d['dark']['primary']}  secondary:{d['dark']['secondary']}  accent:{d['dark']['accent']}")
    lines.append(f"  Scores: Light {r['light_score']}%  |  Dark {r['dark_score']}%  |  Overall {r['overall']}%  [{overall_verdict(r['overall'])}]")
    lines.append("")
    lines.append("  ── LIGHT MODE ──")
    lines.append(render_table(r["light_results"]))
    lines.append("")
    lines.append("  ── DARK MODE ──")
    lines.append(render_table(r["dark_results"]))
    lines.append("")

lines.append("=" * 100)
lines.append("  END OF REPORT")
lines.append("=" * 100)

report_text = "\n".join(lines)
with open(BASE / "accessibility_audit.txt", "w") as f:
    f.write(report_text)

print(report_text)
