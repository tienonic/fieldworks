# Assembly and Test Plan

Status: working
Owner: unassigned
Updated: 2026-07-27
Evidence: compatibility grid and station connection records

## 1. Intake

- Assign a hardware serial to each ENTS board.
- Record exact manufacturer/model, serial, cable, connector, condition, and source for every instrument.
- Keep purchase/loan evidence private; record only its identifier here.
- Reject any part whose voltage, protocol, environmental rating, or mechanical fit differs from the approved design until reviewed.

## 2. Power-only test

- Verify LiPo polarity and protection before connection.
- Power ENTS from a current-limited source first.
- Measure 3.3 V and any switched 5 V rails.
- Verify solar input polarity and charge behavior separately.
- Do not attach a sensor until the rail test passes.

## 3. One sensor at a time

- Connect one sensor using its station table.
- Capture raw ADC counts, pulse events, or SPI values.
- Apply conversion and compare with a reference.
- Disconnect and inspect for heating, clipping, resets, or excess current.

## 4. Station integration

- Combine only individually accepted paths.
- Freeze pin assignments and cable labels.
- Run at least 24 hours on battery/solar simulation.
- Decode every payload and check units, range, missing-value behavior, station ID, and timestamp.

## 5. Radio test

- Configure US915 and the selected sub-band on node and gateway.
- Register unique device credentials without committing them.
- Test packet delivery, reconnect behavior, and signal margin at candidate sites.

## 6. Type-specific tests

### Irrigation

- Meter known water volume and compare pulse count.
- Test pressure against a reference gauge.
- Verify valve open and close with momentary pulses and fail-safe behavior.
- Confirm manual override and authority before connecting to live irrigation.

### Soil

- Verify all four VA3 channels.
- Label each depth before burial.
- Test dry/wet response and temperature reference.

### Meteorological

- Stop until physical model identity is verified.
- Test instruments separately before shared power/ground.
- Record calibration, orientation, height, and reference comparison.

## 7. Installation gate

No field installation passes without approved site, utility/irrigation safety review, mounting plan, cable protection, weatherproofing, maintenance owner, and rollback/removal plan.
