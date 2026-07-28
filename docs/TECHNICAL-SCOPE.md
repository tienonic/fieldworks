# Technical scope

A useful field record needs more than a sensor value. It needs the time, place, units, calibration, and field activity around it. FieldWorks groups that information into four areas.

## Weather

- Air temperature and humidity
- Wind speed and direction
- Solar radiation
- Rainfall when the site needs it

## Soil

- Soil temperature
- Soil moisture or water tension
- Measurements tied to depth and location

## Irrigation

- Flow
- Pressure
- Irrigation start and stop events
- Notes about valves, zones, and maintenance

## System health

- Battery and power state
- Communications state
- Sensor faults and missing data
- Calibration and maintenance history

## Design rules

- Use exact sensor models and documented interfaces
- Keep raw measurements separate from derived values
- Record units, timestamps, location, calibration, and quality flags
- Show failures and missing data instead of hiding them
- Keep the system serviceable with ordinary tools
- A bench result is not a field result
