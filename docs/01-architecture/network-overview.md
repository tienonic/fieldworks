# Network architecture

Status: working
Owner: unassigned
Updated: 2026-07-27
Evidence: Green Grid proposal, compatibility grid, NodeFlow/ENTS documentation

![Network overview](network-overview.svg)

## Field nodes

Each station uses an ENTS board with an STM32WLE5/Wio-E5 radio. Sensor signals enter through ADC, GPIO, or SPI paths documented by station. Firmware converts raw signals to engineering units and encodes a compact payload.

## Radio network

- Region: US915 only
- Node class: Class A for low-power sensing
- Possible irrigation command mode: Class C only if the power and control design supports it
- Sub-band: match the gateway; test sub-band 2 before locking the configuration
- Gateway: US915 unit planned after location, backhaul, and owner are settled

## Data path

1. ENTS node samples sensors.
2. Wio-E5 sends a LoRaWAN packet.
3. `GW-01` forwards it to ChirpStack.
4. ChirpStack authenticates the device and decodes the payload.
5. MQTT carries decoded observations to InfluxDB.
6. Grafana and REST/CSV access expose reviewed data.

Hosting and production deployment remain open work.

## External systems

Four existing Sensus iPERL meters and a HOBO MX1104 logger operate separately. The SCADAmetrics Signalizer remains on hold pending a register and cable compatibility check.
