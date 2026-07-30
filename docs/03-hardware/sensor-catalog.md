# Sensor and interface catalog

Status: working
Owner: unassigned
Updated: 2026-07-27
Evidence: manufacturer documentation and FieldWorks compatibility analysis

Exact electrical, mechanical, network, and candidate values are maintained in [Component Specifications](specifications.md) and [component-specifications.csv](component-specifications.csv).

## Phase I instruments

### D10 water meter with D10-C-SRS

- Function: irrigation volume
- Output: two-wire dry-contact reed switch
- Rate: one pulse per gallon in the selected configuration
- ENTS path: GPIO interrupt with pull-up
- Power: none for the contact
- Mechanical gate: confirm exact NPT size and installation orientation

### DFRobot SEN0257

- Function: water pressure
- Supply: 5 V
- Output: 0.5-4.5 V analog
- ENTS path: 22 kΩ/47 kΩ divider to ADC, producing about 0.34-3.07 V
- Mechanical gate: G1/4 BSP to NPT adapter
- Firmware: restore divider ratio, subtract sensor offset, and scale to pressure

### Watermark 200SS-15 and 200TS through 200SS-VA3

- Function: three soil-tension depths plus soil temperature
- Adapter output: four independent 0-3 V analog channels
- ENTS path: four ADC channels
- Firmware gate: expose a fourth channel without silently losing required battery/peripheral functions

### DC latching valve assembly

- Function: irrigation shutoff/control hardware path
- Supply: boosted pulse, nominally 6-12 V depending on the exact solenoid
- ENTS path: GPIO to a driver stage
- Critical gate: confirm bidirectional latch control. A single relay works only if the complete circuit supports both directions.

## Node and power

### ENTS / Wio-E5

- Logic: 3.3 V
- Interfaces: ADC, GPIO, SPI, UART, I2C, SDI-12 support in platform
- Radio: LoRaWAN US915
- Charger: BQ24210 through center-positive barrel input, up to 18 V
- Battery: protected 3.7 V LiPo with verified JST-PH polarity

## Phase II and candidates

See [MET-01](../02-stations/MET-01.md) for the model-conflicted loan inventory and [WX-CANDIDATE](../02-stations/WX-CANDIDATE.md) for Johan's unselected proposals.
