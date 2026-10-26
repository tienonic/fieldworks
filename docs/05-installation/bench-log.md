# Bench log

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-10-23
Evidence: dated local build checkpoints, the October 2026 accessory delivery readback, and Nicholas's bench reports

**Next test: identify one ENTS board and read a valid controller ID.** Nothing has been powered and measured yet. There is no saved controller ID, soil reading, or radio packet. The last recorded SWD attempt returned `0x000` with `ENTER_SWD error (0x09)`.

## Two separate paths

The **programming path** lets the computer talk to the controller. It runs from the ST-Link through jumper leads and the 1.27 mm adapter and ribbon to the board's small programming header. The **sensor path** turns a Watermark probe's resistance into a voltage the controller reads. It runs from one 200SS probe through the 200SS-VA3 adapter to one confirmed ENTS analog input. The small ribbon is not a soil-sensor cable.

## First check: the controller

Allow 60 to 90 minutes. Keep the battery, solar panel, sensors, and valve disconnected throughout.

1. **Lay out and photograph.** One ENTS board, the ST-Link, the 1.27 mm adapter kit, jumper leads, a USB cable, and a multimeter. Photograph both board faces, the revision text, the programming header, the ST-Link pin labels, and both faces of the adapter. Result: readable markings, not a shopping list.
2. **Match the revision and map the signals.** Find the schematic for the photographed revision. Record where `GND`, `SWDIO`, `SWCLK`, and `NRST` land at the ST-Link, the adapter, and the board. A red stripe or a keyed plug is not an electrical map. With power off, confirm each path in continuity mode and check that power is not shorted to ground. Result: a recorded signal map and continuity results.
3. **Power from one source and measure.** Use the board's USB input as the only supply. Measure the controller rail against its ground. Leave the ST-Link's 3.3 V and 5 V outputs disconnected. Result: measured rail voltage, correct polarity, one supply.
4. **Read the target ID.** Use one debugger with the recorded wiring. Save the tool, host, command, output, and a wiring photo. A supported target ID finishes this check. If the result is `0x000` again, recheck power, continuity, and reset before repeating. Do not flash, erase, or change protection to diagnose an unidentified connection.

| Signal | Purpose | Record before connecting |
|---|---|---|
| `GND` | shared reference | contacts at ST-Link, adapter, and board; continuity |
| `SWDIO` | debug data | contacts at all three ends; continuity |
| `SWCLK` | debug clock | contacts at all three ends; continuity |
| `NRST` | controller reset, if used | probe output and board reset contact |
| 3.3 V / 5 V probe outputs | optional probe-supplied power | leave disconnected while the board is USB-powered |

The numbered header contacts stay unresolved until the board and adapter are matched. The upstream ENTS hardware README names two different connectors `J9`, so it cannot identify a socket on the received board by itself. Earlier local notes gave conflicting D1 and D2 advice; they are historical evidence, not a wiring map.

## Second check: one soil path

Allow 60 to 120 minutes after the controller check, if the matching firmware already exists.

1. Identify the VA3 model and terminal labels against Irrometer sheet 427. Connect one 200SS probe's two wires to the labelled sensor-input pair with power off.
2. With the ENTS inputs still disconnected, supply the VA3 from a verified regulated source and measure its output against the labelled reference. The sheet gives a 3 to 30 V supply, a 0 to 2.8 V output, a 500 ms startup, and roughly five-minute updates under continuous power.
3. Confirm the ENTS input conditioning, common reference, and firmware conversion before joining that output. Save the raw count, the engineering value, the time, and a known physical response. A voltage alone is not a calibrated moisture reading.
4. Only then expand to the other VA3 channels. The ADS1115 waits for the channel map.

## Session record

| Date | What happened | Result |
|---|---|---|
| 2026-09-25 | First bench attempt on the other laptop with female-to-female leads. | Debugger and serial attempts failed. No controller ID. |
| 2026-10-01 to 10-02 | Parts arrival review. Nicholas reported the solar adapter, batteries, and resistors in hand. | Inventory reconciled; no hardware test. |
| 2026-10-13 | Document and receipt review after Nicholas reported the parts arrived and the connections were confusing. | First-check procedure written. No hardware connected. |
| 2026-10-22 to 10-23 | Order reconciliation and workspace recovery. All seven accessory lines confirmed delivered. Gateway present, original antenna missing. Meter and jumper leads confirmed missing and selected for purchase. Older `pending` rows found superseded by later order summaries. | Checkpoint saved; the next test is unchanged. |

## What is still unknown

| Owner | Missing evidence | What it unlocks |
|---|---|---|
| Nicholas | board revision, header markings, continuity, rail voltage | a valid controller ID and an exact wiring map |
| Nicholas | antenna center contacts against the gateway and node sockets | which antenna pack fits where |
| Nicholas | ENTS charging socket diameter and polarity | the solar plug adapter purchase |
| Nicholas | counts inside the three soil-sensor bags and the remaining panels | exact shortages without duplicate orders |
| purchasing owner | receiving readback for the HOBO gateway, Signalizer, and panels | delivery questions closed or the order investigated |
| Nicholas and station owner | Davis transmitter and receiver region; valve coil and supply | the receiver choice and a compatible valve design |

Continue with the [assembly and test plan](assembly-and-test.md) once the controller and one soil path are proved.
