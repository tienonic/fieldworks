# Local runtime acceptance: 2026-08-24

Status: passed for an isolated local test
Owner: unassigned
Validated: 2026-08-24 15:58 PDT
Scope: synthetic data on Citrus WSL, loopback only

This receipt records the local acceptance run after the Citrus WSL teardown. It does not claim a Student Farm deployment, a production data connection, or approval to expose either service beyond loopback.

## Runtime under test

- Grafana OSS 13.1.4, commit `afdab62868c728d60df3f87657e68c8ed6dbb926`;
- Grafana archive SHA-256 `8217002ea098188af18e330d41592cd580c694df56671815a946d7890483d793`;
- InfluxDB OSS 2.9.1, commit `d4fa1941fd`;
- InfluxDB archive SHA-256 `762e4fc825c4386e0c5138e7c3f91fc778081db2bada1ec47066e786bf55d9ff`;
- isolated test bucket, separate bucket-scoped read and write tokens, and no production records;
- Grafana on `127.0.0.1:13000` and InfluxDB on `127.0.0.1:18086`.

The downloaded InfluxDB archive passed its published SHA-256 check and GPG signature check. Docker was not installed, so the pinned Compose definition received static validation only. The same pinned versions were exercised with their official standalone Linux release binaries.

## Acceptance results

| Check | Result |
| --- | --- |
| Environment preflight | Passed with 13 required keys; values were not printed |
| Unit tests | 31 passed |
| Repository validator | Passed for 8 station records and 33 Markdown files |
| Fixture write | 5 synthetic records accepted; HTTP 204 |
| Direct Flux readback | 5 records, 44 fields, 5 station IDs, and 4 source systems |
| Source coverage | `nodeflow_lorawan`, `weatherlink`, `hobo_mx`, and `signalizer` |
| Grafana health | Version 13.1.4; database status `ok` |
| InfluxDB data source | `OK`; one authorized bucket found |
| Provisioned dashboard | Stable UID `student-farm-sensors`; 33 panels |
| Browser acceptance | 5 sections and 27 data panels rendered; station filter and `example_not_live` disclosure passed |
| Browser diagnostics | No missing panels, no no-data section, no query/runtime/console/network error, and no desktop or 390 px page overflow |
| Controlled restart | Both services restarted on the same state directories; all fixture data and provisioning persisted |
| Grafana startup hygiene | No provisioning error and no background plugin install or update activity |

Grafana emitted two internal warnings while registering alpha alerting status resources. They were not provisioning, data source, dashboard, or query failures.

## Data represented

The fixture covered these synthetic station IDs:

- `IH-01`;
- `SM-01`;
- `HOBO-EXAMPLE-01`;
- `IPERL-EXAMPLE-01`;
- `MET-01`.

Every fixture record carried `example_not_live`. The run did not ingest field observations or treat ordered hardware as installed.

## Security and side-effect boundary

- Credentials remained in a mode-600 temporary environment file or process environment and were not written to Git, command arguments, logs, screenshots, or this receipt.
- Anonymous Grafana access, user sign-up, external embedding, telemetry reporting, update checks, plugin administration, background plugin installation, and plugin key retrieval were disabled for the tested Grafana process and in Compose.
- No email, purchase, GitHub push, Google Doc, production service, DNS setting, or vendor record was created or changed.

## Next acceptance gate

Before production use, approve a durable host, accountable owner, retention and backup policy, TLS and firewall boundary, production bucket, source credentials, and one end-to-end physical station test. Repeat this acceptance sequence with the approved production topology and retain a new receipt.
