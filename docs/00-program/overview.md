# Program overview

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-08-24
Evidence: signed TGIF project state, proposal narrative, procurement ledger, physical inventory checklist, and technical compatibility work

## Current objective

Build and document a six-node Phase I irrigation network at the UC Davis Student Farm:

- two irrigation head stations that measure flow and pressure and provide the hardware path for valve control;
- four soil monitoring stations that measure soil water tension at three depths plus soil temperature;
- one ordered but unverified US915 LoRaWAN gateway and an open data path;
- one additional ENTS node retained as a spare or development node.

The station network is a FieldWorks proof-of-work asset and TGIF project `S26-214`. The approved award is $8,749.

## Phase boundaries

### Phase I: funded station network

Six ENTS field stations: `IH-01`, `IH-02`, and `SM-01` through `SM-04`.

### Phase II: meteorological sandbox

`MET-01` is the reported wireless Davis Vantage Pro2 Plus 6162 path. It uses a matching-region WeatherLink Live receiver and does not use an ENTS node, the LoRaWAN gateway, or ChirpStack. The seventh ENTS board remains a spare or development node.

### Design candidate

`WX-CANDIDATE` records Johan's later high-end and 9-in-1 concepts outside the funded station set.

## Open items

- Student Farm site names, coordinates, and mounting positions
- exact labels, completeness, and station allocation for the partially observed hardware pool
- delivery and receiving evidence for ordered items not observed in the physical inventory
- dated physical evidence for the reported Davis 6162 and a matching-region WeatherLink Live receiver
- latching-solenoid driver topology
- exact gateway model and final LoRaWAN/network-server deployment
- MX Gateway/data-plan activation and Signalizer compatibility
- production data host, secret owner, backup plan, and public API surface

## Operating boundary

This repository holds the technical record. Student Farm staff approve locations and installation constraints. Responsible university staff approve purchases. Repository status cannot bypass those gates.
