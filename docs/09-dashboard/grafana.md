# Grafana dashboard

Status: working
Owner: unassigned
Updated: 2026-08-24
Evidence: generated dashboard JSON, provisioned InfluxDB data source, Compose stack, telemetry encoder, automated tests, and the [2026-08-24 local runtime receipt](runtime-acceptance-2026-08-24.md)

The repository contains a local Grafana and InfluxDB stack for the Student Farm sensor network. Static, unit, API, restart, and browser validation passed after the 2026-08-24 Citrus WSL teardown. The proof used exact standalone release binaries because Docker is not installed on this host. The Compose definition is statically validated but was not executed. Do not describe this local test as a deployment or as production-ready.

## Included artifacts

- Grafana image `grafana/grafana:13.1.4`;
- InfluxDB OSS image `influxdb:2.9.1`;
- a generated 33-panel `Student Farm sensors` dashboard;
- a provisioned Flux data source with separate read-token configuration;
- system-health, irrigation, soil, HOBO, Signalizer, and Davis MET-01 sections;
- loopback-only port defaults, disabled anonymous access, disabled background plugin installation and update checks, and bounded container logs;
- a strict telemetry validator and line-protocol encoder;
- synthetic records for all five dashboard source types.

The dashboard source is [build_dashboard.py](../../scripts/build_dashboard.py). Its generated artifact is [student-farm-sensors.json](../../deploy/grafana/dashboards/student-farm-sensors.json). Do not hand-edit the JSON.

## Data behavior

The dashboard queries `station_metrics` through `v.defaultBucket`. It filters by canonical `source_system` and has no embedded token or bucket name. The default time range is 24 hours. Panels remain empty until accepted records exist in that range; startup does not seed data.

The station selector includes all approved station IDs in the selected period. Wind direction uses the latest value instead of an arithmetic mean across north. Valve commands and meter alarms use state panels rather than numeric aggregation.

## Prepare a local test environment

From `deploy/grafana`, copy `.env.example` to an ignored `.env` file and replace every placeholder. Use a test bucket. Keep both bind addresses on loopback.

Validate the file without printing its values:

```bash
python3 ../../scripts/check_grafana_env.py --env-file .env
docker compose --env-file .env config --quiet
```

The admin and Grafana token strings must differ. The Grafana token must also exist in InfluxDB and have read access to the selected bucket; a different string alone does not grant access.

## Start InfluxDB and create the read token

```bash
docker compose --env-file .env up -d influxdb
docker compose --env-file .env ps
```

Use the operator credential through a protected environment or local CLI configuration to create a bucket-scoped read authorization. Put the returned token in `INFLUX_GRAFANA_TOKEN` without printing or committing it. Rerun both preflight commands, then start Grafana:

```bash
docker compose --env-file .env up -d grafana
docker compose --env-file .env ps
```

Open `http://127.0.0.1:3000`. Confirm the `FieldWorks/Student Farm sensors` dashboard loads and the `FieldWorks InfluxDB` data source reports success.

## Validate synthetic data

First verify that the generated dashboard is current and run the tests:

```bash
python3 scripts/build_dashboard.py --check
python3 -m unittest discover -s tests -v
```

The fixture is explicitly non-live. Its fixed source dates fall outside the dashboard's 24-hour window, so shift them during a runtime test:

```bash
INFLUX_TOKEN="$TEST_WRITE_TOKEN" \
python3 scripts/ingest_telemetry.py \
  --input tests/fixtures/telemetry.jsonl \
  --endpoint http://127.0.0.1:8086 \
  --bucket fieldworks_test \
  --shift-examples-to-now \
  --write \
  --confirm-test-data
```

Use a protected environment assignment in actual operation; do not paste a real token into a shared transcript.

Verify these results:

1. `IH-01` appears in flow, pressure, volume, valve-command, battery, and radio panels.
2. `SM-01` appears in three soil-tension series, temperature, battery, and radio panels.
3. `HOBO-EXAMPLE-01` appears in temperature, humidity, light, and analog-input panels.
4. `IPERL-EXAMPLE-01` appears in flow, volume, and meter-alarm panels.
5. `MET-01` appears in temperature, humidity, wind, rainfall, solar, and UV panels.
6. The quality table shows `example_not_live` for every fixture station.

Delete or expire the test bucket before connecting a production data source.

## Connect production sources

1. Approve a production host, owner, retention policy, backup plan, and recovery test.
2. Create separate write and read tokens scoped to the production bucket.
3. Put only the read token in Grafana's `INFLUX_TOKEN` environment path.
4. Normalize NodeFlow, WeatherLink, HOBO, or Signalizer records to [the telemetry schema](telemetry-schema.md).
5. Run one approved source through a test bucket and verify the dashboard readback.
6. Record station ID, source system, firmware or API version, first timestamp, and acceptance receipt.

Do not expose Grafana or InfluxDB beyond loopback until authentication, TLS, firewall, retention, backups, and accountable ownership are approved.

## Runtime acceptance

Runtime verification requires all of these checks:

- the environment preflight and Compose configuration pass without exposing secrets;
- InfluxDB and Grafana report healthy;
- the provisioned data source passes its health check with a read-only bucket token;
- the dashboard loads with no panel, query, browser-console, or provisioning errors;
- all five synthetic source types render in the 24-hour window;
- direct Flux queries return the expected typed fields and tags;
- a controlled restart preserves InfluxDB data and Grafana provisioning;
- no credential appears in Git, logs, screenshots, process arguments, or dashboard JSON.

The latest completed run is recorded in [the local runtime acceptance receipt](runtime-acceptance-2026-08-24.md). Repeat the sequence after changing a version, query, provisioning file, credential boundary, or storage path.

Sources: [Grafana provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/), [Grafana InfluxDB data source](https://grafana.com/docs/grafana/latest/datasources/influxdb/), and [InfluxDB write API](https://docs.influxdata.com/influxdb/v2/api/write-data/).
