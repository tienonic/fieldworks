# Network architecture

Status: working
Owner: unassigned
Updated: 2026-08-24
Evidence: Green Grid proposal, compatibility grid, NodeFlow/ENTS documentation, procurement readback, and dashboard artifacts

![Network overview](network-overview.svg)

## Field nodes

Each station uses an ENTS board with an STM32WLE5/Wio-E5 radio. Sensor signals enter through ADC, GPIO, or SPI paths documented by station. Firmware converts raw signals to engineering units and encodes a compact payload.

## Radio network

- Region: US915 only
- Node class: Class A for low-power sensing
- Possible irrigation command mode: Class C only if the power and control design supports it
- Sub-band: match the gateway; test sub-band 2 before locking the configuration
- Gateway: a US915 unit is ordered; exact model, delivery, location, backhaul, and owner remain unsettled

## Data path

1. ENTS node samples sensors.
2. Wio-E5 sends a LoRaWAN packet.
3. `GW-01` forwards it to ChirpStack.
4. ChirpStack authenticates the device and decodes the payload.
5. MQTT carries decoded observations to InfluxDB.
6. Grafana and REST/CSV access expose reviewed data.

The repository contains a provisioned local InfluxDB and Grafana stack. Isolated post-teardown runtime acceptance passed on 2026-08-24. Upstream ingestion, production hosting, backups, and ownership remain open.

## External systems

Four existing Sensus iPERL meters and a HOBO MX1104 logger operate separately. An MX Gateway/API plan and one Signalizer pilot are ordered. They remain behind delivery, activation, account, register, cable, power, and interface gates. See [External integrations](../02-stations/external-integrations.md).
