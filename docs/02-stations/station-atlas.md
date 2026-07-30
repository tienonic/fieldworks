# Station Atlas

Status: working

Evidence: station BOMs, connection matrix, specifications, and proposed data contracts

Use this page as the human interface to the network. Each station is one physical package with one stable ID, one list of things inside it, and one expected data product.

![Station atlas](station-atlas.svg)

## Phase I station cards

### IH-01 — first irrigation head

**What it is:** one weatherproof box and instrument set mounted at one irrigation head.

**Inside and attached:**

- 1 × ENTS node with Wio-E5 US915 radio
- 1 × D10 meter with D10-C-SRS pulse switch
- 1 × SEN0257 pressure sensor
- 1 × valve and DC-latching solenoid path
- voltage divider, boost converter, bidirectional driver, battery, solar, enclosure, and cable fittings

**Data expected:**

- total irrigation volume in gallons
- flow rate in gallons per minute
- line pressure in psi and MPa
- commanded valve state: `open`, `closed`, or `unknown`
- raw pulse and pressure values for diagnosis
- timestamp, station ID, firmware version, radio quality, and power telemetry when supported

**What it answers:** How much water passed this head, at what pressure, and what did the controller ask the valve to do?

**Current state:** first reference irrigation build; the physical package needs inventory confirmation and bench verification.

[Open the complete IH-01 record](IH-01.md)

---

### IH-02 — second irrigation head

**What it is:** a replica of IH-01 at a second approved irrigation head.

**Inside and attached:** same functional package as IH-01, using the second D10, second SEN0257, and complete valve assembly after the IH-01 design passes.

**Data expected:** the same volume, flow, pressure, valve-command, diagnostic, power, and radio fields as IH-01, always carrying station ID `IH-02`.

**What it answers:** How does a second irrigation head perform, and how does its water delivery compare with IH-01?

**Current state:** planned for later; do not replicate until IH-01 passes.

[Open the complete IH-02 record](IH-02.md)

---

### SM-01 — first soil profile

**What it is:** one weatherproof box connected to four probes at one approved field location.

**Inside and attached:**

- 1 × ENTS node with Wio-E5 US915 radio
- 3 × Watermark 200SS tension sensors labeled shallow, middle, and deep
- 1 × Watermark 200TS soil-temperature sensor
- 1 × 200SS-VA3 four-channel adapter
- battery, solar, enclosure, glands, and labeled probe cables

**Data expected:**

- soil water tension in kPa at shallow, middle, and deep depths
- soil temperature in °C
- four raw adapter voltages for diagnosis
- timestamp, station ID, firmware version, radio quality, and power telemetry when supported

**What it answers:** Where is the soil profile drying, how quickly, and under what soil temperature?

**Current state:** first reference soil build; the physical package needs inventory confirmation and a frozen four-channel ADC map.

[Open the complete SM-01 record](SM-01.md)

---

### SM-02 — second soil profile

**What it is:** the SM-01 package at a second approved field location.

**Data expected:** shallow, middle, and deep tension plus soil temperature, identified as `SM-02`.

**What it answers:** How does the second location's root-zone water profile compare with SM-01?

**Current state:** planned for later after the reference build passes.

[Open the complete SM-02 record](SM-02.md)

---

### SM-03 — third soil profile

**What it is:** the SM-01 package at a third approved field location.

**Data expected:** shallow, middle, and deep tension plus soil temperature, identified as `SM-03`.

**What it answers:** How does the third location differ in drying rate and depth distribution?

**Current state:** planned for later after the reference build passes.

[Open the complete SM-03 record](SM-03.md)

---

### SM-04 — fourth soil profile

**What it is:** the SM-01 package at a fourth approved field location.

**Data expected:** shallow, middle, and deep tension plus soil temperature, identified as `SM-04`.

**What it answers:** How does the fourth location differ, and does the four-station pattern show meaningful spatial variation?

**Current state:** planned for later after the reference build passes.

[Open the complete SM-04 record](SM-04.md)

## Phase II card

### MET-01 — meteorological integration sandbox

**What it is:** the seventh ENTS board on a bench, connected one instrument at a time before any field mast is approved.

**Candidate attached instruments:** temperature/RH probe, wind speed/direction monitor, cup anemometer, and soil-temperature sensor. Exact physical models remain disputed.

**Data expected if the April 19 baseline is verified:**

- air temperature in °C
- relative humidity in percent
- wind speed in m/s
- wind direction in degrees
- second/cup wind-speed channel in m/s
- soil temperature in °C
- raw analog, pulse, and RTD values plus station-health fields

**What it answers:** Can the loaned meteorological instruments be powered, read, calibrated, and sent through ENTS without buying a separate station?

**Current state:** blocked until every physical model and cable is identified.

[Open the complete MET-01 record](MET-01.md)

## Design candidate

### WX-CANDIDATE — Johan weather concept

This is not a physical station and produces no approved data stream. It is a holding record for proposed instruments until exact models, scientific questions, interfaces, and overlap are decided.

[Open the candidate record](WX-CANDIDATE.md)

## Reading the data

- [Data contracts and example records](data-contracts.md)
- [Machine-readable data dictionary](data-dictionary.csv)
- [Network and storage path](../01-architecture/network-overview.md)
- [Connection matrix](../03-hardware/connection-matrix.csv)
