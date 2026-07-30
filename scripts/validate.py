#!/usr/bin/env python
from __future__ import annotations

import csv
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

REQUIRED = [
    "README.md",
    "DOCUMENT-STANDARD.md",
    "docs/01-architecture/network-overview.mmd",
    "docs/01-architecture/network-overview.svg",
    "docs/03-hardware/specifications.md",
    "docs/03-hardware/spec-sheet-index.md",
    "docs/03-hardware/component-specifications.csv",
    "docs/03-hardware/connection-matrix.csv",
    "docs/03-hardware/station-bom.csv",
    "docs/04-procurement/orders.md",
    "docs/04-procurement/orders.csv",
    "docs/04-procurement/needs.md",
    "docs/04-procurement/needs.csv",
    "docs/04-procurement/purchase-list.md",
    "docs/04-procurement/purchase-list.csv",
    "docs/02-stations/station-atlas.md",
    "docs/02-stations/station-atlas.mmd",
    "docs/02-stations/station-atlas.svg",
    "docs/02-stations/data-contracts.md",
    "docs/02-stations/data-dictionary.csv",
]
STATIONS = ["IH-01", "IH-02", "SM-01", "SM-02", "SM-03", "SM-04", "MET-01", "WX-CANDIDATE"]

for rel in REQUIRED:
    if not (ROOT / rel).is_file():
        ERRORS.append(f"missing required file: {rel}")

for station in STATIONS:
    path = ROOT / "docs" / "02-stations" / f"{station}.md"
    if not path.is_file():
        ERRORS.append(f"missing station document: {station}")
    else:
        station_text = path.read_text(encoding="utf-8")
        if station not in station_text:
            ERRORS.append(f"station ID absent from document: {station}")
        if station == "WX-CANDIDATE":
            if "no approved stream" not in station_text:
                ERRORS.append("WX-CANDIDATE must state that no data stream is approved")
        elif "Data expected" not in station_text:
            ERRORS.append(f"station document lacks expected-data interface: {station}")
        if "spec-sheet-index.md" not in station_text:
            ERRORS.append(f"station document lacks spec-sheet index link: {station}")

dictionary_path = ROOT / "docs" / "02-stations" / "data-dictionary.csv"
if dictionary_path.is_file():
    with dictionary_path.open(newline="", encoding="utf-8-sig") as handle:
        dictionary_rows = list(csv.DictReader(handle))
    for station in STATIONS[:-1]:
        matching = [row for row in dictionary_rows if station in row.get("applies_to", "").split()]
        if len(matching) < 5:
            ERRORS.append(f"data dictionary has too few fields for {station}: {len(matching)}")

spec_path = ROOT / "docs" / "03-hardware" / "component-specifications.csv"
if spec_path.is_file():
    with spec_path.open(newline="", encoding="utf-8-sig") as handle:
        spec_rows = list(csv.DictReader(handle))
    for row in spec_rows:
        component = row.get("component_id", "unknown")
        source = row.get("spec_sheet_url", "").strip()
        if not source:
            ERRORS.append(f"component lacks spec-sheet source or pending marker: {component}")
        elif "http" not in source and not source.startswith("pending_"):
            ERRORS.append(f"invalid spec-sheet source: {component} -> {source}")

for path in ROOT.rglob("*.csv"):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        ERRORS.append(f"empty CSV: {path.relative_to(ROOT)}")
        continue
    width = len(rows[0])
    for line, row in enumerate(rows[1:], 2):
        if len(row) != width:
            ERRORS.append(f"malformed CSV: {path.relative_to(ROOT)}:{line}")

link_pattern = re.compile(r"!?(?:\[[^]]*\])\(([^)]+)\)")
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for target in link_pattern.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if clean and not (path.parent / clean).resolve().exists():
            ERRORS.append(f"broken link: {path.relative_to(ROOT)} -> {target}")

tracked = []
try:
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
except (subprocess.CalledProcessError, FileNotFoundError):
    pass
for rel in tracked:
    lower = rel.lower()
    if lower.endswith((".eml", ".msg", ".pst", ".mbox", ".xlsx", ".xls", ".pdf", ".key", ".pem")):
        ERRORS.append(f"private/binary artifact tracked: {rel}")

for path in ROOT.rglob("*.mmd"):
    if "flowchart" not in path.read_text(encoding="utf-8"):
        ERRORS.append(f"Mermaid source lacks flowchart: {path.relative_to(ROOT)}")
    svg = path.with_suffix(".svg")
    if not svg.is_file() or svg.stat().st_size == 0:
        ERRORS.append(f"missing Mermaid render: {svg.relative_to(ROOT)}")
    elif "<svg" not in svg.read_text(encoding="utf-8", errors="ignore"):
        ERRORS.append(f"invalid Mermaid render: {svg.relative_to(ROOT)}")

if ERRORS:
    print("VALIDATION FAILED")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print(f"VALIDATION OK: {len(STATIONS)} station records, {len(list(ROOT.rglob('*.md')))} Markdown files")
