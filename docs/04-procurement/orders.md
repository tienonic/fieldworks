# Equipment status

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-10-23
Evidence: protected OPP and purchaser records read through 2026-08-20, later institutional order summaries, the October 2026 accessory delivery readback, and Nicholas's reports of October 22 and 23

This public record omits dates of purchase, order numbers, request IDs, prices, receipts, account data, and private attachments. A vendor order is not a receipt. A shared-pool observation is not a station allocation or a bench acceptance.

## Physically observed

- Seven ENTS / Wio-E5 boards are on hand. Serial, revision, station assignment, and power-on checks remain open.
- Two `D10-NSF-050` meters or boxes were observed. Their faces say `5/8 x 1/2`, which does not directly match the nominal 3/4-inch working design. Exact D10-C-SRS switches and station allocation are unverified.
- One Rain Bird `CP075` 3/4-inch valve body was observed. Its latching-solenoid path is unverified.
- Three bagged assemblies consistent with the Watermark order were observed. Labels and contents do not prove three complete station sets.
- Multiple Polycase enclosures were observed. Count and model are unverified.
- Field cable, liquid-tight whip, sealant, glue sticks, and brass fittings were observed. Fitting sizes and thread standards remain open.

- A seven-line bench accessory order is delivered in full: SWD adapter kit, resistor assortment, CR123A cells, an RP-SMA antenna pack, an SMA antenna pack, a DRV8871 breakout, and an ADS1115 module. None of it makes a complete station.
- Nicholas reports the RAK gateway present with its original antenna missing. The RP-SMA pack is its replacement, pending a socket check.
- Four solar panels are photographed against six requested.

Two `UN3481` cartons are shipment evidence only. They do not prove the battery model, count, voltage, capacity, connector, protection, or polarity.

See [the physical inventory checklist](physical-inventory.md) for the conservative item-level record.

## Vendor ordered; delivery or exact receipt unverified

The protected purchasing record shows vendor orders for:

- the remaining D10 pulse-switch, SEN0257 pressure-sensor, and irrigation-valve paths;
- remaining Watermark soil packages;
- enclosures, vents, cable glands, solar panels, and LiPo batteries;
- one RAKwireless US915 gateway;
- one Onset MX Gateway and an API-capable annual data plan;
- one Signalizer interface and power adapter;
- programming, bench, weatherproofing, and installation materials.

An older tracking sheet still marks several of these lines `pending`. Later institutional order summaries record that they were placed. Treat the older sheet as superseded: find the unconfirmed deliveries before ordering replacements.

Where a photo matches only a family or package, the physical checklist overrides the broader order description. Items not observed remain `vendor_ordered_delivery_unverified` or a more specific gated state.

## Pending purchases

- One multimeter and one 2.54 mm jumper-lead assortment, needed before the first continuity and rail checks. Selected, not ordered.
- One solar plug adapter, 3.5 x 1.1 mm female to 5.5 x 2.1 mm male, after the ENTS charging socket diameter and polarity are confirmed. It changes plug size, not voltage. Do not substitute a 3.5 x 1.35 mm part.
- Nothing else. Every other apparent shortage is a count or delivery check, not a purchase.

## Release gates

- Build IH-02 only after IH-01 passes and its repeatable plumbing, sensing, valve, power, and enclosure design is frozen.
- Build SM-02 through SM-04 only after SM-01 passes its four-channel test and one complete Watermark set is identified.
- Do not connect the Signalizer until the meter owner approves the pilot and the register, cable, power, output, and protected logger interface match the manufacturer documentation.
- Do not enable HOBO production ingestion until delivery, plan entitlement, account ownership, MX1104 upload, sensor-ID mapping, and a bounded API readback pass.
- Do not commission the gateway until its exact US915 model, site, backhaul, owner, and node sub-band are recorded.
