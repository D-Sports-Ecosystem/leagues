# Hockey League Assets

Official logos, brand color palettes, and WCAG 2.1 accessibility reports for 17 professional and amateur hockey leagues worldwide.

## Structure

```
leagues/
├── <Country>/
│   └── <League>/
│       ├── logo.*                  # Official logo (SVG or PNG, highest available resolution)
│       ├── colors.json             # Brand colors — primary, secondary, accent for light & dark mode
│       └── accessibility_report.json  # WCAG 2.1 contrast audit for all color pairs
├── accessibility_audit.txt         # Full audit report across all leagues
└── accessibility_audit.py          # Script used to generate the audit
```

## Leagues

| League | Full Name | Country/Region | Logo Format |
|--------|-----------|----------------|-------------|
| [NHL](./North_America/NHL/) | National Hockey League | Canada & USA | SVG |
| [AHL](./Canada/AHL/) | American Hockey League | Canada & USA | PNG |
| [CHL](./Canada/CHL/) | Canadian Hockey League | Canada | PNG |
| [OHL](./Canada/OHL/) | Ontario Hockey League | Canada | PNG |
| [WHL](./Canada/WHL/) | Western Hockey League | Canada | PNG |
| [QMJHL](./Canada/QMJHL/) | Quebec Maritimes Junior Hockey League | Canada | PNG |
| [ECHL](./USA/ECHL/) | East Coast Hockey League | USA | SVG |
| [NCAA](./USA/NCAA/) | National Collegiate Athletic Association | USA | SVG |
| [SHL](./Sweden/SHL/) | Swedish Hockey League | Sweden | SVG |
| [DEL](./Germany/DEL/) | Deutsche Eishockey Liga (PENNY DEL) | Germany | SVG |
| [KHL](./Russia_Belarus_China_Kazakhstan/KHL/) | Kontinental Hockey League | Russia / Belarus / China / Kazakhstan | PNG |
| [LIIGA](./Finland/LIIGA/) | Liiga | Finland | PNG |
| [NL](./Switzerland/NL/) | National League | Switzerland | PNG |
| [SL](./Switzerland/SL/) | Swiss League | Switzerland | PNG |
| [Alps HL](./Austria_Italy_Slovenia/Alps_HL/) | Alps Hockey League | Austria / Italy / Slovenia | PNG |
| [Czech Extraliga](./Czech_Republic/Czech_Extraliga/) | Extraliga ledního hokeje | Czech Republic | PNG |
| [EIHL](./United_Kingdom/EIHL/) | Elite Ice Hockey League | United Kingdom | SVG |

## Color Schema

Each `colors.json` follows this structure:

```json
{
  "league": "NHL",
  "light": {
    "primary":   "#041E42",
    "secondary": "#C8102E",
    "accent":    "#00A9E0"
  },
  "dark": {
    "primary":   "#00A9E0",
    "secondary": "#C8102E",
    "accent":    "#FFFFFF"
  },
  "source": "nhl.com CSS custom properties"
}
```

Colors are sourced from official websites, CSS custom properties, and brand guidelines where available.

## Accessibility Audit

Each league folder includes an `accessibility_report.json` with WCAG 2.1 contrast ratios for every color pair combination in both light and dark mode.

### WCAG 2.1 Thresholds

| Level | Normal Text | Large Text | UI Components |
|-------|-------------|------------|---------------|
| AA    | ≥ 4.5:1     | ≥ 3.0:1    | ≥ 3.0:1       |
| AAA   | ≥ 7.0:1     | ≥ 4.5:1    | —             |

### Audit Summary

| League | Light Mode | Dark Mode | Overall | Verdict |
|--------|-----------|-----------|---------|---------|
| OHL | 86% | 43% | 64% | Needs Work |
| WHL | 76% | 52% | 64% | Needs Work |
| QMJHL | 76% | 52% | 64% | Needs Work |
| NCAA | 76% | 52% | 64% | Needs Work |
| LIIGA | 57% | 71% | 64% | Needs Work |
| AlpsHL | 76% | 52% | 64% | Needs Work |
| CHL | 57% | 62% | 60% | Needs Work |
| KHL | 67% | 52% | 60% | Needs Work |
| SL | 57% | 62% | 60% | Needs Work |
| AHL | 48% | 62% | 55% | Needs Work |
| SHL | 57% | 43% | 50% | Needs Work |
| DEL | 48% | 52% | 50% | Needs Work |
| NHL | 43% | 52% | 48% | Poor |
| NL | 43% | 52% | 48% | Poor |
| ECHL | 38% | 43% | 40% | Poor |
| Czech Extraliga | 38% | 43% | 40% | Poor |
| EIHL | 38% | 43% | 40% | Poor |

> Scores reflect the % of color-pair checks (foreground/background combos) that pass at least AA level across normal text, large text, and UI component criteria.

To regenerate the audit:

```bash
python3 accessibility_audit.py
```
