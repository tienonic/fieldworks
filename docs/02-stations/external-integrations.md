# External integrations

Status: working
Owner: unassigned
Updated: 2026-08-24
Evidence: manufacturer specifications, protected purchaser-state readback, and existing-system record

The HOBO and iPERL paths are separate from the six ENTS field stations. Their hardware and services are ordered; delivery and activation are unverified. No live dashboard stream is approved until each acceptance sequence passes.

## HOBO MX path

### Physical and network path

`HOBO MX1104 → Bluetooth Low Energy → MXGTW1 → Wi-Fi or Ethernet → LI-COR Cloud/HOBOlink → Web Services V3 → normalizer → InfluxDB → Grafana`

The MX Gateway can communicate with compatible MX loggers over Bluetooth 5.0 at approximately 30.5 m (100 ft) line-of-sight. It uses 2.4/5 GHz Wi-Fi or 10/100 Ethernet for backhaul and can use AC power or Power over Ethernet.

### Dashboard identity and fields

Do not use the physical logger serial as a public station ID. Assign a stable ID such as `HOBO-EXT-01` after inventory, then keep the serial in protected configuration.

The first normalized record can include these fields when the MX1104 channel configuration proves them:

- `air_temp_c`;
- `relative_humidity_pct`;
- `light_lux`;
- `external_analog_raw_v` and a named converted field after the attached sensor is identified;
- `battery_v` when the API returns a supported battery measurement;
- `quality_flags` for stale, missing, out-of-range, or conversion-unverified data.

The Web Services V3 response supplies logger ID, sensor ID, timestamp, data type, SI value, and unit. The adapter must map approved sensor IDs to stable fields. Do not infer a channel from display order.

### Acceptance sequence

1. Verify the delivered gateway model and power accessories.
2. Record the MX1104 label, serial, enabled channels, interval, and existing data ownership.
3. Confirm the gateway and logger use the same cloud account and that gateway upload is enabled.
4. Verify the ordered plan exposes Web Services V3 credentials.
5. Request a bounded time window from the API and save a protected readback receipt.
6. Map each returned sensor ID and unit to the telemetry contract.
7. Send the normalized records to a test bucket before enabling the production bucket.

Sources: [Onset MX Gateway](https://www.onsetcomp.com/products/communications/mxgtw1), [HOBOlink Web Services V3](https://www.onsetcomp.com/resources/documentation/25113-hobolink-web-services-v3-developers-guide).

## iPERL Signalizer pilot

### Physical path

`Sensus iPERL encoder → Signalizer EMP v2 → dry-contact pulse and/or active 4–20 mA → protected logger input → normalizer → InfluxDB → Grafana`

The Signalizer is a signal converter, not an IP gateway. It reads a compatible three-wire encoder register and produces an active 4–20 mA flow signal, a dry-contact volume pulse, and a dry-contact alarm. It requires 9–36 VDC and is IP40, so the installation needs a protected enclosure.

### Dashboard identity and fields

Assign a stable ID such as `IPERL-PILOT-01` only after the exact meter is selected. The normalized record can include:

- `flow_rate_gpm` from the configured 4–20 mA range;
- `pulse_count` and `volume_total_gal` from the configured pulse resolution;
- `meter_alarm` from the alarm contact;
- raw current or input voltage used by the logger;
- `quality_flags` that include meter-not-detected, conversion-unverified, reset, or stale states.

### Electrical rules

- Do not add a loop supply to the active 4–20 mA output.
- Current-limit the dry-contact pulse and alarm circuits.
- Verify the register's digit count, units, scalar, cable wiring, and DIP-switch configuration.
- Keep the utility endpoint pass-through unchanged unless the meter owner approves the exact wiring.

### Acceptance sequence

1. Obtain Student Farm or meter-owner approval for the pilot meter.
2. Photograph and record the meter, register, encoded cable, units, digit count, and existing endpoint.
3. Verify the ordered Signalizer and power supply labels.
4. Choose a protected pulse and/or analog logger interface.
5. Compare indicated volume and timed flow against the meter display over a controlled test.
6. Verify the alarm contact and power-loss pass-through behavior.
7. Send normalized test records to a test bucket before enabling a production stream.

Source: [SCADAmetrics Sensus Signalizer datasheet](https://scadametrics.com/PDF/EMP_v2_SENSUS.pdf).
