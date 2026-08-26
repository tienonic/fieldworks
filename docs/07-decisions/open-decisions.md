# Open decisions

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-08-24
Evidence: station documents, protected purchaser state, partial physical inventory, and dashboard acceptance plan

| Priority | Decision | Blocks | Evidence needed | Acceptance test |
|---|---|---|---|---|
| P0 | assign physical ENTS boards to stable station IDs | every build and payload | board inventory/serials | seven boards uniquely mapped |
| P0 | identify and allocate the partially received hardware pool | IH-01 and SM-01 assembly | readable labels, counts, connectors, and station assignment | one complete compatible kit matches each reference BOM |
| P0 | resolve observed D10 `5/8 x 1/2` size against the nominal 3/4-inch design | both irrigation stations | body/port inspection and Student Farm plumbing requirements | approved fittings and leak/pulse test |
| P0 | hold ordered replication hardware until the reference builds pass | IH-02 and SM-02-04 | tested reference designs, complete physical sets, and owner approval | exact hardware allocated only after reference acceptance |
| P0 | choose a bidirectional latching-solenoid driver | irrigation valve control | exact solenoid datasheet and driver design | reliable open/close pulses under battery limits |
| P0 | verify physical MET-01 identity and acquire a matching receiver | meteorological path | dated 6162 label, transmitter region/ID, sensor labels, and receiver SKU | RF pairing and all-channel Local API readback |
| P1 | freeze four soil station sites and depth plan | installation | Student Farm approval and field map | named site and depth record per station |
| P1 | freeze two irrigation sites, pipe sizes, and fittings | installation | Student Farm inspection | meter/valve/fittings BOM per head |
| P1 | verify the ordered US915 gateway model and select sub-band | radio tests | delivered label and network plan | all nodes pass packet-forward and reconnect test |
| P1 | choose production data host | dashboard launch | owner, cost, retention, secrets, backup, recovery, API, and uptime plan | approved source survives end-to-end and restore tests |
| P1 | activate and verify the ordered MX Gateway/API path | external HOBO integration | delivery, account, entitlement, credentials, MX1104 channel map | bounded API read maps into the test dashboard |
| P2 | accept or reject each WX-CANDIDATE instrument | Phase II design | scientific need and exact datasheet | approved station allocation or explicit rejection |
| P2 | decide whether the ordered iPERL Signalizer pilot is compatible | external meter integration | owner approval, installed register/encoder, cable, power, and logger interface | manufacturer-backed compatibility and scaled pulse/analog proof |

## Immediate engineering decision

Resolve the latching-solenoid driver before wiring either irrigation station. Existing records verify voltage compatibility; the two-direction control circuit remains open.
