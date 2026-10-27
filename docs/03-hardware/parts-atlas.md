# Parts photo atlas

Status: working
Owner: Nicholas Melnichenko
Updated: 2026-10-26
Evidence: September 24, 2026 inventory photo set (42 photos after removing four duplicate enclosure views) and eleven October 26, 2026 close-ups; labels read from the photos

**Use this page to find a part by what it does.** Each section matches one part of the station: controller, programming, soil, weather, water, power, small electronics, enclosures, supplies, and unidentified items. Click a thumbnail for the full photo. The [physical inventory](../04-procurement/physical-inventory.md) holds counts and receiving status; the [bench log](../05-installation/bench-log.md) uses these photos for the wiring map.

A photo shows that a part was on the table. It does not prove the part works, how many pieces are inside, or which station it belongs to. "Needs check" means the model or size is not readable yet.

## What the October 26 photos settled

- **Board revision:** the photographed ENTS node is version 3.1.0, unit label `3.1.0-046`, dated 2026-04-06. Its back is marked "Solar Input, Voc max 18 V, typical 6 V, center positive" and has a direct SMA antenna jack.
- **Programmer pinout:** the ST-Link V2 label gives pin 2 SWCLK, pin 4 SWDIO, pins 5 and 6 GND, pin 1 RST, and 3.3 V and 5.0 V outputs on pins 7 to 10.
- **Treedix adapter:** its 10-hole breakout row has no pins soldered. The two supplied pin strips are still loose. Jumper wires pushed into bare holes make no reliable contact, which can explain a "no signal" result.
- **ADS1115 and DRV8871:** both delivered. The ADS1115 header is also unsoldered.

## Not photographed yet

The whole front of an ENTS board (D2 programming header, J1 and J4 screw terminals, USB-C port and power switch), the other six boards' labels, the RAK gateway, both antenna packs, the CR123A batteries, the resistor assortment and the inside of the soil-sensor bags.

## Controller board

The ENTS node itself. Seven are on hand; one has been photographed so far.

| Photo | Item | Label | Next check |
|---|---|---|---|
| [<img src="parts-photos/00-controller-board/P54-ents-node-3-1-0-unit-046-back.jpg" width="140" alt="ENTS node 3.1.0, unit 046, back">](parts-photos/00-controller-board/P54-ents-node-3-1-0-unit-046-back.jpg) | **ENTS node 3.1.0, unit 046, back** (P54) | ents-node 3.1.0; 2026-04-06; label 3.1.0-046; Solar Input Voc max 18 V, typical 6 V, center positive; Li-Ion Battery; SDI-12; SMA antenna jack (label read) | Record the other six boards the same way. Photograph the front. |

## Programming chain

Connects the computer to the ENTS controller. Needed for the first bench check.

| Photo | Item | Label | Next check |
|---|---|---|---|
| [<img src="parts-photos/01-programming/P47-st-link-v2-pin-label-october-26.jpg" width="140" alt="ST-Link V2 pin label (October 26)">](parts-photos/01-programming/P47-st-link-v2-pin-label-october-26.jpg) | **ST-Link V2 pin label (October 26)** (P47) | 1 RST, 2 SWCLK, 3 SWIM, 4 SWDIO, 5-6 GND, 7-8 3.3V, 9-10 5.0V (label read) | Use pin 4 SWDIO, pin 2 SWCLK, pin 6 GND, and pin 1 RST only if connect-under-reset is needed. Leave 3.3V and 5.0V unconnected. |
| [<img src="parts-photos/01-programming/P35-adafruit-st-link-stm8-stm32-v2-emulator-p2548.jpg" width="140" alt="Adafruit ST-Link STM8/STM32 v2 Emulator P2548">](parts-photos/01-programming/P35-adafruit-st-link-stm8-stm32-v2-emulator-p2548.jpg) | **Adafruit ST-Link STM8/STM32 v2 Emulator P2548** (P35) | ST-Link STM8/STM32 v2 Emulator; P2548; P2548B (label read) | Keep with programming cables. Verify target board and connector pinout before use. |
| [<img src="parts-photos/01-programming/P56-treedix-breakouts-2-pin-labels.jpg" width="140" alt="Treedix breakouts (2), pin labels">](parts-photos/01-programming/P56-treedix-breakouts-2-pin-labels.jpg) | **Treedix breakouts (2), pin labels** (P56) | Row from square pad: V, DIO, SCK, G, G, SWO, RES, G, NC, V (label read) | Pins are not soldered. Jumpers pushed into bare holes give no reliable contact. |
| [<img src="parts-photos/01-programming/P57-treedix-breakouts-with-loose-pin-strips.jpg" width="140" alt="Treedix breakouts with loose pin strips">](parts-photos/01-programming/P57-treedix-breakouts-with-loose-pin-strips.jpg) | **Treedix breakouts with loose pin strips** (P57) | Two boards, two 10-pin strips (label read) | Solder a strip to one board, then continuity-test each row pin to the 2x5 socket. |
| [<img src="parts-photos/01-programming/P55-10-pin-1-27-mm-swd-ribbon.jpg" width="140" alt="10-pin 1.27 mm SWD ribbon">](parts-photos/01-programming/P55-10-pin-1-27-mm-swd-ribbon.jpg) | **10-pin 1.27 mm SWD ribbon** (P55) | 2x5 1.27 mm sockets; red stripe marks pin 1 (label read) | Treedix 2x5 socket to the ENTS D2 SWD header. Match the red stripe to pin 1 at both ends. |
| [<img src="parts-photos/01-programming/P53-treedix-adapter-with-20-pin-ribbon.jpg" width="140" alt="Treedix adapter with 20-pin ribbon">](parts-photos/01-programming/P53-treedix-adapter-with-20-pin-ribbon.jpg) | **Treedix adapter with 20-pin ribbon** (P53) | Treedix: SWDIO, SWCLK, SWO, NC/TDI, nRESET; 2x5 and 2x10 sockets (label read) | The 2x5 box header is fitted. The 10-hole row has no pins: solder one supplied pin strip before using jumpers. |
| [<img src="parts-photos/01-programming/P25-adafruit-usb-to-ttl-serial-cable-p954.jpg" width="140" alt="Adafruit USB to TTL Serial Cable P954">](parts-photos/01-programming/P25-adafruit-usb-to-ttl-serial-cable-p954.jpg) | **Adafruit USB to TTL Serial Cable P954** (P25) | USB to TTL Serial Cable; P954 (label read) | Verify P954 logic voltage and wire mapping before connecting. |

## Soil sensing

Watermark probes and related sensor parts for the soil monitoring stations.

| Photo | Item | Label | Next check |
|---|---|---|---|
| [<img src="parts-photos/02-soil-sensing/P04-soil-probe-sets-green-and-red-leads.jpg" width="140" alt="Soil probe sets, green and red leads">](parts-photos/02-soil-sensing/P04-soil-probe-sets-green-and-red-leads.jpg) | **Soil probe sets, green and red leads** (P04) | not visible (needs check) | Lay one complete set beside its label; photograph both probe ends. |
| [<img src="parts-photos/02-soil-sensing/P05-soil-probe-sets-green-and-red-leads.jpg" width="140" alt="Soil probe sets, green and red leads">](parts-photos/02-soil-sensing/P05-soil-probe-sets-green-and-red-leads.jpg) | **Soil probe sets, green and red leads** (P05) | not visible (needs check) | Lay one complete set beside its label; photograph both probe ends. |
| [<img src="parts-photos/02-soil-sensing/P06-soil-probe-sets-green-and-red-leads.jpg" width="140" alt="Soil probe sets, green and red leads">](parts-photos/02-soil-sensing/P06-soil-probe-sets-green-and-red-leads.jpg) | **Soil probe sets, green and red leads** (P06) | not visible (needs check) | Lay one complete set beside its label; photograph both probe ends. |
| [<img src="parts-photos/02-soil-sensing/P07-soil-probe-sets-green-and-red-leads.jpg" width="140" alt="Soil probe sets, green and red leads">](parts-photos/02-soil-sensing/P07-soil-probe-sets-green-and-red-leads.jpg) | **Soil probe sets, green and red leads** (P07) | not visible (needs check) | Lay one complete set beside its label; photograph both probe ends. |
| [<img src="parts-photos/02-soil-sensing/P52-ads1115-16-bit-i2c-adc-board.jpg" width="140" alt="ADS1115 16-bit I2C ADC board">](parts-photos/02-soil-sensing/P52-ads1115-16-bit-i2c-adc-board.jpg) | **ADS1115 16-bit I2C ADC board** (P52) | ADS1115; VDD, GND, SCL, SDA, ADDR, ALRT, A0-A3 (label read) | Header pins are loose; solder before use. Connect only after the soil channel map is decided. |
| [<img src="parts-photos/02-soil-sensing/P20-adafruit-pt100-rtd-temp-amplifier-p3328.jpg" width="140" alt="Adafruit PT100 RTD Temp Amplifier P3328">](parts-photos/02-soil-sensing/P20-adafruit-pt100-rtd-temp-amplifier-p3328.jpg) | **Adafruit PT100 RTD Temp Amplifier P3328** (P20) | Adafruit PT100 RTD Temp Amplifier; P3328; P3328D (label read) | Keep sealed with label. Match probe type before wiring. |

## Weather station

Davis transmitter and sensor assembly for MET-01. Separate from the ENTS and gateway paths.

| Photo | Item | Label | Next check |
|---|---|---|---|
| [<img src="parts-photos/03-weather/P30-davis-weather-station-sensor-assembly.jpg" width="140" alt="Davis weather-station sensor assembly">](parts-photos/03-weather/P30-davis-weather-station-sensor-assembly.jpg) | **Davis weather-station sensor assembly** (P30) | DAVIS; ISS Transmitter (partly read) | Photograph transmitter label and complete assembly from both sides. |

## Water and irrigation

Meters, valves, solenoids, pressure sensor and plumbing fittings for the irrigation head stations.

| Photo | Item | Label | Next check |
|---|---|---|---|
| [<img src="parts-photos/04-water-irrigation/P08-assured-automation-d10-water-meter.jpg" width="140" alt="Assured Automation D10 water meter">](parts-photos/04-water-irrigation/P08-assured-automation-d10-water-meter.jpg) | **Assured Automation D10 water meter** (P08) | ASSURED AUTOMATION; D10-NSF-050; 5/8 X 1/2; U.S. GALLONS (label read) | Relabel as water meter, not rain gauge. Keep matching fittings together. |
| [<img src="parts-photos/04-water-irrigation/P09-assured-automation-d10-water-meter.jpg" width="140" alt="Assured Automation D10 water meter">](parts-photos/04-water-irrigation/P09-assured-automation-d10-water-meter.jpg) | **Assured Automation D10 water meter** (P09) | ASSURED AUTOMATION; D10-NSF-050; 5/8 X 1/2; U.S. GALLONS (label read) | Relabel as water meter, not rain gauge. Keep matching fittings together. |
| [<img src="parts-photos/04-water-irrigation/P01-dig-dc-solenoid-s-305dc.jpg" width="140" alt="DIG DC solenoid S-305DC">](parts-photos/04-water-irrigation/P01-dig-dc-solenoid-s-305dc.jpg) | **DIG DC solenoid S-305DC** (P01) | DIG; S-305DC; DC SOLENOID (6-9 VOLT); QTY: 1 (label read) | Keep with valves. Confirm the matching valve before connecting. |
| [<img src="parts-photos/04-water-irrigation/P27-dig-dc-solenoid-s-305dc.jpg" width="140" alt="DIG DC solenoid S-305DC">](parts-photos/04-water-irrigation/P27-dig-dc-solenoid-s-305dc.jpg) | **DIG DC solenoid S-305DC** (P27) | DIG; S-305DC; DC SOLENOID (6-9 VOLT); QTY: 1 (label read) | Keep with valves. Confirm the matching valve before connecting. |
| [<img src="parts-photos/04-water-irrigation/P13-rain-bird-irrigation-valve.jpg" width="140" alt="Rain Bird irrigation valve">](parts-photos/04-water-irrigation/P13-rain-bird-irrigation-valve.jpg) | **Rain Bird irrigation valve** (P13) | RAIN BIRD; FLOW (needs check) | Photograph model marking and port sizes; keep solenoid unpowered. |
| [<img src="parts-photos/04-water-irrigation/P02-dfrobot-sen0257-sensor-package.jpg" width="140" alt="DFRobot SEN0257 sensor package">](parts-photos/04-water-irrigation/P02-dfrobot-sen0257-sensor-package.jpg) | **DFRobot SEN0257 sensor package** (P02) | DFROBOT; SEN0257 (label read) | Photograph the sensor body and connector beside its package. |
| [<img src="parts-photos/04-water-irrigation/P38-brass-threaded-adapters-tailpieces.jpg" width="140" alt="Brass threaded adapters / tailpieces">](parts-photos/04-water-irrigation/P38-brass-threaded-adapters-tailpieces.jpg) | **Brass threaded adapters / tailpieces** (P38) | not visible (needs check) | Lay pieces apart and measure both ends; compare with meter fittings without forcing threads. |
| [<img src="parts-photos/04-water-irrigation/P12-brass-threaded-fittings-bag.jpg" width="140" alt="Brass threaded fittings, bag">](parts-photos/04-water-irrigation/P12-brass-threaded-fittings-bag.jpg) | **Brass threaded fittings, bag** (P12) | not visible (needs check) | Photograph fittings outside bag with ruler; record each thread size. |
| [<img src="parts-photos/04-water-irrigation/P14-brass-threaded-nuts-couplings.jpg" width="140" alt="Brass threaded nuts / couplings">](parts-photos/04-water-irrigation/P14-brass-threaded-nuts-couplings.jpg) | **Brass threaded nuts / couplings** (P14) | not visible (needs check) | Photograph each fitting outside bag beside ruler; record thread size. |
| [<img src="parts-photos/04-water-irrigation/P39-brass-threaded-ring-coupling.jpg" width="140" alt="Brass threaded ring / coupling">](parts-photos/04-water-irrigation/P39-brass-threaded-ring-coupling.jpg) | **Brass threaded ring / coupling** (P39) | not visible (needs check) | Measure inner and outer diameter and photograph thread profile. |
| [<img src="parts-photos/04-water-irrigation/P29-grey-plastic-fittings-or-caps-bag.jpg" width="140" alt="Grey plastic fittings or caps, bag">](parts-photos/04-water-irrigation/P29-grey-plastic-fittings-or-caps-bag.jpg) | **Grey plastic fittings or caps, bag** (P29) | not visible (needs check) | Lay pieces apart and photograph both openings beside ruler. |

## Power

Solar panels, batteries and adapters. Nothing here is connected yet.

| Photo | Item | Label | Next check |
|---|---|---|---|
| [<img src="parts-photos/05-power/P16-adafruit-solar-panel-6v-2w-p5366.jpg" width="140" alt="Adafruit solar panel 6V 2W P5366">](parts-photos/05-power/P16-adafruit-solar-panel-6v-2w-p5366.jpg) | **Adafruit solar panel 6V 2W P5366** (P16) | Medium 6V 2W Solar Panel; P5366; P5366A (label read) | Keep panels and leads together; do not connect to batteries yet. |
| [<img src="parts-photos/05-power/P17-adafruit-solar-panel-6v-2w-p5366.jpg" width="140" alt="Adafruit solar panel 6V 2W P5366">](parts-photos/05-power/P17-adafruit-solar-panel-6v-2w-p5366.jpg) | **Adafruit solar panel 6V 2W P5366** (P17) | Medium 6V 2W Solar Panel; P5366; P5366A (label read) | Keep panels and leads together; do not connect to batteries yet. |
| [<img src="parts-photos/05-power/P18-adafruit-solar-panel-6v-2w-p5366.jpg" width="140" alt="Adafruit solar panel 6V 2W P5366">](parts-photos/05-power/P18-adafruit-solar-panel-6v-2w-p5366.jpg) | **Adafruit solar panel 6V 2W P5366** (P18) | Medium 6V 2W Solar Panel; P5366; P5366A (label read) | Keep panels and leads together; do not connect to batteries yet. |
| [<img src="parts-photos/05-power/P19-adafruit-solar-panel-6v-2w-p5366.jpg" width="140" alt="Adafruit solar panel 6V 2W P5366">](parts-photos/05-power/P19-adafruit-solar-panel-6v-2w-p5366.jpg) | **Adafruit solar panel 6V 2W P5366** (P19) | Medium 6V 2W Solar Panel; P5366; P5366A (label read) | Keep panels and leads together; do not connect to batteries yet. |
| [<img src="parts-photos/05-power/P03-battery-labelled-boxes.jpg" width="140" alt="Battery-labelled boxes">](parts-photos/05-power/P03-battery-labelled-boxes.jpg) | **Battery-labelled boxes** (P03) | UN 3480 (needs check) | Read each battery model, voltage and connector label before opening or connecting. |
| [<img src="parts-photos/05-power/P37-power-adapter-with-barrel-plug.jpg" width="140" alt="Power adapter with barrel plug">](parts-photos/05-power/P37-power-adapter-with-barrel-plug.jpg) | **Power adapter with barrel plug** (P37) | not visible (needs check) | Photograph underside label: output voltage, current, polarity and model. |
| [<img src="parts-photos/05-power/P31-pololu-12v-step-up-regulator-u3v9f12.jpg" width="140" alt="Pololu 12V step-up regulator U3V9F12">](parts-photos/05-power/P31-pololu-12v-step-up-regulator-u3v9f12.jpg) | **Pololu 12V step-up regulator U3V9F12** (P31) | Pololu; Item #5585; 12V Step-Up Voltage Regulator U3V9F12 (label read) | Keep in antistatic bag; verify input limits and wiring before power. |
| [<img src="parts-photos/05-power/P32-outlet-plug-adapters-set.jpg" width="140" alt="Outlet plug adapters, set">](parts-photos/05-power/P32-outlet-plug-adapters-set.jpg) | **Outlet plug adapters, set** (P32) | not visible (needs check) | Photograph prongs, sockets and rating label. Do not connect to mains yet. |

## Small electronics

Resistors and breakout boards for the sensor and valve circuits.

| Photo | Item | Label | Next check |
|---|---|---|---|
| [<img src="parts-photos/06-small-electronics/P49-drv8871-motor-driver-back.jpg" width="140" alt="DRV8871 motor driver, back">](parts-photos/06-small-electronics/P49-drv8871-motor-driver-back.jpg) | **DRV8871 motor driver, back** (P49) | DC Motor H-Bridge; VMotor 6.5-45V; PWM Vlogic 3-5V; 3.6A peak (label read) | Check the latching-solenoid pulse voltage against the 6.5 V minimum before choosing it for IH stations. |
| [<img src="parts-photos/06-small-electronics/P50-drv8871-beside-the-ents-board-front.jpg" width="140" alt="DRV8871 beside the ENTS board front">](parts-photos/06-small-electronics/P50-drv8871-beside-the-ents-board-front.jpg) | **DRV8871 beside the ENTS board front** (P50) | ENTS: SW2 BOOT, SW1 RESET, D8 TXT, D9 RXT, I2C Port 1 (J9), I2C Port 2 (J8) (partly read) | Photograph the whole ENTS front so D2, J1, J4 and the USB-C port are visible. |
| [<img src="parts-photos/06-small-electronics/P48-drv8871-motor-driver-front.jpg" width="140" alt="DRV8871 motor driver, front">](parts-photos/06-small-electronics/P48-drv8871-motor-driver-front.jpg) | **DRV8871 motor driver, front** (P48) | DRV8871; MOTOR and POWER terminals; IN2, IN1, VM, GND (label read) | Valve driver for later. Header not fitted. Not part of the first bench check. |
| [<img src="parts-photos/06-small-electronics/P15-adafruit-resistor-packs-p2782-and-p2783.jpg" width="140" alt="Adafruit resistor packs P2782 and P2783">](parts-photos/06-small-electronics/P15-adafruit-resistor-packs-p2782-and-p2783.jpg) | **Adafruit resistor packs P2782 and P2783** (P15) | CF Axial Resistors -2.2Kohm -25 Pack; P2782; Through-Hole Resistors; P2783 (label read) | Keep each value in its original labelled bag. Confirm P2783 value before use. |
| [<img src="parts-photos/06-small-electronics/P33-adafruit-through-hole-resistors-p2784.jpg" width="140" alt="Adafruit through-hole resistors P2784">](parts-photos/06-small-electronics/P33-adafruit-through-hole-resistors-p2784.jpg) | **Adafruit through-hole resistors P2784** (P33) | Through-Hole Resistors; P2784; P2784A (label read) | Confirm resistance value from product label or meter before use. |
| [<img src="parts-photos/06-small-electronics/P24-adafruit-stemma-relay-p4409.jpg" width="140" alt="Adafruit STEMMA Relay P4409">](parts-photos/06-small-electronics/P24-adafruit-stemma-relay-p4409.jpg) | **Adafruit STEMMA Relay P4409** (P24) | Adafruit STEMMA Relay; P4409; P4409C (label read) | Keep sealed with label; verify P4409 instructions before wiring. |

## Enclosures, cable and mounting

Cases, glands, cable and poles for field installation.

| Photo | Item | Label | Next check |
|---|---|---|---|
| [<img src="parts-photos/07-enclosures-mounting/P45-polycase-enclosures-6-total.jpg" width="140" alt="Polycase enclosures (6 total)">](parts-photos/07-enclosures-mounting/P45-polycase-enclosures-6-total.jpg) | **Polycase enclosures (6 total)** (P45) | not visible (needs check) | Record each enclosure model/size before mounting. |
| [<img src="parts-photos/07-enclosures-mounting/P44-cable-gland-like-fittings-bag.jpg" width="140" alt="Cable gland-like fittings, bag">](parts-photos/07-enclosures-mounting/P44-cable-gland-like-fittings-bag.jpg) | **Cable gland-like fittings, bag** (P44) | not visible (needs check) | Photograph each fitting outside bag with ruler; record thread and cable opening sizes. |
| [<img src="parts-photos/07-enclosures-mounting/P11-cat-cable-coil-24-awg-4pr.jpg" width="140" alt="CAT cable coil, 24 AWG 4PR">](parts-photos/07-enclosures-mounting/P11-cat-cable-coil-24-awg-4pr.jpg) | **CAT cable coil, 24 AWG 4PR** (P11) | 24 AWG 4PR UTP CAT 5E; TESTED TO 350MHZ (label read) | Record length and photograph both cut ends; not a mains extension cord. |
| [<img src="parts-photos/07-enclosures-mounting/P46-jm-eagle-grey-pipe-ground-poles.jpg" width="140" alt="JM Eagle grey pipe / ground poles">](parts-photos/07-enclosures-mounting/P46-jm-eagle-grey-pipe-ground-poles.jpg) | **JM Eagle grey pipe / ground poles** (P46) | JM EAGLE (partly read) | Record pipe diameter and length and photograph full printed specification. Do not treat as electrical grounding rods. |

## Supplies and reference items

Consumables and items that are not station hardware.

| Photo | Item | Label | Next check |
|---|---|---|---|
| [<img src="parts-photos/08-supplies/P51-20-pin-2-54-mm-ribbon.jpg" width="140" alt="20-pin 2.54 mm ribbon">](parts-photos/08-supplies/P51-20-pin-2-54-mm-ribbon.jpg) | **20-pin 2.54 mm ribbon** (P51) | AWM 2651 28AWG 105C 300V (label read) | For 20-pin JTAG probes. Not needed with the ST-Link V2 and jumpers. |
| [<img src="parts-photos/08-supplies/P26-loctite-clear-silicone-sealant.jpg" width="140" alt="Loctite clear silicone sealant">](parts-photos/08-supplies/P26-loctite-clear-silicone-sealant.jpg) | **Loctite clear silicone sealant** (P26) | LOCTITE; CLEAR SILICONE; WATERPROOF SEALANT; 2.7 fl oz (80ml) (label read) | Keep capped; confirm suitable material and use before applying. |
| [<img src="parts-photos/08-supplies/P28-hot-glue-sticks.jpg" width="140" alt="Hot glue sticks">](parts-photos/08-supplies/P28-hot-glue-sticks.jpg) | **Hot glue sticks** (P28) | not visible (needs check) | Keep bag closed; confirm stick diameter matches the glue gun. |
| [<img src="parts-photos/08-supplies/P10-oxygen-absorber-packets.jpg" width="140" alt="Oxygen absorber packets">](parts-photos/08-supplies/P10-oxygen-absorber-packets.jpg) | **Oxygen absorber packets** (P10) | Oxygen Absorber; DO NOT EAT (label read) | Keep sealed and separate from parts. Do not label as silica-gel desiccant. |
| [<img src="parts-photos/08-supplies/P43-washer-like-disc-and-bagged-hardware.jpg" width="140" alt="Washer-like disc and bagged hardware">](parts-photos/08-supplies/P43-washer-like-disc-and-bagged-hardware.jpg) | **Washer-like disc and bagged hardware** (P43) | not visible (needs check) | Lay hardware apart, count it and measure disc hole and diameter. |
| [<img src="parts-photos/08-supplies/P41-polycase-customization-sample-and-brochure.jpg" width="140" alt="Polycase customization sample and brochure">](parts-photos/08-supplies/P41-polycase-customization-sample-and-brochure.jpg) | **Polycase customization sample and brochure** (P41) | polycase; ENCLOSURE CUSTOMIZATION with MACHINING & PRINTING (label read) | Keep with reference paperwork; do not count the sample as a working enclosure. |
| [<img src="parts-photos/08-supplies/P23-adafruit-gold-pcb-coaster-p5719.jpg" width="140" alt="Adafruit Gold PCB Coaster P5719">](parts-photos/08-supplies/P23-adafruit-gold-pcb-coaster-p5719.jpg) | **Adafruit Gold PCB Coaster P5719** (P23) | Gold PCB Coaster w/Adafruit Logo; P5719; P5719B (label read) | Keep separate from working boards. |

## Unidentified

Purpose unknown. Identify before assigning to a station.

| Photo | Item | Label | Next check |
|---|---|---|---|
| [<img src="parts-photos/09-unidentified/P42-black-plastic-fitting-or-bracket.jpg" width="140" alt="Black plastic fitting or bracket">](parts-photos/09-unidentified/P42-black-plastic-fitting-or-bracket.jpg) | **Black plastic fitting or bracket** (P42) | not visible (needs check) | Photograph front, back and both openings outside bag, with ruler. |
| [<img src="parts-photos/09-unidentified/P36-unidentified-bagged-metal-parts.jpg" width="140" alt="Unidentified bagged metal parts">](parts-photos/09-unidentified/P36-unidentified-bagged-metal-parts.jpg) | **Unidentified bagged metal parts** (P36) | not visible (needs check) | Lay metal pieces apart on plain paper and photograph both ends beside ruler. |
