# Contributing

## Before editing

1. Read `DOCUMENT-STANDARD.md`.
2. Check the station's lifecycle and procurement state.
3. Find the primary evidence. Do not upgrade status from memory.
4. Keep private evidence outside this repository.

## Change rules

- Update the station document, `connection-matrix.csv`, and `station-bom.csv` together when a model or connection changes.
- Record a physical model/serial inspection before resolving an `unverified` model.
- Render changed Mermaid diagrams and confirm their SVGs open.
- Explain substitutions by function, voltage, protocol, accuracy, environmental rating, mechanical fit, firmware impact, and approval evidence.
- Do not commit generated caches, raw exports, financial workbooks, email files, or secrets.

## Verification

Run `scripts/validate.py` before committing. The validator checks required files, CSV shape, Markdown links, station IDs, Mermaid source, and the privacy boundary.
