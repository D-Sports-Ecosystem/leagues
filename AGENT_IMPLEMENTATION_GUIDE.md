# Agent Implementation Guide — League Colors & Accessibility

This guide tells you exactly how to consume the data in this repository to build
UI that is always readable, accessible, and correctly themed for light and dark mode.
Follow these rules precisely. Do not guess or infer colors — every value you need is
already computed in the JSON files.

---

## 1. File You Need Per League

```
<Country>/<League>/colors.json
```

That single file contains everything: brand colors, accessible text colors, and
contrast ratios for both light and dark mode.

---

## 2. The Color Schema — Field Reference

```jsonc
{
  "league": "NHL",

  "light": {                          // Use when the app/page is in LIGHT mode
    "primary":   "#041E42",           // Main brand color — cards, headers, buttons
    "secondary": "#C8102E",           // Supporting brand color — badges, highlights
    "accent":    "#00A9E0",           // Calls-to-action, links, active states

    "text": {
      "on_background": {              // Text directly on the page background (#FFFFFF)
        "color": "#000000",
        "contrast_ratio": 21.0
      },
      "on_primary": {                 // Text on a primary-colored surface (card, header)
        "color": "#FFFFFF",
        "contrast_ratio": 16.54
      },
      "on_secondary": {               // Text on a secondary-colored surface (badge, tag)
        "color": "#FFFFFF",
        "contrast_ratio": 5.88
      },
      "on_accent": {                  // Text on an accent-colored surface (CTA button)
        "color": "#000000",
        "contrast_ratio": 7.75
      }
    }
  },

  "dark": {                           // Use when the app/page is in DARK mode
    "primary":   "#00A9E0",
    "secondary": "#C8102E",
    "accent":    "#FFFFFF",

    "text": {
      "on_background": {              // Text on the dark page background (#0D1117)
        "color": "#FFFFFF",
        "contrast_ratio": 18.92
      },
      "on_primary":    { "color": "#000000", "contrast_ratio": 7.75  },
      "on_secondary":  { "color": "#FFFFFF", "contrast_ratio": 5.88  },
      "on_accent":     { "color": "#000000", "contrast_ratio": 21.0  }
    }
  }
}
```

---

## 3. Core Rule — Always Pair Surface + Its Text Color Together

**Never use a brand color for a surface without also applying the matching text color.**

| You are rendering… | Background value to use | Text color to use |
|---|---|---|
| Page / screen background | `#FFFFFF` (light) or `#0D1117` (dark) | `text.on_background.color` |
| Primary card / header / section | `primary` | `text.on_primary.color` |
| Secondary badge / tag / label | `secondary` | `text.on_secondary.color` |
| Accent button / link / active indicator | `accent` | `text.on_accent.color` |

**Example — correct:**
```
card background  →  colors.light.primary          (#041E42)
card title text  →  colors.light.text.on_primary.color   (#FFFFFF)
```

**Example — wrong:**
```
card background  →  colors.light.primary          (#041E42)
card title text  →  colors.light.secondary        (#C8102E)   ← contrast ratio 2.81:1, FAIL
```

---

## 4. Selecting Light vs Dark Mode

Read the user's current mode from their OS/app preference and select the
corresponding top-level key.

```js
const mode = userPrefersDark ? 'dark' : 'light'
const colors = leagueColors[mode]

// Background of the screen
const pageBg   = userPrefersDark ? '#0D1117' : '#FFFFFF'
const pageText = colors.text.on_background.color

// A league-branded card
const cardBg   = colors.primary
const cardText = colors.text.on_primary.color
```

Never mix keys across modes (e.g. `light.primary` as background with `dark.text.on_primary`).

---

## 5. Contrast Ratio Values — How to Use Them

Every `text` entry includes a `contrast_ratio`. Use it to make runtime decisions.

### WCAG 2.1 Minimum Thresholds

| Use case | Minimum ratio | Field to check |
|---|---|---|
| Body / paragraph text | **4.5:1** (AA) | `contrast_ratio >= 4.5` |
| Headings / large text (≥18px regular or ≥14px bold) | **3.0:1** (AA) | `contrast_ratio >= 3.0` |
| Icons, borders, UI chrome | **3.0:1** (AA) | `contrast_ratio >= 3.0` |
| Preferred for all text | **7.0:1** (AAA) | `contrast_ratio >= 7.0` |

### Decision Logic

```js
function getTextColor(surface, mode, leagueColors) {
  const text = leagueColors[mode].text[`on_${surface}`]

  if (text.contrast_ratio >= 4.5) {
    return text.color          // Safe for all text sizes
  } else if (text.contrast_ratio >= 3.0) {
    return text.color          // Safe for large text and UI only — use font-size >= 18px
  } else {
    // Contrast is below AA — fall back to pure black or white
    return mode === 'dark' ? '#FFFFFF' : '#000000'
  }
}
```

### When to Fall Back

A small number of leagues have a secondary color that only barely clears AA for
normal text (ratio between 4.5–5.0). In those cases:
- Use the provided text color for headings and labels
- For small body text (<16px), prefer `#FFFFFF` or `#000000` instead of relying on the brand color surface

---

## 6. Combinations to Avoid

The `accessibility_report.json` in each league folder documents every color-pair
combination. Several brand-color-on-brand-color combinations fail WCAG. Do not
use these as foreground/background pairs.

**Common failures across leagues:**
- `primary` text on `secondary` background — almost always < 3:1
- `secondary` text on `primary` background — same
- `accent` text on `secondary` background — frequently < 3:1

**Rule:** Only use brand colors as backgrounds. Use `text.on_*` for the text on top.
Never layer one brand color on top of another for readable text.

```
// NEVER do this — two brand colors fighting each other
color:            colors.light.accent      ← low contrast on red
background-color: colors.light.secondary

// DO this instead
color:            colors.light.text.on_secondary.color   ← pre-computed safe value
background-color: colors.light.secondary
```

---

## 7. Common UI Patterns

### League Card (matches the app screenshots)

```
┌─────────────────────────────┐
│  [card bg = primary]        │
│                             │
│    ○ Team Logo              │
│                             │
│  ✓ OFFICIAL                 │  ← badge bg = accent, text = text.on_accent.color
│                             │
│  Team Name                  │  ← text = text.on_primary.color
│  League                     │  ← text = text.on_primary.color, reduced opacity ok
│                             │
│  > Follow                   │  ← text = text.on_primary.color
└─────────────────────────────┘
```

### Rankings Row (on page background)

```
4   [avatar]   Player Name  ✦ Elite      840  —
```
- Row background: page background (`#FFFFFF` / `#0D1117`)
- Rank number: `text.on_background.color`
- Player name: `text.on_background.color`
- Points: `primary` (light mode) or `primary` (dark mode) — check `accessibility_report.json` for ratio on the page bg first; if FAIL, use `text.on_background.color` instead
- Elite badge: `accent` background + `text.on_accent.color` text

### Section Header

```
SWISS TEAMS  4        See All
```
- Label text: `text.on_background.color`
- Count bubble: `secondary` background + `text.on_secondary.color`
- "See All" link: `accent` — only use if contrast_ratio on page bg ≥ 3.0 (check `accessibility_report.json`); otherwise use `primary`

---

## 8. Reading `accessibility_report.json`

Use this file to make build-time or runtime decisions about which combinations
are safe to use beyond the pre-approved surface+text pairings.

```jsonc
// accessibility_report.json
{
  "league": "NHL",
  "scores": {
    "light_mode": 43,      // % of pairs passing WCAG — informational only
    "dark_mode": 52,
    "overall": 48,
    "verdict": "Poor"      // Reflects brand color pair clashes, NOT text-on-surface safety
  },
  "light_mode": [
    {
      "pair": "Accent on light bg",
      "foreground": "#00A9E0",
      "background": "#FFFFFF",
      "ratio": 2.71,
      "normal_text": "FAIL",   // Do NOT use accent as standalone text on white
      "large_text":  "FAIL",
      "ui_component":"FAIL"
    },
    ...
  ]
}
```

> **Important:** The "Poor" / "Needs Work" verdict in scores reflects how brand
> colors perform when used as raw text on raw backgrounds — a stress test of the
> palette, not a verdict on the pre-computed `text.*` values. The `text.*` values
> in `colors.json` are always the safe choice and should be used instead of
> applying brand colors as text directly.

---

## 9. Quick-Reference Decision Tree

```
I need to render text on a surface. What color do I use?

Is the surface the page background?
  YES → colors[mode].text.on_background.color

Is the surface filled with `primary`?
  YES → colors[mode].text.on_primary.color

Is the surface filled with `secondary`?
  YES → colors[mode].text.on_secondary.color

Is the surface filled with `accent`?
  YES → colors[mode].text.on_accent.color

Is the surface a custom color not in the palette?
  YES → Compute contrast ratio yourself:
        white (#FFFFFF) vs. the surface
        black (#000000) vs. the surface
        Use whichever ratio is higher.
        If both fail 4.5:1, do not use that surface color.
```

---

## 10. Loading the Data

```js
// Node / browser
const colors = await fetch('./Canada/OHL/colors.json').then(r => r.json())

// React Native / Expo
const colors = require('./leagues/Canada/OHL/colors.json')

const mode = 'dark'
const theme = {
  pageBg:        mode === 'dark' ? '#0D1117' : '#FFFFFF',
  pageText:      colors[mode].text.on_background.color,
  cardBg:        colors[mode].primary,
  cardText:      colors[mode].text.on_primary.color,
  badgeBg:       colors[mode].secondary,
  badgeText:     colors[mode].text.on_secondary.color,
  ctaBg:         colors[mode].accent,
  ctaText:       colors[mode].text.on_accent.color,
}
```

---

## 11. Summary of Guarantees

When you follow this guide:

| Guarantee | How |
|---|---|
| Text on page background is always readable | `text.on_background` ≥ 18.92:1 in dark, 21:1 in light |
| Text on primary cards is always AA or better | `text.on_primary` selected as highest-contrast of white/black |
| Text on secondary surfaces is always AA or better | `text.on_secondary` same method |
| Text on accent surfaces is always AA or better | `text.on_accent` same method |
| No brand color is used as text on a brand background without validation | `accessibility_report.json` documents every such pair |
| Light and dark modes are fully independent | Never mix keys across modes |
