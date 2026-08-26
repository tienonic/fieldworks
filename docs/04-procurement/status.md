# Equipment readiness

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-08-24
Evidence: protected purchaser-state readback and partial physical inventory dated 2026-08-20

The hardware pool is partially received, but no complete sensor station is recorded as allocated, bench-accepted, or working.

| Scope | Current equipment state |
|---|---|
| `IH-01` | ENTS board available; D10 and CP075 family hardware observed in shared pool; meter size, pulse switch, SEN0257, solenoid, allocation, and complete bench test open |
| `IH-02` | hardware ordered; shared D10 pool observed; remaining delivery, exact compatibility, allocation, and IH-01 reference gate open |
| `SM-01` | ENTS board available; three bagged soil assemblies observed in shared pool; labels, completeness, allocation, ADC map, and four-channel test open |
| `SM-02`-`SM-04` | hardware ordered; shared pool is not proven complete or allocated; builds remain gated on SM-01 |
| `MET-01` | Davis 6162 is collaborator-reported; dated inventory evidence and matching-region WeatherLink Live remain open; ENTS is not part of this path |
| `GW-01` | RAKwireless US915 unit ordered; exact model, delivery, site, backhaul, owner, and configuration unverified |
| `HOBO-EXT-01` | MX Gateway and plan ordered; delivery, activation, entitlement, credentials, MX1104 upload, and API readback unverified |
| `IPERL-PILOT-01` | Signalizer and power ordered; delivery, owner approval, meter/register/cable compatibility, protected interface, and scaled outputs unverified |
| Dashboard | isolated post-teardown runtime acceptance passed on 2026-08-24; production host, owner, ingestion, backup, and recovery gates remain open |

## Status meanings

- `ordered`: protected purchaser evidence establishes a vendor order.
- `received`: a physical item or readable package was directly observed.
- `shipment_cartons_only`: a shipping label exists but contents were not verified.
- `allocation_unverified`: an item is in a shared pool but is not assigned to a stable station ID.
- `working`: the exact assembled path passed its documented acceptance test.
- `on hold`: no connection or release until a compatibility, ownership, or reference-build gate passes.

Private purchasing evidence remains outside Git. Use [orders.md](orders.md) for the public order-state summary and [physical-inventory.md](physical-inventory.md) for the item-level receiving record.
