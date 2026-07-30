# WX-CANDIDATE — Johan Weather-Station Concept

Status: candidate
Owner: Johan Marcial Gonzalez / decision owner unassigned
Updated: 2026-07-27
Evidence: `Instrument Cost.pdf`, `Station Possible Variables.pdf`, and `Suggestions and Problems.pdf`

## Purpose

Preserve Johan's proposed station concept without treating it as approved hardware, assigned inventory, or a purchasing authorization.

## Interface state

This record is not a station card yet. Nothing is approved, installed, or assigned to a node, so it has no valid data contract. Potential outputs such as temperature, humidity, wind, PAR, heat flux, radiation, and pollutant data remain questions until exact models and scientific requirements are selected.

The interface should show `no approved stream`, not blank charts or synthetic example values.

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
| integrated weather | ultrasonic 9-in-1 RS485 sensor, vendor/model absent | 1 | suggested alternative | RS485/likely Modbus; power and register map unresolved |

## Important correction

Two pyranometers do not automatically produce four-stream net radiation. The intended longwave-down, longwave-up, shortwave-down, and shortwave-up measurements require an instrument architecture that measures all four components or a documented alternative calculation.

The 9-in-1 description includes wind, temperature, RH, pressure, light, noise, PM2.5, and PM10, but the source does not give a vendor, model, datasheet, accuracy, supply voltage, Modbus register map, ingress rating, or calibration evidence.

## Decision gate

For each proposed instrument, record:

1. scientific question and required accuracy;
2. exact manufacturer and model;
3. ownership, quantity, cost, and procurement route;
4. output protocol and supply requirements;
5. ENTS adapter and firmware path;
6. mounting, calibration, maintenance, and return terms;
7. overlap with Phase I or loaned MET-01 instruments.

Until that record exists, these sensors remain a concept and are not allocated to a station.
