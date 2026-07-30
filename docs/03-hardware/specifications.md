# Component specifications

Status: working
Owner: unassigned

Evidence: manufacturer documentation, ENTS hardware documentation, and FieldWorks compatibility analysis

Use a specification only when the exact physical model matches it. Recheck every value marked `design gate` against the physical label and final selected model.

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
| Meter family | D10 vertical-installation NSF water meter |
| Nominal project size | 3/4-inch NPT; final site size is a design gate |
| Pulse switch | D10-C-SRS, SPST normally open dry contact |
| Pulse rate | one pulse per gallon in the selected project configuration |
| Wiring | two conductors: GPIO input and ground |
| ENTS input | GPIO interrupt with internal or external pull-up |
| Sensor power | none for the dry contact |
| Firmware | debounce/count pulses and preserve cumulative count across resets |

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

## Valve and DC-latching actuation

| Field | Specification |
|---|---|
| Phase I function | automated shutoff/control hardware path |
| IH-01 recorded path | CP075 valve plus received-solenoid replacement path; exact received model is a gate |
| IH-02 requested path | DIG 305DC-075 complete DC valve assembly |
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

## Gateway and network

| Field | Specification |
|---|---|
| Gateway ID | GW-01 |
| Planned unit | US915 gateway; exact model still to be selected |
| Region | US915 only; reject EU868 substitutions |
| Network server | ChirpStack working architecture |
| Integration | gateway packet forwarder -> ChirpStack -> MQTT |
| Data storage | InfluxDB working architecture |
| Presentation | Grafana plus REST/CSV working architecture |
| Sub-band | match every node; test sub-band 2 against the gateway before locking configuration |
| Acceptance | all seven ENTS nodes join, uplink, reconnect, and preserve unique station identity |

## MET-01 baseline specifications

Treat these as wiring baselines. Verify inventory against physical labels.

| Baseline model | Measurement | Signal | Power | ENTS path | Gate |
|---|---|---|---|---|---|
| Campbell EE181-L | air temperature and RH | two 0-1 V analog outputs | 7-30 VDC, under about 1.2 mA | two ADC channels; filtered 12 V boost | verify exact label/suffix |
| Campbell 05103 | wind speed and direction | AC/pulse speed plus ratiometric direction voltage | 5 V direction excitation; passive speed | GPIO counter plus ADC | later evidence says Met One sensors |
| Campbell 014A-L | cup-anemometer speed | pulse/frequency | passive | GPIO counter | later evidence says Met One cup sensor |
| T-PRO TD0030 PT100 | soil temperature | three-wire PT100 resistance | passive | MAX31865 to SPI | later evidence disputes PT100/soil use |

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
