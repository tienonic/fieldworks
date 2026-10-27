# Physical inventory checklist

Status: partial physical count
Owner: Nicholas Melnichenko
Updated: 2026-10-26
Evidence: protected inventory photo set, prior direct ENTS board count, October 2026 accessory delivery readback, and Nicholas's bench reports of October 22 and 23

Scope: hardware physically observed in the current inventory photo set, plus ENTS boards previously confirmed on hand. Procurement approval, order status, or shipping status alone does **not** count as received hardware.

This checklist is intentionally conservative. A part is checked as received only when the physical item, packaging, or prior direct count supports it. Model/SKU mismatches and unreadable labels remain open checks.

## October 26 photo check

Photos are in the [parts photo atlas](../03-hardware/parts-atlas.md).

- ENTS node `3.1.0-046`: revision 3.1.0, dated 2026-04-06, direct SMA antenna jack, solar input marked center positive, 18 V maximum. The other six boards are not yet recorded.
- Treedix 1.27 mm SWD adapter: two breakout boards, two loose 10-pin strips, one 10-pin 1.27 mm ribbon and one 20-pin 2.54 mm ribbon. The breakout pin rows are unsoldered.
- ST-Link V2 programmer: pin label read; three jumper leads attached.
- DRV8871 motor driver: one, received. VMotor 6.5 to 45 V.
- ADS1115 ADC board: one, received; header unsoldered.

## BOM-matched hardware

- [x] **ENTS / Wio-E5 nodes — 7 on hand**
  - BOM role: field node / radio hardware.
  - Physical status: received.
  - Label status: individual board serials/revisions not yet recorded.
  - BOM match: hardware family matches; final station allocation is separate.

- [x] **Assured Automation D10 water meters — 2 D10-NSF-050 units/boxes identified**
  - Visible label/model: `D10-NSF-050`.
  - Visible meter size: `5/8 x 1/2`.
  - Register: U.S. gallons; AWWA C700 marking visible.
  - BOM role: irrigation flow meter.
  - BOM match: **family match, size/design check required**. The current BOM working design references a nominal 3/4-inch NPT D10 path, while the received meter face is marked 5/8 x 1/2.
  - Open check: open/inspect both units, record full body/port markings, and confirm whether each has the required D10-C-SRS pulse switch.

- [ ] **D10-C-SRS pulse switches — exact received quantity not yet verified**
  - One photographed D10 has an attached cable, but the pulse-switch model label is not visible.
  - Do not count the cable alone as proof of a D10-C-SRS until the switch/packaging is identified.

- [x] **Rain Bird CP075 valve body — 1 received**
  - Visible label/model: `CP075`.
  - Size: `3/4 in`.
  - BOM role: IH-01 irrigation valve body.
  - BOM match: **yes for the valve body**.
  - Open check: identify the installed/replacement solenoid and verify that the final actuator supports the required bidirectional DC-latching control path.

- [ ] **DIG 305DC-075 complete valve assembly — not observed in current photo set**
  - Current physical receipt cannot be confirmed from the supplied photos.

- [ ] **DFRobot SEN0257 pressure sensors — not observed in current photo set**
  - Current physical receipt cannot be confirmed from the supplied photos.

- [x] **Soil-sensor hardware — 3 bagged assemblies received**
  - Appearance is consistent with the project's Watermark soil-sensor hardware.
  - BOM role: soil tension / temperature packages.
  - Exact model labels (`200SS-15`, `200TS`, `200SS-VA3`) are not readable in the current photos.
  - BOM match: **pending model and completeness check**; do not yet count these as three complete station sets.
  - Open check: photograph the model tags/packaging and count the 200SS, 200TS, and VA3 components in each bag.

- [x] **Polycase enclosures — multiple received**
  - Manufacturer branding: Polycase.
  - Exact quantity: not yet counted.
  - Exact model/SKU: not visible in the current photo.
  - BOM match: **pending**; verify whether the received enclosures are the working WQ-44 baseline or another compatible Polycase model.

- [ ] **Field LiPo batteries — shipment evidence only; contents not yet verified**
  - Two cartons with `UN3481` lithium-ion battery shipping labels were photographed.
  - This confirms battery-related shipments, not the exact battery model, voltage, capacity, JST-PH polarity, or physical quantity inside.
  - Do not count battery units as verified until the cartons are opened and the battery labels/connectors are recorded.

## Received support hardware / consumables

These items are physically on hand but are not currently represented as individual station-level lines in `station-bom.csv`.

- [x] **Southwire CAT5e indoor/outdoor cable — 1 package**
  - `24/4`, `CMR/CMX-TAN`, `100 ft / 30.48 m`.
  - Role: field wiring / communications support.

- [x] **Southwire Ultra-Whip — 1 package**
  - `1/2 in`, `6 ft / 1.83 m`, non-metallic liquid-tight preassembled whip.
  - Label indicates two 10 AWG conductors plus one 10 AWG ground conductor.
  - Role: protected field wiring / conduit support.

- [x] **Loctite Clear Silicone waterproof sealant — 1 package**
  - `2.7 fl oz / 80 mL`.
  - Role: enclosure/weatherproofing consumable.

- [x] **Arrow MG24 mini glue sticks — 1 pack / 24 sticks**
  - `4 in / 10 cm`, `5/16 in / 8 mm` diameter.
  - Role: assembly consumable.

- [x] **Assorted brass threaded fittings/adapters — received**
  - Several fittings are physically visible.
  - Exact quantity, thread size, and BSP/NPT type are not yet verified.
  - Do not allocate them to the SEN0257 plumbing path until thread standards are confirmed.

## Bench accessories received in October 2026

One accessory order for the bench was confirmed delivered in full. Pack contents are advertised quantities; counted units are recorded only where someone opened the pack.

- [x] **Treedix 1.27 mm SWD adapter kit with 200 mm ribbon — 1 kit**
  - Role: bridges the ST-Link's 2.54 mm header to the ENTS board's small programming header.
  - Open check: the signal map through the adapter and ribbon is not recorded. A keyed plug or a red stripe does not establish the electrical map.
- [x] **Resistor assortment — 1 pack**
  - Role: 22 kOhm and 47 kOhm candidates for the SEN0257 pressure divider.
  - Open check: loose counts and exact values uninspected.
- [x] **CR123A 3 V lithium cells — 2 advertised**
  - Role: Davis ISS backup battery. Not the ENTS LiPo supply.
- [x] **RP-SMA antenna pack — 2 advertised**
  - Role: replacement for the gateway's original antenna, which Nicholas reports missing.
  - Open check: match the center contact and thread to the actual gateway socket before fitting.
- [x] **SMA antenna pack with U.FL pigtails — 2 advertised**
  - Role: candidate node antennas for the Wio-E5 radio.
  - Open check: match the node socket; a direct SMA socket does not need the pigtail. SMA and RP-SMA look alike, so inspect the center contact.
- [x] **Adafruit DRV8871 motor-driver breakout — 1**
  - Role: candidate reversing driver for the latching solenoid. Coil, supply, and pulse timing remain unproved.
- [x] **ADS1115 16-bit ADC module — 1 line, module count unverified**
  - Role: conditional analog expansion. Not needed to read the controller ID. Allocation waits for the soil-input channel map.

## Reported by Nicholas, October 2026

These are owner reports, not photographed counts.

- The RAK gateway is present. Its original antenna is missing.
- Four solar panels have been photographed; six were requested institutionally. Locate the other two or match receiving records before buying replacements.
- One WIND lead fits the Davis ISS; another is too large. UV, SUN, RAIN, and TEMP/HUM are connected.
- Usable jumper leads and a working multimeter are not on hand. One meter and one 2.54 mm jumper assortment are selected for purchase and not yet ordered.
- The solar panel plug is 3.5 x 1.1 mm. The matching 5.5 x 2.1 mm adapter is identified but not bought, because the ENTS charging socket diameter is unconfirmed.
- No controller ID or soil reading has been saved. The last recorded SWD attempt returned `0x000` with `ENTER_SWD error (0x09)`.

## Not counted from procurement status alone

Any part listed elsewhere as `opp_complete`, `submitted_approver`, `submitted_not_ordered`, `delivery_unverified`, or similar remains unchecked here unless there is direct physical evidence that it arrived.

## Next physical-inventory pass

When access to the remaining hardware is available, record:

1. one full-item photo and one readable label photo per component;
2. exact model/SKU and quantity;
3. serial number where present;
4. connector, voltage, or size markings that affect compatibility;
5. which station the item is assigned to, only after the model is verified.

The machine-readable version of this partial count is in [physical-inventory.csv](physical-inventory.csv).

MET-01/Davis hardware is being handled separately in the Davis integration pull request and is not duplicated here as newly received procurement hardware.
