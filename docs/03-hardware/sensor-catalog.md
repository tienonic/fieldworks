# Sensor and interface catalog

Status: working
Owner: unassigned
Updated: 2026-08-02
Evidence: manufacturer documentation and FieldWorks compatibility analysis

Exact electrical, mechanical, network, and candidate values are maintained in [Component Specifications](specifications.md), the [manufacturer spec sheet index](spec-sheet-index.md), and [component-specifications.csv](component-specifications.csv).

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

## Phase II meteorology

### Davis Vantage Pro2 Plus 6162

- Function: complete wireless meteorological sensor suite for `MET-01`
- Physical identity: transmitter label verified as Davis Vantage Pro2 Plus product number `6162`
- Installed Sensor Interface Module ports: `TEMP HUM`, `WIND`, `RAIN`, `SUN`, `UV`
- Measurements: air temperature, relative humidity, wind speed, wind direction, rainfall, solar radiation, UV
- Outdoor power: integrated solar-powered ISS with backup battery
- Transport: Davis wireless RF to a compatible Davis receiver
- ENTS path: none; the Davis Sensor Interface Module performs the weather-sensor acquisition

### Vantage Pro2 temperature/RH assembly

- Function: air temperature and relative humidity
- Port: `TEMP HUM`
- Status: installed
- Exact replaceable sensor-board revision: verify from physical hardware before ordering replacement parts

### Davis Vantage Pro2 anemometer / wind vane

- Function: wind speed and direction
- Port: `WIND`
- Current Davis replacement model: `6410`
- Status: installed; inspect cups, vane, bearings, cable, and north alignment
- Manufacturer: [Davis 6410](https://www.davisinstruments.com/products/anemometer-for-vantage-pro2-vantage-pro)

### Davis rain collector

- Function: rainfall and rain rate
- Port: `RAIN`
- Status: installed as part of the 6162 suite
- Exact legacy collector assembly/revision: verify physically before replacement procurement
- Acceptance: level the collector and perform a controlled tip test

### Davis 6450 Solar Radiation Sensor

- Function: solar radiation
- Port: `SUN`
- Status: installed
- Manufacturer: [Davis 6450](https://www.davisinstruments.com/products/solar-radiation-sensor)
- Acceptance: verify level, cleanliness, and WeatherLink channel output

### Davis 6490 UV Sensor

- Function: global solar UV irradiance / UV index
- Port: `UV`
- Status: installed
- Manufacturer: [Davis 6490](https://www.davisinstruments.com/products/uv-sensor)
- Acceptance: verify level, cleanliness, and WeatherLink channel output

### Davis WeatherLink Live 6100

- Function: receive the wireless 6162 station and bridge its observations to the network/software layer
- Input: Davis wireless RF
- Network: Ethernet or 2.4 GHz Wi-Fi
- Local interface: HTTP/JSON WeatherLink Live Local API; real-time UDP is also available
- ENTS path: none
- Status: required for the MET-01 network path; procurement/receiving evidence still needed
- Manufacturer: [WeatherLink Live](https://www.davisinstruments.com/pages/weatherlink-live)
- Developer interface: [WeatherLink Live Local API](https://weatherlink.github.io/weatherlink-live-local-api/)

## Phase II and candidates

See [MET-01](../02-stations/MET-01.md) for the verified Davis meteorological path and [WX-CANDIDATE](../02-stations/WX-CANDIDATE.md) for other unselected concepts.
