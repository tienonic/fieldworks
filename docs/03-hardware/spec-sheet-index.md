# Spec sheet index

Status: working
Owner: unassigned
Updated: 2026-08-02

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

## MET-01 baseline

The collaborator's inspection report identifies MET-01 as a **Davis Vantage Pro2 Plus wireless weather station, product number 6162** and reports the `TEMP HUM`, `WIND`, `RAIN`, `SUN`, and `UV` ports as populated. A dated inventory artifact and exact sensor labels remain required before treating the model details as independently verified.

| Baseline model | Manufacturer document | Status |
|---|---|---|
| Davis Vantage Pro2 Plus 6162 | [Davis Vantage Pro2 support/manual index](https://support.davisinstruments.com/category/2adgkl7szt-vantage-pro-2) | Reported existing in-kind station; dated inventory artifact and transmitter ID pending |
| Vantage Pro2 temperature/RH assembly | [Davis Vantage Pro2 support/manual index](https://support.davisinstruments.com/category/2adgkl7szt-vantage-pro-2) | `TEMP HUM` reported populated; exact internal board revision remains to verify |
| Davis Vantage Pro2 anemometer / wind vane; current replacement SKU 6410 | [Davis 6410 product page](https://www.davisinstruments.com/products/anemometer-for-vantage-pro2-vantage-pro) | `WIND` reported populated; exact installed revision, condition and alignment pending |
| 6162-generation Davis rain collector | [Davis Vantage Pro2 support/manual index](https://support.davisinstruments.com/category/2adgkl7szt-vantage-pro-2) | `RAIN` reported populated; exact collector assembly and `rain_size` remain to verify |
| Davis-compatible solar radiation sensor; exact SKU pending | [Davis 6450 product page](https://www.davisinstruments.com/products/solar-radiation-sensor) | `SUN` reported populated; do not call it 6450 until its label is checked |
| Davis-compatible UV sensor; exact SKU pending | [Davis 6490 product page](https://www.davisinstruments.com/products/uv-sensor) | `UV` reported populated; do not call it 6490 until its label is checked |
| Davis WeatherLink Live receiver | [WeatherLink Live product page](https://www.davisinstruments.com/pages/weatherlink-live), [Local API documentation](https://weatherlink.github.io/weatherlink-live-local-api/) | Required receiver/network bridge; exact regional SKU must match the transmitter and is not recorded as purchased |

## Design candidates

| Candidate | Manufacturer document | Status |
|---|---|---|
| Onset S-LIB-M003 | [manual PDF](https://www.onsetcomp.com/sites/default/files/resources-documents/6708-G%20S-LIB%20Manual.pdf) | Model named in Johan's concept; interface remains open |
| Campbell TRH probe | None yet | Exact model required |
| Davis soil-moisture probe | None yet | Exact model required |
| Davis 2D sonic anemometer | None yet | Exact variant, output, power, environmental rating required |
| McMaster bolt-on thermocouple | None yet | Thermocouple type and part number required |
| Apogee PAR sensor | None yet | Exact model, analog/digital output, calibration required |
| Soil heat-flux sensor | None yet | Manufacturer, model, output, installation method required |
| Ultrasonic 9-in-1 RS485 sensor | None yet | Vendor, model, datasheet, power, and register map required |
| US915 LoRaWAN gateway | None yet | Select the exact RAKwireless model first |
| Solar panel | None yet | Verify the received SKU first |
| 3.7 V LiPo battery | None yet | Verify the received SKU, protection circuit, capacity, and polarity first |

## Link check

The repository validator checks internal links. External manufacturer links need a network check before each procurement or wiring decision because vendors can move files.
