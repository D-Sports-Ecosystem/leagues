# Team metadata (`teams.canonical.json`)

This folder holds **machine-readable team records** that are separate from the league logo and `colors.json` tree under `<Country>/<League>/`.

## Purpose

- Give importers a **single canonical name**, **stable slug**, and **league code** per team.
- Capture **aliases** so fuzzy or legacy strings from feeds, vendors, or user input can be normalized to one record.
- Reserve **`externalRefs`** for future IDs (API keys, federation IDs, etc.) without changing the core shape.
- **`branding`** (from schema `1.1.0+`): `primaryColor` / `secondaryColor` (hex), `logoUrl` (original download/reference URL), `logoPath` (path relative to **repository root** under `teams/assets/…`), and **`sources`** entries that explain provenance and confidence.

## Logo assets (`teams/assets/`)

Logos are stored under:

`teams/assets/<leagueCode>/<slug>/logo.<ext>`

Example: `teams/assets/NHL/toronto-maple-leafs/logo.svg`.

- Paths in JSON use **forward slashes** and are relative to the **leagues repo root** (not this `teams/` folder only).
- Many files were sourced from **Wikimedia Commons** or **English Wikipedia** logo files. **Copyright and trademark rules still apply**; `branding.sources` notes whether a file is Commons-licensed or a Wikipedia *non-free / fair-use* logo. Do not assume redistribution rights for NHL, OHL, NCAA marks, etc., without your own clearance.

## Sourcing and color confidence

- **Official** university or league brand pages are preferred for hex values where available.
- **Aggregators** (e.g. team color code sites) are used only when no official hex is published; those rows are labeled in `sources.quality`.
- When hex values are **estimated** from kits or logos, `sources.note` states that explicitly.

## Normalization intent

1. **Match on `slug`** when you control identifiers; it is stable and URL-safe.
2. **Match incoming strings** against `canonicalName`, `displayName`, and `aliases` (case-folding and trimming are recommended; collation is up to the importer).
3. **Use `leagueCode`** for league association. Codes here may be finer-grained than this repo’s folder layout (e.g. `NCAA-BigTen` vs `USA/NCAA/`). Importers should map `leagueCode` to their own league registry or to paths in this repo as needed.
4. **`country`** is ISO 3166-1 alpha-2 where the home market is unambiguous for the listed team.

`schemaVersion` documents the top-level JSON contract; bump it when you make breaking changes to required fields or types.
