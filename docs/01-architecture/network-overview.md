# Network Architecture

Status: working
Owner: unassigned
Updated: 2026-07-27
Evidence: Green Grid proposal, compatibility grid, NodeFlow/ENTS documentation

![Network overview](network-overview.svg)

## Field nodes

Each station uses an ENTS board with an STM32WLE5/Wio-E5 radio. Sensor signals enter through ADC, GPIO, or SPI paths described in the station documents. Firmware converts raw signals into engineering units and encodes a compact payload.

## Radio network

- Region: US915 only
- Intended node class: Class A for low-power sensing
- Possible irrigation command mode: Class C only if the power and control design supports it
- Sub-band: must match the gateway; sub-band 2 is the current working assumption, not a locked setting
- Gateway: US915 unit planned after the location, backhaul, and owner are settled

## Data path

1. ENTS node samples sensors.
2. Wio-E5 sends a LoRaWAN packet.
3. `GW-01` forwards it to ChirpStack.
4. ChirpStack authenticates the device and decodes the payload.
5. MQTT carries decoded observations to InfluxDB.
6. Grafana and REST/CSV access expose reviewed data.

The cloud/API plan is an intended architecture. Hosting and production deployment are not yet verified.

## External systems

Four existing Sensus iPERL meters and a HOBO MX1104 logger remain separate. The SCADAmetrics Signalizer request is held behind a register/cable compatibility check and is not part of the core network diagram.
