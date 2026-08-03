# Contributing

## Before editing

1. Read `DOCUMENT-STANDARD.md`.
2. Check the station lifecycle and procurement state.
3. Find the primary evidence before changing status.
4. Keep private evidence outside this repository.

## Change rules

- Update the station document, `connection-matrix.csv`, and `station-bom.csv` together when a model or connection changes.
- Record a physical model or serial inspection before changing an `unverified` model to verified.
- Render changed Mermaid diagrams with `python scripts/render_diagrams.py <changed.mmd> [...]` and confirm that their SVGs open. The render script stamps each SVG and existing PNG with its source hash so validation rejects stale images.
- Explain substitutions by function, voltage, protocol, accuracy, environmental rating, mechanical fit, firmware impact, and approval evidence.
- Keep generated caches, raw exports, financial workbooks, email files, and secrets out of Git.

## Verification

Run `scripts/validate.py` before committing. It checks required files, CSV shape, Markdown links, station IDs, Mermaid source, and the privacy boundary.
