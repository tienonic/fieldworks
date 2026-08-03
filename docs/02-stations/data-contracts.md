# Data contracts

Status: working
Owner: firmware and data owners unassigned
Updated: 2026-08-02
Evidence: station signal paths and proposed decoded data model

These schema examples show the normalized station payloads. Raw values stay beside converted values where the acquisition path exposes them so calibration and ingestion errors can be diagnosed.

## Common envelope

Every record includes:

| Field | Meaning |
|---|---|
| `station_id` | stable hardware/data identity such as `IH-01` |
| `station_type` | `irrigation_head`, `soil_profile`, or `met_sandbox` |
| `observed_at` | best available source timestamp in ISO-8601 UTC; for the WeatherLink Live Local API this is the response `ts`, not a per-sensor sample time |
| `quality_flags` | explicit warnings such as `uncalibrated`, `stale`, `counter_reset`, or `receiver_offline` |

ENTS records may additionally include `firmware_version`, `battery_v`, `rssi_dbm`, and `snr_db`. MET-01 is acquired through the Davis/WeatherLink path rather than ENTS/LoRaWAN, so those ENTS-specific fields are not required for MET-01.

## Irrigation-head record

```json
{
  "station_id": "IH-01",
  "station_type": "irrigation_head",
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

## Quality behavior

- Preserve raw values with engineering-unit values where the source exposes useful raw telemetry.
- Use `null` plus a quality flag for unavailable readings. Reserve zero for measured zero.
- Mark counter resets and preserve a counter epoch.
- Label `valve_command` as a controller command.
- Store sensor depths and installation metadata separately from time-series values.
- Preserve the WeatherLink response timestamp and ingestion timestamp separately. Do not claim a per-sensor sample timestamp that the Local API does not provide.
- Reject impossible values at presentation time, but retain the source record for diagnosis.

The complete field list is in [data-dictionary.csv](data-dictionary.csv).
