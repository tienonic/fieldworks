# Dashboard telemetry schema

Status: working
Owner: unassigned
Updated: 2026-08-24
Evidence: station data contracts, WeatherLink Local API contract, external-system specifications, telemetry encoder tests, and Grafana Flux queries

Store accepted observations in the InfluxDB measurement `station_metrics`. Tags identify the station and acquisition path. Fields hold measurements, diagnostics, quality state, and health values.

## Tags

Every stored point has these tags:

| Tag | Meaning | Accepted values |
|---|---|---|
| `station_id` | stable public station identity | core IDs or an approved `HOBO-` or `IPERL-` ID; never a protected device serial |
| `station_type` | record shape | `irrigation_head`, `soil_profile`, `met_sandbox`, `external_hobo`, or `external_meter` |
| `source_system` | acquisition path | `nodeflow_lorawan`, `weatherlink`, `hobo_mx`, or `signalizer` |

`source_system` is canonical. The encoder accepts `data_source` only as a migration alias and rejects a record when both names are present with different values. It emits only `source_system`.

## Common fields

The encoder adds these fields to every stored point:

| Field | InfluxDB type | Meaning |
|---|---|---|
| `record_count` | integer | always `1`; used to count reporting stations |
| `quality_flag_count` | integer | number of unique input quality flags |
| `quality_state` | string | sorted comma-delimited flags, or `ok` |

It stores `firmware_version` as a string and `battery_v`, `rssi_dbm`, and `snr_db` as floats when a source provides them. Measurement values are always floats, even when an input JSON number is integral. Counters, pulse durations, source codes, and source counts are integers. Alarm and feedback-availability fields are Boolean. This rule prevents InfluxDB field-type conflicts.

## Irrigation fields

| Field | Type | Unit | Source |
|---|---|---|---|
| `pulse_count` | integer | count | D10-C-SRS dry-contact pulses |
| `volume_total_gal` | float | gallon | verified pulse conversion |
| `flow_rate_gpm` | float | gallon/minute | pulse change divided by elapsed time |
| `pressure_raw_v` | float | volt | divided SEN0257 signal |
| `pressure_mpa` | float | MPa | calibrated SEN0257 conversion |
| `pressure_psi` | float | psi | MPa converted to psi |
| `valve_command` | string | enum | `open`, `closed`, or `unknown` |
| `valve_pulse_ms` | integer | millisecond | requested latching pulse duration |
| `valve_position_feedback_available` | Boolean | none | whether a physical position sensor exists |

`valve_command` is a controller request. It is not proof of valve position.

## Soil fields

| Field | Type | Unit |
|---|---|---|
| `tension_shallow_kpa` | float | kPa |
| `tension_middle_kpa` | float | kPa |
| `tension_deep_kpa` | float | kPa |
| `tension_shallow_raw_v` | float | volt |
| `tension_middle_raw_v` | float | volt |
| `tension_deep_raw_v` | float | volt |
| `soil_temp_raw_v` | float | volt |
| `soil_temp_c` | float | degree Celsius |

Keep approved depths and coordinates in protected station metadata. The encoder rejects non-null `depths_cm` values in time-series input.

## MET-01 WeatherLink fields

Use `station_type=met_sandbox` and `source_system=weatherlink`.

| Field | Type | Unit or meaning |
|---|---|---|
| `air_temp_c` | float | degree Celsius |
| `relative_humidity_pct` | float | percent |
| `wind_speed_ms` | float | meter/second |
| `wind_direction_deg` | float | degree |
| `rainfall_daily_mm` | float | millimeter since local midnight |
| `rain_rate_mm_hr` | float | millimeter/hour |
| `solar_radiation_wm2` | float | watt/meter^2 |
| `uv_index` | float | UV index |
| `received_at` | string | UTC ingestion timestamp |
| `ingest_latency_s` | float | `received_at - observed_at` in seconds |
| `source_temp_f` | float | retained WeatherLink temperature |
| `source_wind_speed_mph` | float | retained WeatherLink wind speed |
| `source_rain_size_code` | integer | retained collector-size code |
| `source_rainfall_daily_counts` | integer | retained daily rain count |
| `source_rain_rate_counts_per_hr` | integer | retained rain-rate count |

Map the WeatherLink response `ts` to `observed_at`. It is a response timestamp, not a per-sensor sample time, so every WeatherLink record must carry `source_timestamp_not_sample_time`. `received_at` must not precede `observed_at`.

Convert temperature with `(temp_f - 32) * 5/9` and wind with `wind_speed_mph * 0.44704`. Convert rain counts with the collector increment declared by `rain_size`. Keep the source values beside the converted values. If `model_unverified` is present, the encoder rejects every non-null MET engineering or source value.

## HOBO fields

Use `station_type=external_hobo` and `source_system=hobo_mx`.

| Field | Type | Unit | Gate |
|---|---|---|---|
| `air_temp_c` | float | degree Celsius | verified MX1104 channel and API unit |
| `relative_humidity_pct` | float | percent | verified MX1104 channel and API unit |
| `light_lux` | float | lux | verified MX1104 channel and API unit |
| `external_analog_raw_v` | float | volt | verified external channel and API unit |

Retain the API timestamp in UTC. Keep client credentials, cloud user ID, logger and sensor serials, and incremental-query cursor outside Git.

## Signalizer fields

Use `station_type=external_meter` and `source_system=signalizer`.

| Field | Type | Unit | Gate |
|---|---|---|---|
| `flow_rate_gpm` | float | gallon/minute | verified 4-20 mA range and logger scaling |
| `pulse_count` | integer | count | debounced dry-contact input |
| `volume_total_gal` | float | gallon | verified pulse resolution and reset boundary |
| `meter_alarm` | Boolean | none | verified alarm-contact polarity |
| `signalizer_current_ma` | float | milliampere | retained active-loop reading |
| `logger_input_v` | float | volt | retained logger input used for scaling |

Compare total volume and timed flow with the physical meter before accepting the stream.

## Validate input

The ingestion script accepts one JSON object, a JSON array, or JSON Lines:

```bash
python3 scripts/ingest_telemetry.py --input path/to/records.jsonl
```

Dry run is the default. It validates the records and prints InfluxDB line protocol without writing data. Unknown top-level or nested fields, invalid station/type/source combinations, wrong scalar types, and empty records fail validation.

The repository fixture is synthetic and older than the dashboard's default 24-hour window. Shift it while preserving the relative timestamps when testing a live stack:

```bash
python3 scripts/ingest_telemetry.py \
  --input tests/fixtures/telemetry.jsonl \
  --shift-examples-to-now
```

## Write controls

An InfluxDB write reads its token from `INFLUX_TOKEN` by default. Keep the token out of command arguments and shell history.

Plain HTTP writes are accepted only for a loopback endpoint. Use HTTPS for a remote InfluxDB service. The endpoint URL must not contain credentials, a query, or a fragment, and the writer rejects redirects so the token stays on the selected endpoint.

Example records require both a test bucket and an explicit confirmation:

```bash
python3 scripts/ingest_telemetry.py \
  --input tests/fixtures/telemetry.jsonl \
  --bucket fieldworks_test \
  --shift-examples-to-now \
  --write \
  --confirm-test-data
```

A non-test bucket requires `--confirm-production`. Synthetic data cannot be written to a non-test bucket even with that flag.

## Quality rules

- Use null or omit a field when no accepted value exists. Do not use zero for missing data.
- Add `example_not_live` to every synthetic or illustrative record.
- Add `model_unverified` when the physical model or conversion is not accepted.
- Preserve reset boundaries for cumulative counters.
- Retain rejected source records in a protected diagnostic store.
- Never use an account, device serial, credential, or precise protected location as a public tag.

Sources: [InfluxDB line protocol](https://docs.influxdata.com/influxdb/cloud/write-data/developer-tools/line-protocol/), [Grafana Flux macros](https://grafana.com/docs/grafana/latest/datasources/influxdb/query-editor/), [WeatherLink Live Local API](https://weatherlink.github.io/weatherlink-live-local-api/), [HOBOlink Web Services V3](https://www.onsetcomp.com/resources/documentation/25113-hobolink-web-services-v3-developers-guide), and [Signalizer Sensus datasheet](https://scadametrics.com/PDF/EMP_v2_SENSUS.pdf).
