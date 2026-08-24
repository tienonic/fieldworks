# Controlled hardware plan

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-08-24
Evidence: station acceptance gates, protected order-state readback, and partial physical inventory

Purchasing authority: none. This page records the current order and release state; it does not authorize a purchase. Several later-build items were ordered before the reference builds passed. Keep them unallocated and uninstalled until the gates below pass.

## Inventory before any new request

1. Assign serials and revisions to the seven ENTS boards.
2. Inspect both D10 bodies and ports, identify both pulse switches, and resolve the size mismatch.
3. Open the soil bags and count exact 200SS-15, 200TS, and 200SS-VA3 items.
4. Count and identify Polycase units, solar panels, LiPo packs, glands, vents, drivers, fittings, and support hardware.
5. Allocate only one complete IH-01 kit and one complete SM-01 kit.
6. Set a deficit only after both reference kits pass.

## Reference builds

For IH-01, fill only verified gaps in the meter interface, pressure plumbing and divider, solenoid driver, enclosure, power, fittings, and test equipment.

For SM-01, fill only verified gaps in the complete Watermark set, four-channel ADC path, enclosure, power, cable protection, and reference-test equipment.

## Ordered hardware held for later builds

- IH-02 irrigation hardware remains held until IH-01 passes and the repeatable BOM is frozen.
- SM-02 through SM-04 hardware remains held until SM-01 passes and the repeatable BOM is frozen.
- Shared enclosure and power hardware remains unallocated until exact SKUs and quantities are known.
- The US915 gateway remains uncommissioned until exact model, site, backhaul, owner, and node sub-band are recorded.

## Ordered pilots held for verification

- The MX Gateway and data plan remain out of production until delivery, account, entitlement, MX1104 upload, API access, and sensor-ID mapping pass.
- The Signalizer and power adapter remain disconnected until the meter owner approves the pilot and register, cable, power, protected logger interface, scaling, and alarm tests pass.

## MET-01 conditional item

A matching-region WeatherLink Live receiver is still required for the reported Davis 6162. Select it only after the transmitter region and physical station identity are documented.

Every released item needs an exact model, quantity, owner, physical fit check, electrical check, acceptance test, station allocation, and receiving record in protected storage.
