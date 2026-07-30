# What we need

The project has enough ENTS boards for six field stations and one meteorological sandbox. A complete bench-ready station parts set still needs verification.

The immediate work is to inventory what is on hand, finish `IH-01` and `SM-01`, and use those builds to settle the repeatable design.

## First irrigation station

`IH-01` gaps:

- a verified meter, pulse switch, pressure sensor, valve, and solenoid set;
- the correct pressure fitting and safe voltage-divider circuit;
- a tested bidirectional valve driver and boost stage;
- a weatherproof enclosure and field-power package;
- pressure and measured-volume reference tests.

## First soil station

`SM-01` gaps:

- a verified three-depth soil-tension and temperature set;
- a frozen four-channel ADC map;
- a weatherproof enclosure and field-power package;
- dry/wet and temperature reference tests.

## After the reference builds

- one more irrigation package for `IH-02`;
- three more soil packages for `SM-02` through `SM-04`;
- the remaining enclosures and field-power parts;
- one US915 LoRaWAN gateway.

Schedule these after the reference builds pass:

## Other open needs

- confirm the exact loaned instruments for `MET-01` before choosing interface parts;
- approve station locations, depths, pipe sizes, mounting, and cable protection;
- assign owners for assembly, firmware, gateway, data, and maintenance;
- prove the complete data path from field packet to dashboard and export.

Build the final hardware list from tested reference builds and physical inventory.
