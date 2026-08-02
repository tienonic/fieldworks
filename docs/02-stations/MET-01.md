# MET-01: Phase II meteorological sandbox

Status: working
Owner: Johan Marcial Gonzalez; software integration owner unassigned
Updated: 2026-08-02
Evidence: physical Davis Vantage Pro2 Plus transmitter/Sensor Interface Module inspection; Davis Vantage Pro2/Pro2 Plus documentation; Davis sensor documentation; WeatherLink Live documentation
Spec sheets: [baseline instrument index](../03-hardware/spec-sheet-index.md#met-01-baseline)

## Purpose

Use the existing wireless Davis Vantage Pro2 Plus 6162 as the Phase II meteorological station and verify a complete weather-data path from the installed Davis sensors through a compatible Davis receiver into the Green Grid backend before permanent field deployment.

## At a glance

| Physical package | Data product | Question |
|---|---|---|
| Davis Vantage Pro2 Plus 6162 wireless sensor suite plus WeatherLink Live 6100 | air temperature, RH, wind speed/direction, rainfall, solar radiation, UV | Can the existing Davis station provide stable, traceable meteorological observations to the common Green Grid backend? |

## Data expected

| Field | Unit | Source | Current confidence |
|---|---|---|---|
| `air_temp_c` | °C | Vantage Pro2 Plus temperature sensor | high after receiver/reference verification |
| `relative_humidity_pct` | % | Vantage Pro2 Plus humidity sensor | high after receiver/reference verification |
| `wind_speed_ms` | m/s | Davis Vantage Pro2 anemometer | high after mechanical/reference verification |
| `wind_direction_deg` | degree | Davis Vantage Pro2 wind vane | high after north-alignment verification |
| `rain_mm` | mm | Vantage Pro2 rain collector | high after tip/level verification |
| `rain_rate_mm_hr` | mm/h | Vantage Pro2 rain collector / WeatherLink | working; verify field mapping |
| `solar_radiation_wm2` | W/m² | Davis 6450 Solar Radiation Sensor | installed; verify WeatherLink channel |
| `uv_index` | index | Davis 6490 UV Sensor | installed; verify WeatherLink channel |

Use `null` plus a quality flag for unavailable or unverified observations. Do not substitute zero for missing data.

[Full data contract and example payload](data-contracts.md#met-01-record).

![Meteorological sandbox path](../01-architecture/met-sandbox.svg)

## Physical identity gate

The outdoor transmitter label identifies the station as a **Davis Vantage Pro2 Plus, product number 6162**. The Sensor Interface Module is wireless and the `UV`, `SUN`, `RAIN`, `WIND`, and `TEMP HUM` ports are populated.

Before permanent deployment, record the station serial/manufacturing information, transmitter ID, condition, and exact replaceable sensor revisions where labels are accessible.

| Role | Baseline hardware | Port | State |
|---|---|---|---|
| temperature and RH | Vantage Pro2 Plus temperature/RH assembly | `TEMP HUM` | installed; exact internal board revision to verify |
| wind speed/direction | Davis Vantage Pro2 anemometer/wind vane; current replacement SKU 6410 | `WIND` | installed; verify physical condition |
| rainfall | 6162-generation Davis rain collector | `RAIN` | installed; exact collector assembly revision to verify |
| solar radiation | Davis 6450 Solar Radiation Sensor | `SUN` | installed |
| UV | Davis 6490 UV Sensor | `UV` | installed |
| receiver | Davis WeatherLink Live 6100 | Davis wireless RF | required for network/API integration |

## Baseline connection design

| Component | Signal and power | Green Grid path | Extra requirement |
|---|---|---|---|
| Vantage Pro2 Plus 6162 ISS | solar-powered outdoor sensor suite with battery backup; Davis wireless RF | ISS -> WeatherLink Live | verify transmitter ID, battery and RF reception |
| temperature/RH assembly | dedicated Davis sensor connection | `TEMP HUM` -> Sensor Interface Module | verify readings against reference |
| anemometer/wind vane | dedicated Davis wind connection | `WIND` -> Sensor Interface Module | north alignment and mechanical check |
| rain collector | dedicated Davis rain connection | `RAIN` -> Sensor Interface Module | level and tip test |
| Davis 6450 | dedicated Davis solar connection | `SUN` -> Sensor Interface Module | level/clean sensor and verify WeatherLink field |
| Davis 6490 | dedicated Davis UV connection | `UV` -> Sensor Interface Module | level/clean sensor and verify WeatherLink field |
| WeatherLink Live 6100 | AC powered; optional 4x AA backup | Davis RF -> Ethernet/Wi-Fi -> WeatherLink interface | protected powered network location |
| Green Grid adapter | HTTP/JSON software integration | WeatherLink -> MQTT -> InfluxDB -> Grafana | ingestion host and field mapping |

MET-01 does **not** connect its sensors to ENTS ADC/GPIO ports. The Davis Sensor Interface Module performs sensor acquisition, and the completed station transmits over Davis wireless RF to WeatherLink Live.

MET-01 does **not** use the Green Grid LoRaWAN gateway or ChirpStack. The Davis and ENTS acquisition paths converge at the Green Grid backend.

## Resource check

MET-01 needs:

- the existing functioning wireless Vantage Pro2 Plus 6162;
- one WeatherLink Live 6100;
- receiver AC power, with four AA backup batteries recommended;
- Ethernet or compatible Wi-Fi at the receiver location;
- a Green Grid ingestion host able to reach the selected WeatherLink interface;
- a WeatherLink-to-Green-Grid adapter that normalizes observations and publishes them to the common backend;
- suitable mast/mounting hardware and an approved meteorological site.

The seventh ENTS board is not required for MET-01 and can remain available as a spare/development node.

## Acceptance sequence

1. Record the 6162 transmitter label, transmitter ID, installed sensor channels, condition, and available mounting hardware.
2. Inspect the radiation shield, anemometer, wind vane, rain collector, solar panel, 6450 solar sensor, 6490 UV sensor, cables, and connectors.
3. Pair the 6162 with one WeatherLink Live 6100.
4. Verify temperature, RH, wind, rain, solar, and UV channels in WeatherLink.
5. Compare temperature/RH and other practical channels against an available trusted reference and record the comparison.
6. Retrieve WeatherLink observations programmatically and verify sensor identity, timestamps, units, missing-data behavior, and update frequency.
7. Normalize MET-01 observations to the Green Grid data contract and publish them through the common backend.
8. Run the complete Vantage Pro2 -> WeatherLink -> Green Grid path continuously for at least 24 hours before permanent field deployment.

## Field gate

Field plan status: exact mast location, measurement heights, wind fetch, rain-gauge exposure/level, wind-vane north alignment, nearby canopy/building clearance, Davis RF reception, receiver location, network access, maintenance access, and Student Farm approval remain to be recorded before permanent deployment.
