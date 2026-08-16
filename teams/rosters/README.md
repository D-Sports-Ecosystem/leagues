# Team roster data (`teams/rosters.json`)

Starters + bench player data per club, complementing `teams/teams.canonical.json` (which covers branding/logos/colors, not players).

## Purpose

- Give consumers (e.g. a lineup builder) a real, named roster per team instead of fabricated demo data.
- Keyed by the same `slug` used in `teams/teams.canonical.json`, so a consumer can join the two files.

## Schema

```json
{
  "schemaVersion": "1.0.0",
  "note": "...",
  "rosters": {
    "<slug>": {
      "asOf": "2025-26",
      "league": "...",
      "players": [
        { "name": "Full Name", "jersey": 12, "position": "D", "note": "optional caveat" }
      ],
      "sources": ["https://..."]
    }
  }
}
```

- `position` vocabulary (hockey — every team in this file today is a hockey club): `G` (goalie), `C` (center), `LW` (left wing), `RW` (right wing), `D` (defenseman).
- `note` on a player is optional — used when a source only exposed a broad "Forward" grouping without a center/wing split (defaulted to `C` and flagged), or when a player's position/status was ambiguous across sources.
- `sources` lists the URLs used to compile that team's roster (official club/athletics sites, hockeydb.com, EliteProspects, Wikipedia, league news).

## Coverage and scope

- **Starters + bench, not a full organizational depth chart.** Typically 15-22 players per club: goalies, defensemen, and forwards, enough to fill a lineup/formation builder.
- **This is a research snapshot, not a live feed.** Each team's `asOf` records the season the data represents. Rosters turn over — junior and college rosters especially — so this file will drift over time without a re-scrape.
- Every player is a real, named, public person, cross-checked against at least one independent source beyond the primary one. No fabricated or placeholder players are included anywhere in this file.
- Teams without a real competitive roster (e.g. brand/promotional teams) are intentionally absent from this file rather than given placeholder data.

## Adding a new team's roster

1. Confirm the team's `slug` already exists in `teams/teams.canonical.json`.
2. Research via the club's official site plus at least one independent cross-check (hockeydb.com, EliteProspects, Wikipedia, or league news).
3. Add an entry to `teams/rosters.json` keyed by that slug, following the schema above.
4. Flag any position ambiguity with a per-player `note` rather than guessing silently.
