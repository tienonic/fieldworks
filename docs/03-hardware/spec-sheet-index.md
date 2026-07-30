# Spec sheet index

Status: working
Owner: unassigned
Updated: 2026-07-30

Match every sheet to the physical label before using its values.

## Station hardware

| Component | Manufacturer document | Status |
|---|---|---|
| ENTS node | [hardware repository](https://github.com/jlab-sensing/ENTS-node-hardware), [firmware repository](https://github.com/jlab-sensing/ENTS-node-firmware) | Verify board revision and connector polarity |
| Seeed Wio-E5 module | [module datasheet PDF](https://files.seeedstudio.com/products/317990687/res/LoRa-E5%20module%20datasheet_V1.1.pdf) | Matches the documented radio family; verify module label |
| TI BQ24210 solar charger | [datasheet PDF](https://www.ti.com/lit/gpn/BQ24210) | ENTS charging baseline |
| D10 water meter | [datasheet PDF](https://www.flows.com/content/literature/Datasheets/D10_datasheet.pdf), [installation manual PDF](https://www.flows.com/content/literature/Manuals/D10-IOM.pdf) | Verify body size and pulse configuration |
| D10-C-SRS pulse switch | [product page](https://www.flows.com/pulse-output-switch-for-d10-water-meters/), [D10 installation manual PDF](https://www.flows.com/content/literature/Manuals/D10-IOM.pdf) | Verify switch label and pulse rate |
| DFRobot SEN0257 | [manufacturer documentation](https://wiki.dfrobot.com/sen0257) | Exact model named |
| Watermark 200SS-15 | [product page](https://www.irrometer.com/200ss.html), [sensor sheet PDF](https://www.irrometer.com/pdf/403.pdf) | Exact family named; verify 15-foot lead |
| Watermark 200TS | [temperature sensor sheet PDF](https://irrometer.com/pdf/406.pdf) | Exact model named |
| Watermark 200SS-VA3 | [adapter sheet PDF](https://irrometer.com/pdf/427.pdf) | Exact model named |
| Rain Bird CP075 valve body | [manufacturer product page](https://store.rainbird.com/cp075-3-4-in-fpt-inline-irrigation-valve.html) | Valve body named; replacement solenoid model remains open |
| DIG 305DC-075 valve | [DC valve sheet PDF](https://www.digcorp.com/wp-content/uploads/2020/06/DC_Valves_031621.pdf), [product page](https://www.digcorp.com/professional-irrigation-products/300dc-3-4-and-1-vdc-valves/) | Requested model; verify received label |
| DIG S-305DC solenoid | [solenoid sheet PDF](https://www.digcorp.com/wp-content/uploads/digcorp/S-305DC.pdf) | Use only if the physical solenoid matches |
| Polycase WQ-44 | [product page](https://www.polycase.com/wq-44), [print template PDF](https://www.polycase.com/media/catalog/product/file/WQ-44S-PrintTemplate.pdf) | Working enclosure baseline; received SKU remains open |
| MAX31865 RTD converter | [Analog Devices datasheet PDF](https://www.analog.com/media/en/technical-documentation/data-sheets/MAX31865.pdf) | Applies only if MET-01 uses a PT100 sensor |

## MET-01 baseline

These links support the April 19 baseline. Physical labels and later loan records conflict with parts of that baseline.

| Baseline model | Manufacturer document | Status |
|---|---|---|
| Campbell EE181-L | [manual PDF](https://s.campbellsci.com/documents/us/manuals/ee181.pdf) | Verify label suffix and cable |
| Campbell 05103 | [manual PDF](https://s.campbellsci.com/documents/us/manuals/05103.pdf) | Later evidence mentions Met One sensors |
| Campbell 014A-L | [manual PDF](https://s.campbellsci.com/documents/us/manuals/014a.pdf) | Later evidence mentions a Met One cup sensor |
| T-PRO TD0030 PT100 | [manufacturer PT100 family page](https://tprosensor.com/products/pt100) | Exact TD0030 sheet still needed; later evidence mentions thermistors |

## Design candidates

| Candidate | Manufacturer document | Status |
|---|---|---|
| Onset S-LIB-M003 | [manual PDF](https://www.onsetcomp.com/sites/default/files/resources-documents/6708-G%20S-LIB%20Manual.pdf) | Model named in Johan's concept; interface remains open |
| Campbell TRH probe | None yet | Exact model required |
| Davis soil-moisture probe | None yet | Exact model required |
| Davis 2D sonic anemometer | None yet | Exact model required |
| McMaster bolt-on thermocouple | None yet | Thermocouple type and part number required |
| Apogee PAR sensor | None yet | Exact model required |
| Soil heat-flux sensor | None yet | Manufacturer and model required |
| Ultrasonic 9-in-1 RS485 sensor | None yet | Vendor, model, datasheet, power, and register map required |
| US915 LoRaWAN gateway | None yet | Select the exact RAKwireless model first |
| Solar panel | None yet | Verify the received SKU first |
| 3.7 V LiPo battery | None yet | Verify the received SKU, protection circuit, capacity, and polarity first |

## Link check

The repository validator checks internal links. External manufacturer links need a network check before each procurement or wiring decision because vendors can move files.
