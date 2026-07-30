# Program Overview

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-07-27
Evidence: signed TGIF project state, proposal narrative, procurement ledger, technical compatibility work

## Current objective

Build and document a six-node Phase I irrigation network at the UC Davis Student Farm:

- two irrigation head stations that measure flow and pressure and provide the hardware path for valve control;
- four soil monitoring stations that measure soil water tension at three depths plus soil temperature;
- one US915 LoRaWAN gateway and an open data path;
- one additional ENTS node reserved for Phase II meteorological sandbox work.

The station network is a FieldWorks proof-of-work asset and TGIF project `S26-214`. The approved award is $8,749.

## Phase boundaries

### Phase I: funded station network

Six ENTS field stations: `IH-01`, `IH-02`, and `SM-01` through `SM-04`.

### Phase II: meteorological sandbox

`MET-01` uses the seventh ENTS board and loaned Biometeorology instruments after exact physical models are verified. It is not one of the six Phase I field nodes.

### Design candidate

`WX-CANDIDATE` records Johan's later high-end and 9-in-1 concepts. These components are not assigned to a funded station.

## What remains unsettled

- Student Farm site names, coordinates, and mounting positions
- proof that completed requests were delivered and accepted
- vendor orders for the July 27 requests
- exact physical identity of the loaned meteorological instruments
- latching-solenoid driver topology
- gateway purchase and final LoRaWAN/network-server deployment
- final public data host and API surface

## Operating boundary

This repository prepares the technical record. Student Farm staff approve locations and installation constraints. The responsible university staff approve purchases. No repository status may bypass those gates.
