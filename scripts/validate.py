#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []

REQUIRED = [
    "README.md",
    "DOCUMENT-STANDARD.md",
    "docs/01-architecture/network-overview.mmd",
    "docs/01-architecture/network-overview.svg",
    "docs/02-stations/station-atlas.md",
    "docs/02-stations/station-atlas.mmd",
    "docs/02-stations/station-atlas.svg",
    "docs/02-stations/data-contracts.md",
    "docs/02-stations/data-dictionary.csv",
    "docs/02-stations/external-integrations.md",
    "docs/03-hardware/specifications.md",
    "docs/03-hardware/spec-sheet-index.md",
    "docs/03-hardware/component-specifications.csv",
    "docs/03-hardware/connection-matrix.csv",
    "docs/03-hardware/station-bom.csv",
    "docs/04-procurement/orders.md",
    "docs/04-procurement/orders.csv",
    "docs/04-procurement/needs.md",
    "docs/04-procurement/needs.csv",
    "docs/04-procurement/purchase-list.md",
    "docs/04-procurement/purchase-list.csv",
    "docs/04-procurement/physical-inventory.md",
    "docs/04-procurement/physical-inventory.csv",
    "docs/09-dashboard/grafana.md",
    "docs/09-dashboard/runtime-acceptance-2026-08-24.md",
    "docs/09-dashboard/telemetry-schema.md",
    "deploy/grafana/.env.example",
    "deploy/grafana/compose.yaml",
    "deploy/grafana/provisioning/datasources/influxdb.yaml",
    "deploy/grafana/provisioning/dashboards/dashboards.yaml",
    "deploy/grafana/provisioning/alerting/empty.yaml",
    "deploy/grafana/provisioning/plugins/empty.yaml",
    "deploy/grafana/dashboards/student-farm-sensors.json",
    "scripts/build_dashboard.py",
    "scripts/check_grafana_env.py",
    "scripts/ingest_telemetry.py",
    "tests/fixtures/telemetry.jsonl",
    "tests/test_grafana_env.py",
    "tests/test_telemetry.py",
]
STATIONS = ["IH-01", "IH-02", "SM-01", "SM-02", "SM-03", "SM-04", "MET-01", "WX-CANDIDATE"]
ALLOWED_STATION_TYPES = {
    "irrigation_head",
    "soil_profile",
    "met_sandbox",
    "external_hobo",
    "external_meter",
}
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
PNG_KEYWORD = b"mermaid-source-sha256\x00"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def png_source_hash(path: Path) -> str | None:
    data = path.read_bytes()
    if not data.startswith(PNG_SIGNATURE):
        return None
    offset = len(PNG_SIGNATURE)
    while offset < len(data):
        length = struct.unpack(">I", data[offset : offset + 4])[0]
        chunk_type = data[offset + 4 : offset + 8]
        payload = data[offset + 8 : offset + 8 + length]
        if chunk_type == b"tEXt" and payload.startswith(PNG_KEYWORD):
            return payload[len(PNG_KEYWORD) :].decode("ascii", errors="ignore")
        offset += 12 + length
    return None


def run_check(command: list[str], label: str) -> None:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode != 0:
        output = (result.stdout + result.stderr).strip()
        ERRORS.append(f"{label} failed" + (f":\n{output}" if output else ""))


for rel in REQUIRED:
    if not (ROOT / rel).is_file():
        ERRORS.append(f"missing required file: {rel}")

for station in STATIONS:
    path = ROOT / "docs" / "02-stations" / f"{station}.md"
    if not path.is_file():
        ERRORS.append(f"missing station document: {station}")
        continue
    station_text = path.read_text(encoding="utf-8")
    if station not in station_text:
        ERRORS.append(f"station ID absent from document: {station}")
    if station == "WX-CANDIDATE":
        if "no approved stream" not in station_text:
            ERRORS.append("WX-CANDIDATE must state that no data stream is approved")
    elif "Data expected" not in station_text:
        ERRORS.append(f"station document lacks expected-data interface: {station}")
    if "spec-sheet-index.md" not in station_text:
        ERRORS.append(f"station document lacks spec-sheet index link: {station}")

dictionary_path = ROOT / "docs" / "02-stations" / "data-dictionary.csv"
if dictionary_path.is_file():
    dictionary_rows = read_csv(dictionary_path)
    expected_columns = {
        "station_type",
        "applies_to",
        "field_name",
        "display_name",
        "unit",
        "storage_type",
        "source",
        "transformation",
        "required",
        "confidence",
        "notes",
    }
    if not dictionary_rows or set(dictionary_rows[0]) != expected_columns:
        ERRORS.append("data dictionary columns do not match the telemetry contract")
    for station in STATIONS[:-1]:
        matching = [row for row in dictionary_rows if station in row.get("applies_to", "").split()]
        if len(matching) < 5:
            ERRORS.append(f"data dictionary has too few fields for {station}: {len(matching)}")
    if not any(row.get("field_name") == "source_system" and row.get("storage_type") == "tag" for row in dictionary_rows):
        ERRORS.append("data dictionary lacks canonical source_system tag")

connection_path = ROOT / "docs" / "03-hardware" / "connection-matrix.csv"
if connection_path.is_file():
    for line, row in enumerate(read_csv(connection_path), 2):
        if row.get("station_type") not in ALLOWED_STATION_TYPES:
            ERRORS.append(f"connection matrix uses a non-contract station type: {connection_path.relative_to(ROOT)}:{line}")

spec_path = ROOT / "docs" / "03-hardware" / "component-specifications.csv"
if spec_path.is_file():
    for row in read_csv(spec_path):
        component = row.get("component_id", "unknown")
        source = row.get("spec_sheet_url", "").strip()
        if not source:
            ERRORS.append(f"component lacks spec-sheet source or pending marker: {component}")
        elif "http" not in source and not source.startswith("pending_"):
            ERRORS.append(f"invalid spec-sheet source: {component} -> {source}")

for path in ROOT.rglob("*.csv"):
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        ERRORS.append(f"empty CSV: {path.relative_to(ROOT)}")
        continue
    width = len(rows[0])
    for line, row in enumerate(rows[1:], 2):
        if len(row) != width:
            ERRORS.append(f"malformed CSV: {path.relative_to(ROOT)}:{line}; expected {width} columns and found {len(row)}")

link_pattern = re.compile(r"!?(?:\[[^]]*\])\(([^)]+)\)")
for path in ROOT.rglob("*.md"):
    text = path.read_text(encoding="utf-8")
    for target in link_pattern.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0]
        if clean and not (path.parent / clean).resolve().exists():
            ERRORS.append(f"broken link: {path.relative_to(ROOT)} -> {target}")

try:
    tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
except (subprocess.CalledProcessError, FileNotFoundError):
    tracked = []
for rel in tracked:
    lower = rel.lower()
    if lower.endswith((".eml", ".msg", ".pst", ".mbox", ".xlsx", ".xls", ".pdf", ".key", ".pem")):
        ERRORS.append(f"private/binary artifact tracked: {rel}")
    if lower.endswith("/.env") or lower == ".env":
        ERRORS.append(f"local secret environment tracked: {rel}")

for path in ROOT.rglob("*.mmd"):
    if "flowchart" not in path.read_text(encoding="utf-8"):
        ERRORS.append(f"Mermaid source lacks flowchart: {path.relative_to(ROOT)}")
    svg = path.with_suffix(".svg")
    if not svg.is_file() or svg.stat().st_size == 0:
        ERRORS.append(f"missing Mermaid render: {svg.relative_to(ROOT)}")
        continue
    svg_text = svg.read_text(encoding="utf-8", errors="ignore")
    if "<svg" not in svg_text:
        ERRORS.append(f"invalid Mermaid render: {svg.relative_to(ROOT)}")
        continue
    match = re.search(r"mermaid-source-sha256: ([0-9a-f]{64})", svg_text)
    source_text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    expected = hashlib.sha256(source_text.encode("utf-8")).hexdigest()
    if not match:
        ERRORS.append(f"Mermaid render lacks source hash: {svg.relative_to(ROOT)}")
    elif match.group(1) != expected:
        ERRORS.append(f"stale Mermaid render: {svg.relative_to(ROOT)}")
    png = path.with_suffix(".png")
    if png.is_file():
        png_hash = png_source_hash(png)
        if not png_hash:
            ERRORS.append(f"Mermaid PNG lacks source hash: {png.relative_to(ROOT)}")
        elif png_hash != expected:
            ERRORS.append(f"stale Mermaid PNG: {png.relative_to(ROOT)}")

dashboard_path = ROOT / "deploy" / "grafana" / "dashboards" / "student-farm-sensors.json"
if dashboard_path.is_file():
    try:
        dashboard = json.loads(dashboard_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        ERRORS.append(f"invalid Grafana dashboard JSON: {exc}")
    else:
        if dashboard.get("uid") != "student-farm-sensors":
            ERRORS.append("Grafana dashboard has the wrong stable UID")
        if dashboard.get("time") != {"from": "now-24h", "to": "now"}:
            ERRORS.append("Grafana dashboard does not use the required 24-hour default window")
        panels = dashboard.get("panels", [])
        if len(panels) < 30:
            ERRORS.append(f"Grafana dashboard has too few panels: {len(panels)}")
        panel_ids = [panel.get("id") for panel in panels]
        if None in panel_ids or len(panel_ids) != len(set(panel_ids)):
            ERRORS.append("Grafana dashboard contains missing or duplicate panel IDs")
        query_text = "\n".join(target.get("query", "") for panel in panels for target in panel.get("targets", []))
        for field in (
            "battery_v",
            "rssi_dbm",
            "snr_db",
            "flow_rate_gpm",
            "pressure_psi",
            "volume_total_gal",
            "valve_command",
            "tension_shallow_kpa",
            "tension_middle_kpa",
            "tension_deep_kpa",
            "soil_temp_c",
            "light_lux",
            "external_analog_raw_v",
            "meter_alarm",
            "air_temp_c",
            "relative_humidity_pct",
            "wind_speed_ms",
            "wind_direction_deg",
            "rainfall_daily_mm",
            "rain_rate_mm_hr",
            "solar_radiation_wm2",
            "uv_index",
        ):
            if field not in query_text:
                ERRORS.append(f"Grafana dashboard does not query required field: {field}")
        for source_system in ("nodeflow_lorawan", "weatherlink", "hobo_mx", "signalizer"):
            if source_system not in query_text and source_system != "nodeflow_lorawan":
                ERRORS.append(f"Grafana dashboard lacks source-system query: {source_system}")
        if 'r["data_source"]' in query_text:
            ERRORS.append("Grafana dashboard uses obsolete data_source tag")
        if 'from(bucket: "' in query_text or "INFLUX_TOKEN" in query_text:
            ERRORS.append("Grafana dashboard contains a hard-coded bucket or token")
        if "v.defaultBucket" not in query_text:
            ERRORS.append("Grafana dashboard does not use the provisioned default bucket")

compose_path = ROOT / "deploy" / "grafana" / "compose.yaml"
if compose_path.is_file():
    compose_text = compose_path.read_text(encoding="utf-8")
    for required in (
        "grafana/grafana:13.1.4",
        "influxdb:2.9.1",
        "127.0.0.1",
        "INFLUX_GRAFANA_TOKEN",
        "GRAFANA_DASHBOARD_PATH",
        "GF_SECURITY_DISABLE_GRAVATAR",
        "GF_ANALYTICS_CHECK_FOR_PLUGIN_UPDATES",
        "GF_PLUGINS_PREINSTALL_DISABLED",
        "GF_PLUGINS_PLUGIN_ADMIN_ENABLED",
        "GF_PLUGINS_PUBLIC_KEY_RETRIEVAL_DISABLED",
        "healthcheck:",
        "no-new-privileges:true",
        'max-size: "10m"',
    ):
        if required not in compose_text:
            ERRORS.append(f"Grafana Compose file lacks required control: {required}")
    if "0.0.0.0" in compose_text:
        ERRORS.append("Grafana Compose file contains a non-loopback wildcard bind")

fixture_path = ROOT / "tests" / "fixtures" / "telemetry.jsonl"
if fixture_path.is_file():
    try:
        fixture = [json.loads(line) for line in fixture_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    except json.JSONDecodeError as exc:
        ERRORS.append(f"invalid telemetry fixture: {exc}")
    else:
        types = {record.get("station_type") for record in fixture}
        if types != ALLOWED_STATION_TYPES:
            ERRORS.append(f"telemetry fixture source-type coverage is incomplete: {sorted(str(item) for item in types)}")
        if any("example_not_live" not in record.get("quality_flags", []) for record in fixture):
            ERRORS.append("telemetry fixture contains an unlabeled synthetic record")

run_check([sys.executable, "scripts/build_dashboard.py", "--check"], "dashboard generator check")
run_check([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py"], "telemetry/dashboard unit tests")

if ERRORS:
    print("VALIDATION FAILED")
    for error in ERRORS:
        print(f"- {error}")
    sys.exit(1)

print(
    "VALIDATION OK: "
    f"{len(STATIONS)} station records; "
    f"{len(list(ROOT.rglob('*.md')))} Markdown files; "
    "dashboard and telemetry checks passed"
)
