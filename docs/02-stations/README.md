# Station index

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-08-02
Evidence: proposal architecture, compatibility grid, procurement evidence, physical Davis 6162 inspection, and current station records

## Start with the station atlas

[Open the Station Atlas](station-atlas.md) for each station package, its expected data, its field question, and its deployment blockers.

- [Data contracts and example records](data-contracts.md)
- [Machine-readable data dictionary](data-dictionary.csv)

## Phase I field stations

| ID | Purpose | Site | Lifecycle |
|---|---|---|---|
| [IH-01](IH-01.md) | Irrigation flow, pressure, and valve-control path | Unassigned | bench build blocked on inventory/delivery proof |
| [IH-02](IH-02.md) | Second irrigation head | Unassigned | procurement requests submitted; receiving/bench verification pending |
| [SM-01](SM-01.md) | Soil tension at three depths plus temperature | Unassigned | bench build blocked on inventory/delivery proof |
| [SM-02](SM-02.md) | Soil tension at three depths plus temperature | Unassigned | procurement request submitted; receiving pending |
| [SM-03](SM-03.md) | Soil tension at three depths plus temperature | Unassigned | procurement request submitted; receiving pending |
| [SM-04](SM-04.md) | Soil tension at three depths plus temperature | Unassigned | procurement request submitted; receiving pending |

## Phase II and proposals

| ID | Purpose | Lifecycle |
|---|---|---|
| [MET-01](MET-01.md) | Davis Vantage Pro2 Plus 6162 meteorological integration through WeatherLink | station reported existing; inventory evidence, matching receiver, network and bench verification pending |
| [WX-CANDIDATE](WX-CANDIDATE.md) | Johan's other proposed weather-station concepts | candidate only |

## Numbering rule

Station IDs describe function. Add the approved site as metadata, and keep the station ID fixed across inventory, firmware, and data history.
