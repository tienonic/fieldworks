# Data contracts

Status: working
Owner: firmware and data owners unassigned
Updated: 2026-07-27
Evidence: station signal paths and proposed decoded data model

These schema examples show the decoded LoRaWAN payload. Raw values stay beside converted values so calibration errors can be diagnosed.

## Common envelope

Every record includes:

| Field | Meaning |
|---|---|
| `station_id` | stable hardware/data identity such as `IH-01` |
| `station_type` | `irrigation_head`, `soil_profile`, or `met_sandbox` |
| `observed_at` | UTC timestamp in ISO-8601 format |
| `firmware_version` | decoder and field-behavior traceability |
| `battery_v` | node battery voltage when supported by the final pin map |
| `rssi_dbm`, `snr_db` | LoRaWAN link quality from gateway metadata |
| `quality_flags` | explicit warnings such as `uncalibrated`, `stale`, `counter_reset`, or `model_unverified` |

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
  "observed_at": "2026-08-01T18:00:00Z",
  "air_temp_c": null,
  "relative_humidity_pct": null,
  "wind_speed_ms": null,
  "wind_direction_deg": null,
  "cup_wind_speed_ms": null,
  "soil_temp_c": null,
  "quality_flags": ["model_unverified", "bench_only", "example_not_live"]
}
```

Publish MET-01 values only after verifying the physical instruments and conversions.

## Quality behavior

- Preserve raw values with engineering-unit values.
- Use `null` plus a quality flag for unavailable readings. Reserve zero for measured zero.
- Mark counter resets and preserve a counter epoch.
- Label `valve_command` as a controller command.
- Store sensor depths and installation metadata separately from time-series values.
- Reject impossible values at presentation time, but retain the raw record for diagnosis.

The complete field list is in [data-dictionary.csv](data-dictionary.csv).
