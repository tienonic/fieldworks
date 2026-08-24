# Data contracts

Status: working
Owner: firmware and data owners unassigned
Updated: 2026-08-24
Evidence: station signal paths, WeatherLink Local API contract, external integration specifications, and tested telemetry encoder

These schema examples show the normalized station payloads. Raw values stay beside converted values where the acquisition path exposes them so calibration and ingestion errors can be diagnosed.

## Common envelope

Every record includes:

| Field | Meaning |
|---|---|
| `station_id` | stable hardware/data identity such as `IH-01` |
| `station_type` | `irrigation_head`, `soil_profile`, `met_sandbox`, `external_hobo`, or `external_meter` |
| `source_system` | canonical acquisition path: `nodeflow_lorawan`, `weatherlink`, `hobo_mx`, or `signalizer` |
| `observed_at` | best available source timestamp in ISO-8601 UTC; for the WeatherLink Live Local API this is the response `ts`, not a per-sensor sample time |
| `quality_flags` | explicit warnings such as `uncalibrated`, `stale`, `counter_reset`, or `receiver_offline` |

ENTS records may additionally include `firmware_version`, `battery_v`, `rssi_dbm`, and `snr_db`. MET-01 is acquired through the Davis/WeatherLink path rather than ENTS/LoRaWAN, so those ENTS-specific fields are not required for MET-01.

## Irrigation-head record

```json
{
  "station_id": "IH-01",
  "station_type": "irrigation_head",
  "source_system": "nodeflow_lorawan",
  "observed_at": "2026-08-01T18:00:00Z",
  "flow": {
    "pulse_count": 1042,
    "volume_total_gal": 1042,
    "flow_rate_gpm": 8.0
  },
  "pressure": {
    "raw_v": 1.09,
    "mpa": 0.44,
    "psi": 63.8
  },
  "valve": {
    "command": "open",
    "pulse_ms": 80,
    "position_feedback_available": false
  },
  "firmware_version": "example-only",
  "battery_v": 3.91,
  "rssi_dbm": -92,
  "snr_db": 7.5,
  "quality_flags": ["example_not_live"]
}
```

In this example, the counter shows 1,042 gallons, recent flow is 8.0 gpm, line pressure is 63.8 psi, and the controller last commanded the valve open. `valve_command` records the request; the station has no position sensor.

## Soil-profile record

```json
{
  "station_id": "SM-01",
  "station_type": "soil_profile",
  "source_system": "nodeflow_lorawan",
  "observed_at": "2026-08-01T18:00:00Z",
  "depths_cm": {
    "shallow": null,
    "middle": null,
    "deep": null
  },
  "soil_tension_kpa": {
    "shallow": 18.0,
    "middle": 31.0,
    "deep": 46.0
  },
  "raw_v": {
    "shallow": 1.10,
    "middle": 1.55,
    "deep": 2.02,
    "temperature": 1.31
  },
  "soil_temp_c": 22.4,
  "firmware_version": "example-only",
  "battery_v": 3.88,
  "rssi_dbm": -101,
  "snr_db": 4.0,
  "quality_flags": ["example_not_live", "depths_not_assigned"]
}
```

The illustrative record gets drier with depth. Depth values stay null until the Student Farm approves the installation plan.

## MET-01 record

```json
{
  "station_id": "MET-01",
  "station_type": "met_sandbox",
  "source_system": "weatherlink",
  "observed_at": "2026-08-01T18:00:00Z",
  "received_at": "2026-08-01T18:00:04Z",
  "air_temp_c": null,
  "relative_humidity_pct": null,
  "wind_speed_ms": null,
  "wind_direction_deg": null,
  "rainfall_daily_mm": null,
  "rain_rate_mm_hr": null,
  "solar_radiation_wm2": null,
  "uv_index": null,
  "source_values": {
    "temp_f": null,
    "wind_speed_mph": null,
    "rain_size": null,
    "rainfall_daily_counts": null,
    "rain_rate_counts_per_hr": null
  },
  "quality_flags": ["bench_only", "example_not_live", "source_timestamp_not_sample_time"]
}
```

MET-01 is the Davis Vantage Pro2 Plus 6162 weather path. Publish the weather fields after the 6162 is paired with a matching-region WeatherLink Live receiver and the corresponding channels are verified. For the Local API, map response `ts` to `observed_at` and flag that it is not a per-sensor sample time; `received_at` records when Green Grid ingested the response.

The Local API exposes temperature in °F, wind speed in mph, and rain as counts plus a `rain_size` code. The adapter converts temperature with `(°F - 32) × 5/9`, wind with `mph × 0.44704`, and rain counts using the collector size declared by `rain_size`. `rainfall_daily_mm` is the daily count since local midnight after that conversion. Retain the source values beside the normalized values.

## External HOBO record

```json
{
  "station_id": "HOBO-EXAMPLE-01",
  "station_type": "external_hobo",
  "source_system": "hobo_mx",
  "observed_at": "2026-08-01T18:00:30Z",
  "air_temp_c": 24.2,
  "relative_humidity_pct": 51.0,
  "light_lux": 18400.0,
  "external_analog_raw_v": 1.42,
  "battery_v": 2.98,
  "quality_flags": ["channel_mapping_unverified", "example_not_live"]
}
```

Map an approved HOBOlink sensor ID and SI unit to each public field. Keep logger and sensor serials in protected configuration.

## External iPERL pilot record

```json
{
  "station_id": "IPERL-EXAMPLE-01",
  "station_type": "external_meter",
  "source_system": "signalizer",
  "observed_at": "2026-08-01T18:00:40Z",
  "flow_rate_gpm": 7.5,
  "pulse_count": 258,
  "volume_total_gal": 258.0,
  "meter_alarm": false,
  "signalizer_current_ma": 12.0,
  "logger_input_v": 2.4,
  "quality_flags": ["compatibility_unverified", "example_not_live"]
}
```

The numeric values are synthetic. Publish this shape only after the meter/register, pulse resolution, active 4-20 mA range, logger scaling, and alarm polarity pass the documented pilot test.

## Quality behavior

- Preserve raw values with engineering-unit values where the source exposes useful raw telemetry.
- Use `null` plus a quality flag for unavailable readings. Reserve zero for measured zero.
- Mark counter resets and preserve a counter epoch.
- Label `valve_command` as a controller command.
- Store sensor depths and installation metadata separately from time-series values.
- Preserve the WeatherLink response timestamp and ingestion timestamp separately. Do not claim a per-sensor sample timestamp that the Local API does not provide.
- Use `source_system` as the canonical source tag. `data_source` is a temporary ingestion alias only.
- Keep station identity, type, and acquisition path consistent; reject unknown fields instead of silently dropping them.
- Reject impossible values at presentation time, but retain the source record for diagnosis.

The complete field list and stable storage types are in [data-dictionary.csv](data-dictionary.csv). The InfluxDB mapping and write controls are in [the dashboard telemetry schema](../09-dashboard/telemetry-schema.md).
