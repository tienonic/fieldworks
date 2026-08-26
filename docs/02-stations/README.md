# Station index

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-08-24
Evidence: proposal architecture, compatibility grid, procurement evidence, partial physical inventory, reported Davis 6162 inspection, and current station records

## Start with the station atlas

[Open the Station Atlas](station-atlas.md) for each station package, its expected data, its field question, and its deployment blockers.

- [Data contracts and example records](data-contracts.md)
- [Machine-readable data dictionary](data-dictionary.csv)
- [External HOBO and iPERL integration paths](external-integrations.md)

## Phase I field stations

| ID | Purpose | Site | Lifecycle |
|---|---|---|---|
| [IH-01](IH-01.md) | Irrigation flow, pressure, and valve-control path | Unassigned | partial pool inventory; compatibility, allocation, and bench gates open |
| [IH-02](IH-02.md) | Second irrigation head | Unassigned | ordered; partial pool inventory; build gated on IH-01 |
| [SM-01](SM-01.md) | Soil tension at three depths plus temperature | Unassigned | three bagged pool assemblies need exact model and completeness checks |
| [SM-02](SM-02.md) | Soil tension at three depths plus temperature | Unassigned | ordered; pool allocation unverified; build gated on SM-01 |
| [SM-03](SM-03.md) | Soil tension at three depths plus temperature | Unassigned | ordered; pool allocation unverified; build gated on SM-01 |
| [SM-04](SM-04.md) | Soil tension at three depths plus temperature | Unassigned | ordered; pool allocation unverified; build gated on SM-01 |

## Phase II and proposals

| ID | Purpose | Lifecycle |
|---|---|---|
| [MET-01](MET-01.md) | Davis Vantage Pro2 Plus 6162 meteorological integration through WeatherLink | station reported existing; inventory evidence, matching receiver, network and bench verification pending |
| [WX-CANDIDATE](WX-CANDIDATE.md) | Johan's other proposed weather-station concepts | candidate only |

## Numbering rule

Station IDs describe function. Add the approved site as metadata, and keep the station ID fixed across inventory, firmware, and data history.
