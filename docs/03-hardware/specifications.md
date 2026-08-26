# Component specifications

Status: working
Owner: unassigned
Updated: 2026-08-24
Evidence: manufacturer documentation, ENTS hardware documentation, FieldWorks compatibility analysis, protected purchasing state, and partial physical inventory

Use a specification only when the exact physical model matches it. Recheck every value marked `design gate` against the physical label and final selected model.

Open the [manufacturer spec sheet index](spec-sheet-index.md) for direct product pages, manuals, and unresolved model gaps.

## ENTS node

| Field | Specification |
|---|---|
| MCU/radio | STM32WLE5-class ENTS design with Seeed Wio-E5 LoRa module |
| Radio region | US915 |
| LoRaWAN | v1.0.3-capable; Class A baseline |
| Logic | 3.3 V |
| Interfaces | ADC, GPIO, SPI, UART, I2C, and platform SDI-12 support |
| ADC working range | 0-3.3 V; design must stay below absolute input limit |
| Power input | protected 3.7 V LiPo through JST-PH |
| Solar charger | TI BQ24210 path; center-positive barrel input up to 18 V |
| Recommended panel | about 6 V nominal/open-circuit design, at least 1 W |
| Connectors | J1 five-pin and J4 three-pin screw-terminal groups in the documented baseline |
| Gate | inspect each board revision and connector polarity before applying this pin plan |

Sources: [ENTS node hardware](https://github.com/jlab-sensing/ENTS-node-hardware), [ENTS node firmware](https://github.com/jlab-sensing/ENTS-node-firmware).

## D10 water meter and D10-C-SRS pulse switch

| Field | Specification |
|---|---|
| Function | irrigation volume |
| Observed meter | two `D10-NSF-050` units or boxes in the shared hardware pool |
| Observed face marking | `5/8 x 1/2`; reconcile with the plumbing design before allocation |
| Meter family | D10 vertical-installation NSF water meter; family match only |
| Nominal project size | 3/4-inch NPT; final site size is a design gate |
| Pulse switch | D10-C-SRS, SPST normally open dry contact |
| Pulse rate | one pulse per gallon in the selected project configuration |
| Wiring | two conductors: GPIO input and ground |
| ENTS input | GPIO interrupt with internal or external pull-up |
| Sensor power | none for the dry contact |
| Firmware | debounce/count pulses and preserve cumulative count across resets |

The photographed cable does not prove the exact pulse-switch model. Identify a D10-C-SRS label or matching packaging for each meter before relying on the one-pulse-per-gallon conversion.

Sources: [D10 water meter](https://www.flows.com/vertical-installation-nsf-approved-water-meter-d10-series/), [D10 pulse switch](https://www.flows.com/pulse-output-switch-for-d10-water-meters/).

## DFRobot SEN0257 pressure sensor

| Field | Specification |
|---|---|
| Function | water-line pressure |
| Supply | 5 VDC |
| Output | 0.5-4.5 V analog |
| Pressure range | 0-1.6 MPa |
| Thread | G1/4 BSP male; included adapter is also BSP-based |
| ENTS protection | 22 kΩ high side and 47 kΩ low side voltage divider |
| Divided range | about 0.34-3.07 V |
| ENTS input | ADC |
| Mechanical adapter | G1/4 BSP female to 1/4-inch NPT male, selected for the final plumbing |
| Conversion | `pressure_MPa = (ADC_V * 69/47 - 0.5) / 4.0 * 1.6` |

Source: [DFRobot SEN0257 documentation](https://wiki.dfrobot.com/Gravity__Water_Pressure_Sensor_SKU__SEN0257).

## Watermark soil-sensor set

### 200SS-15 soil water tension sensor

| Field | Specification |
|---|---|
| Quantity per soil station | 3 |
| Measurement | soil water tension |
| Native signal | two-wire resistive sensor |
| Project interface | 200SS-VA3 adapter |
| Working depth labels | shallow, middle, deep; exact depths require site approval |
| Cabling | 15-foot project variant in the current BOM |

### 200TS soil temperature sensor

| Field | Specification |
|---|---|
| Quantity per soil station | 1 |
| Measurement | soil temperature |
| Native signal | thermistor path through VA3 |
| Project interface | VA3 temperature channel |

### 200SS-VA3 adapter

| Field | Specification |
|---|---|
| Inputs | 3 x 200SS plus 1 x 200TS |
| Outputs | four independent analog channels |
| Output range | 0-3 VDC |
| ENTS path | four ADC channels |
| Firmware gate | expose the fourth ADC input without losing a required board function |
| Conversion gate | lock the manufacturer voltage-to-tension and voltage-to-temperature formulas during bench calibration |

Sources: [Irrometer sensors](https://www.irrometer.com/sensors.html), [Watermark 200SS](https://www.irrometer.com/200ss.html), [VA adapter documentation](https://www.irrometer.com/pdf/427.pdf).

Three bagged assemblies were physically observed, but the labels and contents were not readable enough to prove three complete Watermark station sets. Count the 200SS-15, 200TS, and 200SS-VA3 components before station allocation.

## Valve and DC-latching actuation

| Field | Specification |
|---|---|
| Phase I function | automated shutoff/control hardware path |
| IH-01 observed path | one CP075 valve body in the shared pool; exact installed or replacement solenoid is a gate |
| IH-02 ordered path | DIG 305DC-075 complete DC valve assembly; not observed in the current photo set |
| Latching supply | commonly 6-12 VDC depending on exact solenoid |
| Node source | 3.7 V battery through a boost stage, nominal 9 V design |
| Control | short open/close pulses only; zero sustained coil power |
| Critical driver requirement | support both latch directions, normally by polarity reversal or the exact manufacturer's required method |
| ENTS path | GPIO command through an isolated transistor, H-bridge, or DPDT relay driver to the solenoid |
| Acceptance | five consecutive open/close cycles at low battery voltage without reset or overheating |

Select the final driver only after the exact solenoid datasheet is attached to the station record.

## Solar, battery, and enclosure

| Field | Specification |
|---|---|
| Solar panel | nominal 6 V class, at least 1 W; exact model still to be verified |
| Charger input | center-positive; below ENTS/BQ24210 18 V maximum |
| Battery | protected 3.7 V LiPo, JST-PH, polarity physically verified |
| Baseline enclosure | Polycase WQ-44 working design; exact delivered SKU unverified |
| WQ-44 internal space | approximately 156 x 110 x 79 mm in the compatibility record |
| Cable entry | drilled PG7/PG9-class glands selected to actual cable diameters |
| Irrigation external cables | solar, D10 pulse, SEN0257, solenoid |
| Soil external cables | solar and bundled VA3/sensor paths |
| Gate | complete fit, condensation, strain-relief, and ingress test with exact parts |

Multiple Polycase enclosures were observed, but their count and SKU remain open. `UN3481` cartons are shipment evidence only; open them and verify battery labels, count, voltage, capacity, connector, protection, and polarity before recording batteries as received.

## Gateway and network

| Field | Specification |
|---|---|
| Gateway ID | GW-01 |
| Ordered unit | RAKwireless US915 gateway; exact model and physical label remain unverified |
| Region | US915 only; reject EU868 substitutions |
| Network server | ChirpStack working architecture |
| Integration | gateway packet forwarder -> ChirpStack -> MQTT |
| Data storage | InfluxDB working architecture |
| Presentation | Grafana plus REST/CSV working architecture |
| Sub-band | match every node; test sub-band 2 against the gateway before locking configuration |
| Acceptance | all seven ENTS nodes join, uplink, reconnect, and preserve unique station identity |

## Ordered external integration paths

These systems remain separate from the six ENTS stations. Vendor-order evidence does not prove delivery, activation, compatibility, or live data.

### HOBO MX Gateway

| Field | Specification |
|---|---|
| Ordered hardware | Onset MX Gateway `MXGTW1` |
| Existing logger | Student Farm HOBO MX1104; serial and active channel configuration unverified |
| Logger link | Bluetooth 5.0 Low Energy; approximately 30.5 m or 100 ft line-of-sight |
| Backhaul | 2.4/5 GHz Wi-Fi or 10/100 Ethernet |
| Power | AC adapter or Power over Ethernet |
| Capacity | up to 100 compatible MX loggers |
| Ordered service | API-capable annual data plan recorded in the protected purchasing thread |
| API | HOBOlink Web Services V3 with OAuth client credentials and JSON observations |
| Gate | verify delivery, account ownership, plan entitlement, MX1104 compatibility and upload, credentials, and one bounded readback |

Sources: [Onset MX Gateway](https://www.onsetcomp.com/products/communications/mxgtw1), [HOBOlink Web Services V3](https://www.onsetcomp.com/resources/documentation/25113-hobolink-web-services-v3-developers-guide).

### iPERL Signalizer pilot

| Field | Specification |
|---|---|
| Ordered hardware | SCADAmetrics Signalizer `EMP v2` plus power adapter |
| Intended meter | one existing Sensus iPERL or iPERL+; exact register and cable unverified |
| Meter input | three-wire Sensus encoder protocol |
| Flow output | active 4-20 mA; do not add an external loop supply |
| Volume output | isolated solid-state dry contact with configured pulse resolution |
| Alarm output | isolated solid-state dry contact |
| Power | 9-36 VDC at about 1.25 W; manufacturer recommends isolated 24 VDC |
| Enclosure | IP40; requires a protected field enclosure |
| Gate | obtain meter-owner approval then verify register, cable, units, scalar, power, protected logger interface, and scaled pulse/analog readback |

Source: [SCADAmetrics Sensus Signalizer datasheet](https://scadametrics.com/PDF/EMP_v2_SENSUS.pdf).

## MET-01 Davis specifications

The collaborator reports a wireless Davis Vantage Pro2 Plus 6162 with `TEMP HUM`, `WIND`, `RAIN`, `SUN`, and `UV` populated. A dated inventory artifact and exact replaceable-sensor labels are still required. MET-01 does not use an ENTS node.

| Component | Signal and power | Data path | Gate |
|---|---|---|---|
| Vantage Pro2 Plus 6162 ISS | solar-powered suite with backup battery and Davis wireless RF | ISS to WeatherLink Live | record label, transmitter ID, condition, channels, and radio region |
| temperature/RH assembly | dedicated `TEMP HUM` interface within ISS | WeatherLink source temperature and RH | verify physical assembly and compare with reference |
| anemometer and vane | dedicated `WIND` interface within ISS | WeatherLink mph and direction degrees | verify revision, mechanical condition, and north alignment |
| rain collector | dedicated `RAIN` interface within ISS | WeatherLink counts plus `rain_size` | verify collector revision, level, tip behavior, and count increment |
| solar sensor | dedicated `SUN` interface within ISS | WeatherLink solar radiation | verify exact label, level, cleanliness, and channel |
| UV sensor | dedicated `UV` interface within ISS | WeatherLink UV index | verify exact label, level, cleanliness, and channel |
| WeatherLink Live | AC with optional AA backup; matching-region Davis RF; Ethernet/Wi-Fi | same-LAN Local API HTTP JSON to adapter | acquire matching region then verify RF, timestamps, units, fields, missing data, and restart behavior |

The adapter maps the Local API response `ts` to `observed_at` and records a separate `received_at`. It converts degrees Fahrenheit to degrees Celsius, miles per hour to meters per second, and rain counts with the reported `rain_size`. It retains the source values for diagnosis. The WeatherLink response timestamp is not a per-sensor sample timestamp.

## Johan WX-CANDIDATE specifications

Most proposed instruments lack exact specifications. The candidate record lists the fields needed for selection.

| Candidate | Known detail | Missing specification |
|---|---|---|
| Campbell TRH probe | temperature/RH role | exact model, outputs, power, accuracy |
| Davis soil-moisture probe | approximate product family | exact model, calibration, ENTS interface |
| Davis 2D sonic anemometer | sonic wind concept | exact variant, output, power, environmental rating |
| bolt-on thermocouple | surface-temperature concept | thermocouple type, range, conditioner |
| Apogee PAR sensor | PAR role | exact model, analog/digital output, calibration |
| soil heat-flux sensor | role only | manufacturer, model, output, installation method |
| two S-LIB-M003 pyranometers | Onset smart-sensor family | logger/interface path and proof of four-stream measurement |
| ultrasonic 9-in-1 RS485 | RS485 concept only | vendor, model, supply, Modbus map, accuracy, ingress and calibration |
