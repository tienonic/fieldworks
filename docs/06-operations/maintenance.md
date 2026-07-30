# Operations and maintenance

Status: working
Owner: unassigned
Updated: 2026-07-27
Evidence: proposal commitments and current station design

## Routine checks

| Interval | Check |
|---|---|
| each dashboard review | missing packets, implausible values, clock drift, battery trend |
| monthly | enclosure seal, cable glands, solar panel, mounting, animal/equipment damage |
| seasonal | sensor comparison, depth/site record, valve operation, gateway connectivity |
| after repair | model/serial, wiring, firmware, calibration, photos, and change record |

## Incident record

For each failure, record the station ID, first and last good timestamp, observed symptom, raw reading or gateway evidence, physical inspection, action, replacement part, verification test, and return-to-service time.

## Data quality

- Keep raw and converted values where practical.
- Mark missing, clipped, out-of-range, maintenance, and calibration periods.
- Leave measured values blank when only an assumption exists.
- Preserve station ID and sensor depth/orientation through every payload and export.

## Access and safety

Keep device credentials, gateway keys, university account data, and private endpoints outside Git. Valve commands require approved authority and a fail-safe procedure. A public dashboard is read-only unless a separate control surface is explicitly designed and approved.

## End of service

Record the final data timestamp, reason, recovered equipment, loan return, safe valve state, removed cable and anchors, and archive location. Remove all enclosures, batteries, sensors, and buried cable from the field.
