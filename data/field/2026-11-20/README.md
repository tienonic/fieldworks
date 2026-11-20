# First field data, November 19–20, 2026

The first readings from a Green Grid node at the UC Davis Student Farm. Luis Blas installed one ENTS node on November 16 and exported this file on November 20.

| File | What it is |
|---|---|
| [sm-pilot-soil-temperature-2026-11-19.csv](sm-pilot-soil-temperature-2026-11-19.csv) | 56 readings from the node: sensor voltage and soil temperature, one every 14.7 minutes, 5:45 p.m. November 19 to 7:12 a.m. November 20 (Pacific). |
| [open-meteo-davis-model-2026-11-16-to-20.csv](open-meteo-davis-model-2026-11-16-to-20.csv) | Hourly model values for the Student Farm coordinates (38.5425, −121.7646): air temperature, soil temperature at 0, 6 and 18 cm, and rain. Used for comparison only. |

## What the readings show

- Soil temperature fell from 10.1 °C at dusk to a low of 6.0 °C around 1 a.m., then held near 6.6 °C until morning.
- The readings stay within 0.8 °C on average of the modeled surface (0 cm) soil temperature and read about 1.6 °C cooler than the 6 cm model. The probe is buried about 2 inches (5 cm) deep, per Luis.
- A small rise near 5 a.m. matches a short modeled rain shower.

## Limits

- **One channel.** Only the Watermark 200TS temperature channel through the VA3 adapter is present. The three soil-tension (moisture) channels are not in this file.
- **Estimated times.** The board has no real-time clock. `est_time` is reconstructed from the reading count; `earliest` and `latest` bound it, about ±16 minutes.
- **Coarse steps.** Temperature changes in steps of about 0.5 °C, set by the voltage resolution.
- **Partial record.** The file covers about 14% of the time since installation. Luis reported power problems over the three days before export, when about 84 mm of rain was modeled for November 18–19.
- **Station identity.** The node has no permanent station ID yet; it is labeled `SM-PILOT` in the dashboard.

## Columns

`count` reading number · `volts` sensor output (V) · `temp_c` soil temperature (°C) · `status` reading validity · `est_time` estimated time · `earliest`, `latest` bounds on that time.

Model data: [Open-Meteo](https://open-meteo.com/) forecast API with past days, fetched November 20, 2026, licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).
