# FieldWorks Green Grid Station Network

Station-by-station design record for the FieldWorks Green Grid deployment at the UC Davis Student Farm. This repository shows what each station measures, how every sensor connects to its ENTS node, how data reaches the dashboard, and what still needs to be tested or decided.

> Current design basis: TGIF project `S26-214`, six Phase I field stations, one Phase II meteorological sandbox node, and one LoRaWAN gateway. Site locations are not yet assigned.

## Pick a station

Start with the [visual station atlas](docs/02-stations/station-atlas.md). It treats every station as one physical package: what is installed there, what data it should produce, and what is still blocking it.

| Station | What is physically there | Data you should receive | Readiness |
|---|---|---|---|
| [IH-01](docs/02-stations/IH-01.md) | D10 meter, pressure sensor, controlled-valve path, ENTS box | total gallons, GPM, psi/MPa, valve command, health | reference build; inventory check and bench test needed |
| [IH-02](docs/02-stations/IH-02.md) | second irrigation package | same fields as IH-01 with identity `IH-02` | planned after IH-01 passes |
| [SM-01](docs/02-stations/SM-01.md) | three tension depths, soil temperature, VA3, ENTS box | shallow/middle/deep kPa, soil °C, health | reference build; inventory check and ADC map needed |
| [SM-02](docs/02-stations/SM-02.md) | second soil-profile package | same fields as SM-01 with identity `SM-02` | planned after SM-01 passes |
| [SM-03](docs/02-stations/SM-03.md) | third soil-profile package | same fields as SM-01 with identity `SM-03` | planned after SM-01 passes |
| [SM-04](docs/02-stations/SM-04.md) | fourth soil-profile package | same fields as SM-01 with identity `SM-04` | planned after SM-01 passes |
| [MET-01](docs/02-stations/MET-01.md) | loaned weather instruments connected to seventh ENTS board | air °C, RH%, wind m/s and direction, soil °C if models verify | bench sandbox; model gate open |
| [WX-CANDIDATE](docs/02-stations/WX-CANDIDATE.md) | nothing approved or deployed | no approved stream | concept only |

The Student Farm's four existing Sensus iPERL meters and HOBO MX1104 logger are external systems. They are not counted among the six Phase I ENTS stations. The proposed SCADAmetrics Signalizer is a compatibility-gated pilot, not an approved station component.

## Architecture

![Network architecture](docs/01-architecture/network-overview.svg)

Every field node uses an ENTS board with a Wio-E5 LoRa radio. Nodes send US915 LoRaWAN packets to a Student Farm gateway. The intended data path is gateway → ChirpStack → MQTT → InfluxDB → Grafana and REST/CSV access. The gateway request is pending and cloud/API choices are not final.

## Read in this order

1. [Program overview](docs/00-program/overview.md)
2. [Network architecture](docs/01-architecture/network-overview.md)
3. [Station index](docs/02-stations/README.md)
4. [Station atlas](docs/02-stations/station-atlas.md)
5. [Data contracts and examples](docs/02-stations/data-contracts.md)
6. [Machine-readable data dictionary](docs/02-stations/data-dictionary.csv)
7. [Component specifications](docs/03-hardware/specifications.md)
8. [Machine-readable specifications](docs/03-hardware/component-specifications.csv)
9. [Connection matrix](docs/03-hardware/connection-matrix.csv)
10. [Station bill of materials](docs/03-hardware/station-bom.csv)
11. [Equipment status](docs/04-procurement/orders.md)
12. [Machine-readable equipment status](docs/04-procurement/orders.csv)
13. [What we need](docs/04-procurement/needs.md)
14. [Machine-readable needs register](docs/04-procurement/needs.csv)
15. [Future hardware plan](docs/04-procurement/purchase-list.md)
16. [Machine-readable future hardware plan](docs/04-procurement/purchase-list.csv)
17. [Equipment readiness](docs/04-procurement/status.md)
18. [Assembly and test plan](docs/05-installation/assembly-and-test.md)
19. [Open decisions](docs/07-decisions/open-decisions.md)
20. [Source index](docs/08-sources/source-index.md)

## Evidence rules

- `planned later` means a design may need the item after the reference build passes. It does not mean the item has been ordered or purchased.
- Models marked `unverified` must be checked against the physical label and datasheet before wiring.
- Raw email, receipts, account data, credentials, and private attachments are not stored here.
- Site names and field coordinates remain blank until the Student Farm approves them.

## Repository scope

This repository is the formatted technical and operating record for the station network. It does not replace private financial evidence, raw Gmail messages, the signed TGIF agreement, or source files kept in the protected FieldWorks workspace.
