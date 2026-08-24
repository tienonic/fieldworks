# What we still need

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-08-24
Evidence: station acceptance gates, protected order-state readback, and partial physical inventory

Do not buy from this page. First identify the shared hardware pool, allocate complete reference kits, and bench-test IH-01 and SM-01. Only a verified deficit can become a new purchase request.

## IH-01 reference build

Before assembly:

- resolve the observed `D10-NSF-050` `5/8 x 1/2` marking against the nominal 3/4-inch plumbing design;
- identify an exact D10-C-SRS switch and verify pulse resolution;
- locate and verify one SEN0257 plus the BSP-to-NPT fitting and 22 kOhm/47 kOhm divider;
- allocate the CP075 body, identify its exact latching solenoid, and select a bidirectional pulse driver;
- allocate one compatible enclosure, solar panel, protected LiPo, glands, vents, and fittings;
- pass leak, measured-volume, pressure-reference, valve-cycle, charge, runtime, and telemetry tests.

## SM-01 reference build

Before assembly:

- open and identify the bagged soil hardware;
- prove one complete set contains three 200SS-15 sensors, one 200TS, and one 200SS-VA3;
- freeze four ENTS ADC inputs without losing another required function;
- allocate one compatible enclosure, solar panel, protected LiPo, glands, and cable protection;
- pass independent wet/dry response, temperature-reference, charge, runtime, and telemetry tests.

## Ordered replication hardware

IH-02 and SM-02 through SM-04 hardware was ordered, but the observed pool has no station allocation and is not proven complete. Inventory it now; assemble it only after the matching reference build passes.

## Network and external paths

- Verify the exact delivered US915 gateway, site, backhaul, owner, node sub-band, ChirpStack registration, MQTT path, and reconnect behavior.
- Acquire a matching-region WeatherLink Live for the reported Davis 6162 and verify the complete MET-01 path.
- Verify the ordered MX Gateway, plan entitlement, account ownership, MX1104 upload, credentials, sensor-ID map, and bounded API readback.
- Verify the ordered Signalizer pilot against the selected iPERL register, cable, units, scalar, power, protected logger input, and meter-owner approval.
- Preserve the passed local InfluxDB and Grafana acceptance receipt, then select a production host, retention policy, backup owner, and recovery test.

## Field and operating decisions

Student Farm approval is still required for sites, depths, pipe sizes, fittings, mounts, backflow and safety rules, cable protection, valve-control authority, and maintenance access. Assign accountable owners for assembly, firmware, gateway, data, secrets, backups, and maintenance before deployment.
