# WX-CANDIDATE: Johan weather-station concept

Status: candidate
Owner: Johan Marcial Gonzalez / decision owner unassigned
Updated: 2026-07-27
Evidence: `Instrument Cost.pdf`, `Station Possible Variables.pdf`, and `Suggestions and Problems.pdf`

## Purpose

Record Johan's station concept in one place while approval, inventory, and purchasing remain open.

## Interface state

Status: concept only. Hardware, node assignment, and data contract await approval. Potential outputs include temperature, humidity, wind, PAR, heat flux, radiation, and pollutant data. Exact models and scientific requirements remain open.

Show `no approved stream` until approval.

## Proposed instruments

| Role | Proposed description | Quantity | Selection state | Connection state |
|---|---|---:|---|---|
| air temperature/RH | Campbell TRH probe, exact model absent | 1 | unselected | unknown until model selected |
| soil moisture | Davis soil-moisture probe, exact model absent | 1 | unselected | unknown |
| wind speed/direction | Davis 2D sonic anemometer, exact variant absent | 1 | unselected | unknown |
| surface temperature | McMaster bolt-on thermocouple, type absent | 1 | unselected | unknown |
| PAR | Apogee quantum/PAR sensor, exact model absent | 1 | unselected | unknown |
| soil heat flux | manufacturer/model absent | 1 | unselected | unknown |
| net radiation | Onset S-LIB-M003 pyranometer | 2 | proposed | Onset smart-sensor interface; ENTS path unresolved |
| integrated weather | ultrasonic 9-in-1 RS485 sensor, vendor/model absent | 1 | suggested alternative | RS485; Modbus unverified; power and register map unresolved |

## Important correction

Two pyranometers alone cannot produce four-stream net radiation. Measuring longwave down, longwave up, shortwave down, and shortwave up requires a four-component instrument or a documented calculation.

The 9-in-1 description includes wind, temperature, RH, pressure, light, noise, PM2.5, and PM10. The source gives no vendor, model, datasheet, accuracy, supply voltage, Modbus register map, ingress rating, or calibration evidence.

## Decision gate

For each proposed instrument, record:

1. scientific question and required accuracy;
2. exact manufacturer and model;
3. ownership, quantity, cost, and procurement route;
4. output protocol and supply requirements;
5. ENTS adapter and firmware path;
6. mounting, calibration, maintenance, and return terms;
7. overlap with Phase I or loaned MET-01 instruments.

Complete this record before assigning sensors to a station.
