#!/usr/bin/env python3
"""Build the provisioned Student Farm Grafana dashboard."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "deploy" / "grafana" / "dashboards" / "student-farm-sensors.json"
DATASOURCE = {"type": "influxdb", "uid": "fieldworks-influxdb"}
STATION_FILTER = '  |> filter(fn: (r) => r["station_id"] =~ /^${station_id:regex}$/)'
REPOSITORY_URL = "https://github.com/tienonic/fieldworks"
NO_DATA_TEXT = "No accepted records in selected window"
SERIES_DISPLAY_NAME = "${__field.labels.station_id} ${__field.name}"


def flux_query(
    fields: list[str],
    *,
    station_type: str | None = None,
    source_system: str | None = None,
    aggregate: str = "mean",
) -> str:
    encoded_fields = ", ".join(json.dumps(field) for field in fields)
    lines = [
        "from(bucket: v.defaultBucket)",
        "  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)",
        '  |> filter(fn: (r) => r["_measurement"] == "station_metrics")',
    ]
    if station_type:
        lines.append(f'  |> filter(fn: (r) => r["station_type"] == {json.dumps(station_type)})')
    if source_system:
        lines.append(f'  |> filter(fn: (r) => r["source_system"] == {json.dumps(source_system)})')
    lines.extend(
        [
            STATION_FILTER,
            f"  |> filter(fn: (r) => contains(value: r._field, set: [{encoded_fields}]))",
        ]
    )
    if aggregate:
        lines.append(f"  |> aggregateWindow(every: v.windowPeriod, fn: {aggregate}, createEmpty: false)")
    return "\n".join(lines)


def base_panel(panel_id: int, title: str, panel_type: str, x: int, y: int, w: int, h: int) -> dict[str, Any]:
    return {
        "datasource": DATASOURCE if panel_type not in {"row", "text"} else None,
        "gridPos": {"h": h, "w": w, "x": x, "y": y},
        "id": panel_id,
        "title": title,
        "type": panel_type,
    }


def row_panel(panel_id: int, title: str, y: int) -> dict[str, Any]:
    panel = base_panel(panel_id, title, "row", 0, y, 24, 1)
    panel.update({"collapsed": False, "panels": []})
    panel.pop("datasource")
    return panel


def text_panel(panel_id: int, title: str, content: str, y: int, *, height: int = 4) -> dict[str, Any]:
    panel = base_panel(panel_id, title, "text", 0, y, 24, height)
    panel.update({"options": {"content": content, "mode": "markdown"}, "transparent": True})
    panel.pop("datasource")
    return panel


def field_defaults(unit: str, *, minimum: float | None = None) -> dict[str, Any]:
    defaults: dict[str, Any] = {
        "color": {"mode": "palette-classic"},
        "custom": {
            "axisCenteredZero": False,
            "axisColorMode": "text",
            "axisLabel": "",
            "axisPlacement": "auto",
            "drawStyle": "line",
            "fillOpacity": 8,
            "gradientMode": "none",
            "hideFrom": {"legend": False, "tooltip": False, "viz": False},
            "lineInterpolation": "linear",
            "lineWidth": 2,
            "pointSize": 5,
            "scaleDistribution": {"type": "linear"},
            "showPoints": "auto",
            "spanNulls": False,
            "stacking": {"group": "A", "mode": "none"},
            "thresholdsStyle": {"mode": "off"},
        },
        "mappings": [],
        "displayName": SERIES_DISPLAY_NAME,
        "noValue": NO_DATA_TEXT,
        "thresholds": {
            "mode": "absolute",
            "steps": [{"color": "green", "value": None}, {"color": "red", "value": 80}],
        },
        "unit": unit,
    }
    if minimum is not None:
        defaults["min"] = minimum
    return defaults


def timeseries_panel(
    panel_id: int,
    title: str,
    description: str,
    query: str,
    unit: str,
    x: int,
    y: int,
    w: int = 12,
    h: int = 8,
    *,
    minimum: float | None = None,
) -> dict[str, Any]:
    panel = base_panel(panel_id, title, "timeseries", x, y, w, h)
    panel.update(
        {
            "description": description,
            "fieldConfig": {"defaults": field_defaults(unit, minimum=minimum), "overrides": []},
            "options": {
                "legend": {"calcs": ["lastNotNull"], "displayMode": "list", "placement": "bottom", "showLegend": True},
                "tooltip": {"hideZeros": False, "mode": "multi", "sort": "none"},
            },
            "targets": [{"datasource": DATASOURCE, "query": query, "refId": "A"}],
        }
    )
    return panel


def state_panel(
    panel_id: int,
    title: str,
    description: str,
    query: str,
    x: int,
    y: int,
    w: int = 12,
    h: int = 8,
) -> dict[str, Any]:
    panel = base_panel(panel_id, title, "state-timeline", x, y, w, h)
    panel.update(
        {
            "description": description,
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "thresholds"},
                    "custom": {"fillOpacity": 70, "lineWidth": 0, "spanNulls": False},
                    "mappings": [
                        {"options": {"false": {"color": "green", "index": 0, "text": "clear"}, "true": {"color": "red", "index": 1, "text": "alarm"}}, "type": "value"},
                        {"options": {"closed": {"color": "blue", "index": 2, "text": "closed"}, "open": {"color": "green", "index": 3, "text": "open"}, "unknown": {"color": "orange", "index": 4, "text": "unknown"}}, "type": "value"},
                    ],
                    "noValue": NO_DATA_TEXT,
                    "thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": None}]},
                },
                "overrides": [],
            },
            "options": {
                "alignValue": "left",
                "legend": {"displayMode": "list", "placement": "bottom", "showLegend": True},
                "mergeValues": True,
                "rowHeight": 0.9,
                "showValue": "auto",
                "tooltip": {"mode": "single", "sort": "none"},
            },
            "targets": [{"datasource": DATASOURCE, "query": query, "refId": "A"}],
        }
    )
    return panel


def table_column_override(
    field_name: str,
    display_name: str,
    *,
    width: int | None = None,
    hidden: bool = False,
) -> dict[str, Any]:
    properties: list[dict[str, Any]] = [{"id": "displayName", "value": display_name}]
    if width is not None:
        properties.append({"id": "custom.width", "value": width})
    if hidden:
        properties.append({"id": "custom.hidden", "value": True})
    return {"matcher": {"id": "byName", "options": field_name}, "properties": properties}


def table_panel(
    panel_id: int,
    title: str,
    description: str,
    query: str,
    x: int,
    y: int,
    w: int,
    h: int,
    *,
    overrides: list[dict[str, Any]] | None = None,
    cell_height: str = "sm",
) -> dict[str, Any]:
    panel = base_panel(panel_id, title, "table", x, y, w, h)
    panel.update(
        {
            "description": description,
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "thresholds"},
                    "custom": {"align": "auto", "cellOptions": {"type": "auto"}, "inspect": False},
                    "mappings": [],
                    "noValue": NO_DATA_TEXT,
                    "thresholds": {"mode": "absolute", "steps": [{"color": "green", "value": None}]},
                },
                "overrides": overrides or [],
            },
            "options": {"cellHeight": cell_height, "footer": {"enablePagination": False, "show": False}, "showHeader": True},
            "targets": [{"datasource": DATASOURCE, "query": query, "refId": "A"}],
        }
    )
    if overrides:
        hidden_names = [item["matcher"]["options"] for item in overrides
                        if any(p["id"] == "custom.hidden" and p["value"] for p in item["properties"])]
        if hidden_names:
            panel["transformations"] = [{"id": "organize", "options": {
                "excludeByName": {name: True for name in hidden_names},
                "indexByName": {"station_id": 0, "_time": 1, "_value": 2}, "renameByName": {}}}]
            panel["fieldConfig"]["defaults"]["custom"]["wrapText"] = True
    return panel


def stat_panel(panel_id: int, title: str, description: str, query: str, x: int, y: int, w: int, h: int) -> dict[str, Any]:
    panel = base_panel(panel_id, title, "stat", x, y, w, h)
    panel.update(
        {
            "description": description,
            "fieldConfig": {
                "defaults": {
                    "color": {"mode": "thresholds"},
                    "mappings": [],
                    "noValue": NO_DATA_TEXT,
                    "thresholds": {"mode": "absolute", "steps": [{"color": "red", "value": None}, {"color": "green", "value": 1}]},
                    "unit": "short",
                },
                "overrides": [],
            },
            "options": {
                "colorMode": "value",
                "graphMode": "none",
                "justifyMode": "auto",
                "orientation": "auto",
                "reduceOptions": {"calcs": ["lastNotNull"], "fields": "", "values": False},
                "showPercentChange": False,
                "textMode": "auto",
                "wideLayout": True,
            },
            "targets": [{"datasource": DATASOURCE, "query": query, "refId": "A"}],
        }
    )
    return panel


def build_dashboard() -> dict[str, Any]:
    panels: list[dict[str, Any]] = []
    panel_id = 1
    y = 0

    def add(panel: dict[str, Any]) -> None:
        nonlocal panel_id
        panels.append(panel)
        panel_id += 1

    add(
        text_panel(
            panel_id,
            "Read first",
            (
                "**Review only.** This dashboard is not evidence of field deployment. Review **Quality state** flags before using a value; "
                "a station becomes live only after documented acceptance.\n\n"
                "`example_not_live` marks synthetic test data, not field observations. Keep fixture records in a test bucket. "
                "Empty panels mean no accepted records in the time window.\n\n"
                "Use **Station** to filter. Start with **System health**, then **Irrigation**, **Soil profile**, **External systems**, "
                f"and **MET-01 weather**. [Repository record]({REPOSITORY_URL})"
            ),
            y,
            height=5,
        )
    )
    y += 5

    add(row_panel(panel_id, "System health", y))
    y += 1
    reporting_query = "\n".join(
        [
            "from(bucket: v.defaultBucket)",
            "  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)",
            '  |> filter(fn: (r) => r["_measurement"] == "station_metrics" and r["_field"] == "record_count")',
            STATION_FILTER,
            '  |> group(columns: ["station_id"])',
            "  |> last()",
            "  |> group()",
            '  |> count(column: "_value")',
        ]
    )
    add(stat_panel(panel_id, "Reporting stations", "Stations with at least one record in the selected time range.", reporting_query, 0, y, 6, 8))
    last_seen_query = "\n".join(
        [
            "from(bucket: v.defaultBucket)",
            "  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)",
            '  |> filter(fn: (r) => r["_measurement"] == "station_metrics" and r["_field"] == "record_count")',
            STATION_FILTER,
            '  |> group(columns: ["station_id", "station_type", "source_system"])',
            "  |> last()",
            '  |> keep(columns: ["_time", "station_id", "station_type", "source_system"])',
            "  |> group()",
        ]
    )
    add(
        table_panel(
            panel_id,
            "Last seen",
            "Use the timestamp to identify silent or stale stations.",
            last_seen_query,
            6,
            y,
            18,
            8,
            overrides=[
                table_column_override("_time", "Last observed", width=230),
                table_column_override("station_id", "Station", width=150),
                table_column_override("station_type", "Station type", width=160),
                table_column_override("source_system", "Source", width=160),
            ],
        )
    )
    y += 8
    quality_query = "\n".join(
        [
            "from(bucket: v.defaultBucket)",
            "  |> range(start: v.timeRangeStart, stop: v.timeRangeStop)",
            '  |> filter(fn: (r) => r["_measurement"] == "station_metrics" and r["_field"] == "quality_state")',
            STATION_FILTER,
            '  |> group(columns: ["station_id", "station_type", "source_system"])',
            "  |> last()",
            '  |> keep(columns: ["_time", "_value", "station_id", "station_type", "source_system"])',
            "  |> group()",
        ]
    )
    add(
        table_panel(
            panel_id,
            "Quality state",
            "Review flags before using a value. Station type and source are retained in the query but hidden here to keep the flags readable.",
            quality_query,
            0,
            y,
            24,
            10,
            overrides=[
                table_column_override("_time", "Observed", width=230),
                table_column_override("_value", "Quality flags", width=710),
                table_column_override("station_id", "Station", width=180),
                table_column_override("station_type", "Station type", hidden=True),
                table_column_override("source_system", "Source", hidden=True),
            ],
            cell_height="md",
        )
    )
    y += 10
    add(timeseries_panel(panel_id, "Battery voltage", "ENTS and supported external-source battery telemetry.", flux_query(["battery_v"], aggregate="mean"), "volt", 0, y, 8, 8, minimum=0))
    add(timeseries_panel(panel_id, "LoRaWAN RSSI", "NodeFlow LoRaWAN received signal strength.", flux_query(["rssi_dbm"], source_system="nodeflow_lorawan", aggregate="mean"), "dBm", 8, y, 8, 8))
    add(timeseries_panel(panel_id, "LoRaWAN SNR", "NodeFlow LoRaWAN signal-to-noise ratio.", flux_query(["snr_db"], source_system="nodeflow_lorawan", aggregate="mean"), "dB", 16, y, 8, 8))
    y += 8

    add(row_panel(panel_id, "Irrigation", y))
    y += 1
    add(timeseries_panel(panel_id, "Flow rate", "D10 pulse-derived flow after pulse resolution and timing are verified.", flux_query(["flow_rate_gpm"], station_type="irrigation_head"), "gpm", 0, y, minimum=0))
    add(timeseries_panel(panel_id, "Line pressure", "SEN0257 pressure after divider correction and reference calibration.", flux_query(["pressure_psi"], station_type="irrigation_head"), "pressurepsi", 12, y, minimum=0))
    y += 8
    add(timeseries_panel(panel_id, "Cumulative volume", "Cumulative D10 volume. Counter resets require an explicit quality flag.", flux_query(["volume_total_gal"], station_type="irrigation_head", aggregate="last"), "gallons", 0, y, minimum=0))
    add(state_panel(panel_id, "Valve command", "Command history only. The current design has no valve-position feedback.", flux_query(["valve_command"], station_type="irrigation_head", aggregate="last"), 12, y))
    y += 8

    add(row_panel(panel_id, "Soil profile", y))
    y += 1
    add(timeseries_panel(panel_id, "Soil water tension by depth", "Three Watermark 200SS channels after VA3 conversion and bench calibration.", flux_query(["tension_shallow_kpa", "tension_middle_kpa", "tension_deep_kpa"], station_type="soil_profile"), "pressurekpa", 0, y, minimum=0))
    add(timeseries_panel(panel_id, "Soil temperature", "Watermark 200TS temperature after VA3 conversion and reference comparison.", flux_query(["soil_temp_c"], station_type="soil_profile"), "celsius", 12, y))
    y += 8

    add(row_panel(panel_id, "External systems", y))
    y += 1
    add(timeseries_panel(panel_id, "HOBO air temperature", "HOBO MX value after sensor-ID and unit mapping.", flux_query(["air_temp_c"], source_system="hobo_mx"), "celsius", 0, y))
    add(timeseries_panel(panel_id, "HOBO relative humidity", "HOBO MX value after sensor-ID and unit mapping.", flux_query(["relative_humidity_pct"], source_system="hobo_mx"), "percent", 12, y, minimum=0))
    y += 8
    add(timeseries_panel(panel_id, "HOBO light", "HOBO MX light channel after channel identity is verified.", flux_query(["light_lux"], source_system="hobo_mx"), "lux", 0, y, minimum=0))
    add(timeseries_panel(panel_id, "HOBO external analog input", "Raw external-channel voltage retained for conversion checks.", flux_query(["external_analog_raw_v"], source_system="hobo_mx"), "volt", 12, y, minimum=0))
    y += 8
    add(timeseries_panel(panel_id, "Signalizer flow rate", "Active 4–20 mA flow after meter range and logger scaling are verified.", flux_query(["flow_rate_gpm"], source_system="signalizer"), "gpm", 0, y, minimum=0))
    add(timeseries_panel(panel_id, "Signalizer cumulative volume", "Pulse-derived volume after pulse resolution and reset handling are verified.", flux_query(["volume_total_gal"], source_system="signalizer", aggregate="last"), "gallons", 12, y, minimum=0))
    y += 8
    add(state_panel(panel_id, "Signalizer alarm", "Alarm-contact state. This panel is separate from numeric flow and volume.", flux_query(["meter_alarm"], source_system="signalizer", aggregate="last"), 0, y, 24, 7))
    y += 7

    add(row_panel(panel_id, "MET-01 weather", y))
    y += 1
    add(timeseries_panel(panel_id, "MET-01 air temperature", "Davis 6162 temperature converted from the retained WeatherLink source value.", flux_query(["air_temp_c"], station_type="met_sandbox", source_system="weatherlink"), "celsius", 0, y))
    add(timeseries_panel(panel_id, "MET-01 relative humidity", "Davis 6162 relative humidity after channel verification.", flux_query(["relative_humidity_pct"], station_type="met_sandbox", source_system="weatherlink"), "percent", 12, y, minimum=0))
    y += 8
    add(timeseries_panel(panel_id, "MET-01 wind speed", "WeatherLink wind speed converted from mph to m/s.", flux_query(["wind_speed_ms"], station_type="met_sandbox", source_system="weatherlink"), "suffix:m/s", 0, y, minimum=0))
    add(timeseries_panel(panel_id, "MET-01 wind direction", "Latest direction is shown without arithmetic averaging across north.", flux_query(["wind_direction_deg"], station_type="met_sandbox", source_system="weatherlink", aggregate="last"), "degree", 12, y, minimum=0))
    y += 8
    add(timeseries_panel(panel_id, "MET-01 daily rainfall", "Daily cumulative rainfall converted from WeatherLink counts using the reported collector size.", flux_query(["rainfall_daily_mm"], station_type="met_sandbox", source_system="weatherlink", aggregate="last"), "suffix:mm", 0, y, minimum=0))
    add(timeseries_panel(panel_id, "MET-01 rain rate", "WeatherLink rain-rate counts converted to millimeters per hour.", flux_query(["rain_rate_mm_hr"], station_type="met_sandbox", source_system="weatherlink"), "suffix:mm/h", 12, y, minimum=0))
    y += 8
    add(timeseries_panel(panel_id, "MET-01 solar radiation", "Davis SUN-channel value after physical sensor and WeatherLink channel verification.", flux_query(["solar_radiation_wm2"], station_type="met_sandbox", source_system="weatherlink"), "suffix:W/m²", 0, y, minimum=0))
    add(timeseries_panel(panel_id, "MET-01 UV index", "Davis UV-channel value after physical sensor and WeatherLink channel verification.", flux_query(["uv_index"], station_type="met_sandbox", source_system="weatherlink"), "short", 12, y, minimum=0))

    return {
        "annotations": {"list": []},
        "description": "FieldWorks Green Grid Student Farm sensor dashboard.",
        "editable": False,
        "fiscalYearStartMonth": 0,
        "graphTooltip": 1,
        "id": None,
        "links": [],
        "panels": panels,
        "refresh": "5m",
        "schemaVersion": 41,
        "tags": ["fieldworks", "student-farm", "provisioned"],
        "templating": {
            "list": [
                {
                    "allValue": ".*",
                    "current": {"selected": True, "text": "All", "value": "$__all"},
                    "datasource": DATASOURCE,
                    "definition": "",
                    "hide": 0,
                    "includeAll": True,
                    "label": "Station",
                    "multi": True,
                    "name": "station_id",
                    "options": [],
                    "query": (
                        'import "influxdata/influxdb/schema"\n'
                        'schema.tagValues(bucket: v.defaultBucket, tag: "station_id", '
                        'predicate: (r) => r._measurement == "station_metrics", start: -30d)'
                    ),
                    "refresh": 2,
                    "regex": "",
                    "skipUrlSync": False,
                    "sort": 1,
                    "type": "query",
                }
            ]
        },
        "time": {"from": "now-24h", "to": "now"},
        "timepicker": {"refresh_intervals": ["1m", "5m", "15m", "1h"]},
        "timezone": "browser",
        "title": "Student Farm sensors",
        "uid": "student-farm-sensors",
        "version": 1,
        "weekStart": "",
    }


def render_dashboard() -> str:
    return json.dumps(build_dashboard(), indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true", help="Fail if the output does not match the generator")
    args = parser.parse_args(argv)
    rendered = render_dashboard()
    if args.check:
        if not args.output.is_file() or args.output.read_text(encoding="utf-8") != rendered:
            print(f"dashboard is stale: {args.output}", file=sys.stderr)
            return 1
        print(f"dashboard is current: {args.output}")
        return 0
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
