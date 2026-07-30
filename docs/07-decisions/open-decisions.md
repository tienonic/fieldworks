# Open Decisions

Status: working

Evidence: station documents and current procurement state

| Priority | Decision | Blocks | Evidence needed | Acceptance test |
|---|---|---|---|---|
| P0 | assign physical ENTS boards to stable station IDs | every build and payload | board inventory/serials | seven boards uniquely mapped |
| P0 | prove delivery and exact received SKUs for completed requests | IH-01 and SM-01 assembly | receipts, packing slips, physical labels | BOM matches physical inventory |
| P0 | decide which replication hardware should proceed after the reference builds | IH-02, SM-02–04, GW-01 | tested reference designs and owner approval | final model and quantity per station |
| P0 | choose a bidirectional latching-solenoid driver | irrigation valve control | exact solenoid datasheet and driver design | reliable open/close pulses under battery limits |
| P0 | verify physical MET-01 models and loan terms | meteorological wiring | labels, cables, serials, calibration, return date | revised model-specific connection table |
| P1 | freeze four soil station sites and depth plan | installation | Student Farm approval and field map | named site and depth record per station |
| P1 | freeze two irrigation sites, pipe sizes, and fittings | installation | Student Farm inspection | meter/valve/fittings BOM per head |
| P1 | select US915 gateway and sub-band | radio tests | selected model and network plan | all nodes pass packet-forward test |
| P1 | choose production data host | dashboard launch | owner, cost, retention, API, uptime plan | test data survives end-to-end |
| P2 | accept or reject each WX-CANDIDATE instrument | Phase II design | scientific need and exact datasheet | approved station allocation or explicit rejection |
| P2 | decide whether iPERL Signalizer pilot is compatible | external meter integration | installed register/encoder and cable identity | manufacturer-backed compatibility proof |

## Next engineering decision

Resolve the latching-solenoid driver before wiring either irrigation station. The existing records prove voltage compatibility but do not yet prove a circuit that can command both latch directions safely.
