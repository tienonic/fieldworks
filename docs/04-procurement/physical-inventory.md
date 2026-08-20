# Physical inventory checklist

Status: partial physical count
Updated: 2026-08-20
Scope: hardware physically observed in the current inventory photo set, plus ENTS boards previously confirmed on hand. Procurement approval, order status, or shipping status alone does **not** count as received hardware.

This checklist is intentionally conservative. A part is checked as received only when the physical item, packaging, or prior direct count supports it. Model/SKU mismatches and unreadable labels remain open checks.

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
