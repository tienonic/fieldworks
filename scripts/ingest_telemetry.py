#!/usr/bin/env python3
"""Validate normalized station records and encode them for InfluxDB.

Dry-run output is the default. Writes require an API token. Synthetic records
can enter only a test bucket and require an explicit confirmation flag.
"""

from __future__ import annotations

import argparse
import copy
import ipaddress
import json
import math
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Iterable


STATION_ID = re.compile(r"^[A-Z0-9][A-Z0-9-]{2,39}$")
QUALITY_FLAG = re.compile(r"^[a-z0-9][a-z0-9_:-]*$")
CORE_STATIONS = {
    "IH-01": "irrigation_head",
    "IH-02": "irrigation_head",
    "SM-01": "soil_profile",
    "SM-02": "soil_profile",
    "SM-03": "soil_profile",
    "SM-04": "soil_profile",
    "MET-01": "met_sandbox",
}
EXPECTED_SOURCE = {
    "irrigation_head": "nodeflow_lorawan",
    "soil_profile": "nodeflow_lorawan",
    "met_sandbox": "weatherlink",
    "external_hobo": "hobo_mx",
    "external_meter": "signalizer",
}
MET_FIELDS = (
    "air_temp_c",
    "relative_humidity_pct",
    "wind_speed_ms",
    "wind_direction_deg",
    "rainfall_daily_mm",
    "rain_rate_mm_hr",
    "solar_radiation_wm2",
    "uv_index",
)
COMMON_INPUT_KEYS = {
    "station_id",
    "station_type",
    "source_system",
    "data_source",  # Accepted migration alias. Output uses source_system.
    "observed_at",
    "quality_flags",
    "firmware_version",
    "battery_v",
    "rssi_dbm",
    "snr_db",
}
TYPE_INPUT_KEYS = {
    "irrigation_head": {"flow", "pressure", "valve"},
    "soil_profile": {"soil_tension_kpa", "raw_v", "soil_temp_c", "depths_cm"},
    "met_sandbox": set(MET_FIELDS) | {"received_at", "source_values"},
    "external_hobo": {
        "air_temp_c",
        "relative_humidity_pct",
        "light_lux",
        "external_analog_raw_v",
    },
    "external_meter": {
        "flow_rate_gpm",
        "pulse_count",
        "volume_total_gal",
        "meter_alarm",
        "signalizer_current_ma",
        "logger_input_v",
    },
}


class RecordError(ValueError):
    """The input record does not satisfy the dashboard telemetry contract."""


class RejectRedirects(urllib.request.HTTPRedirectHandler):
    """Keep a write token on the operator-selected endpoint."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):  # type: ignore[no-untyped-def]
        raise RecordError("InfluxDB write endpoint redirects are not allowed")


def parse_datetime(value: Any, name: str = "observed_at") -> datetime:
    if not isinstance(value, str) or not value.strip():
        raise RecordError(f"{name} must be a non-empty ISO-8601 string")
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError as exc:
        raise RecordError(f"invalid {name}: {value}") from exc
    if parsed.tzinfo is None:
        raise RecordError(f"{name} must include a timezone")
    return parsed.astimezone(timezone.utc)


def timestamp_ns(value: Any, name: str = "observed_at") -> int:
    parsed = parse_datetime(value, name)
    seconds = int(parsed.timestamp())
    return seconds * 1_000_000_000 + parsed.microsecond * 1_000


def format_timestamp(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def require_number(name: str, value: Any) -> int | float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise RecordError(f"{name} must be numeric")
    if not math.isfinite(float(value)):
        raise RecordError(f"{name} must be finite")
    return value


def add_float(fields: dict[str, Any], name: str, value: Any) -> None:
    if value is not None:
        fields[name] = float(require_number(name, value))


def add_int(fields: dict[str, Any], name: str, value: Any) -> None:
    if value is None:
        return
    if isinstance(value, bool) or not isinstance(value, int):
        raise RecordError(f"{name} must be an integer")
    fields[name] = value


def add_string(fields: dict[str, Any], name: str, value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, str) or not value.strip():
        raise RecordError(f"{name} must be a non-empty string")
    fields[name] = value.strip()


def add_bool(fields: dict[str, Any], name: str, value: Any) -> None:
    if value is None:
        return
    if not isinstance(value, bool):
        raise RecordError(f"{name} must be Boolean")
    fields[name] = value


def nested_mapping(record: dict[str, Any], section: str, allowed: set[str]) -> dict[str, Any]:
    container = record.get(section)
    if container is None:
        return {}
    if not isinstance(container, dict):
        raise RecordError(f"{section} must be an object")
    unknown = sorted(set(container) - allowed)
    if unknown:
        raise RecordError(f"{section} contains unknown fields: {', '.join(unknown)}")
    return container


def validate_station_identity(station_id: str, station_type: str) -> None:
    expected = CORE_STATIONS.get(station_id)
    if expected and expected != station_type:
        raise RecordError(f"{station_id} requires station_type={expected}")
    if station_type == "irrigation_head" and station_id not in {"IH-01", "IH-02"}:
        raise RecordError("irrigation_head station_id must be IH-01 or IH-02")
    if station_type == "soil_profile" and station_id not in {"SM-01", "SM-02", "SM-03", "SM-04"}:
        raise RecordError("soil_profile station_id must be SM-01 through SM-04")
    if station_type == "met_sandbox" and station_id != "MET-01":
        raise RecordError("met_sandbox station_id must be MET-01")
    if station_type == "external_hobo" and not station_id.startswith("HOBO-"):
        raise RecordError("external_hobo station_id must use the HOBO- prefix")
    if station_type == "external_meter" and not station_id.startswith("IPERL-"):
        raise RecordError("external_meter station_id must use the IPERL- prefix")


def resolve_source(record: dict[str, Any], station_type: str) -> str:
    source_system = record.get("source_system")
    alias = record.get("data_source")
    if source_system is not None and alias is not None and source_system != alias:
        raise RecordError("source_system and data_source disagree")
    source_system = source_system if source_system is not None else alias
    expected = EXPECTED_SOURCE[station_type]
    if source_system is None and station_type in {"irrigation_head", "soil_profile"}:
        source_system = expected
    if not isinstance(source_system, str) or not source_system.strip():
        raise RecordError(f"{station_type} records require source_system={expected}")
    source_system = source_system.strip()
    if source_system != expected:
        raise RecordError(f"{station_type} records require source_system={expected}")
    return source_system


def normalize_quality_flags(value: Any) -> list[str]:
    if not isinstance(value, list):
        raise RecordError("quality_flags must be an array")
    normalized: list[str] = []
    for flag in value:
        if not isinstance(flag, str) or not QUALITY_FLAG.fullmatch(flag):
            raise RecordError("quality_flags must contain lowercase machine-readable names")
        normalized.append(flag)
    return sorted(set(normalized))


def normalize_record(record: dict[str, Any]) -> tuple[dict[str, str], dict[str, Any], int, bool]:
    if not isinstance(record, dict):
        raise RecordError("each record must be a JSON object")

    station_id = record.get("station_id")
    station_type = record.get("station_type")
    if not isinstance(station_id, str) or not STATION_ID.fullmatch(station_id):
        raise RecordError(f"invalid station_id: {station_id!r}")
    if station_type not in TYPE_INPUT_KEYS:
        raise RecordError(f"unsupported station_type: {station_type!r}")
    validate_station_identity(station_id, station_type)

    unknown = sorted(set(record) - COMMON_INPUT_KEYS - TYPE_INPUT_KEYS[station_type])
    if unknown:
        raise RecordError(f"record contains unknown fields: {', '.join(unknown)}")

    observed = parse_datetime(record.get("observed_at"))
    observed_ns = timestamp_ns(record.get("observed_at"))
    source_system = resolve_source(record, station_type)
    quality_flags = normalize_quality_flags(record.get("quality_flags"))
    is_example = "example_not_live" in quality_flags

    tags = {
        "station_id": station_id,
        "station_type": station_type,
        "source_system": source_system,
    }
    fields: dict[str, Any] = {
        "record_count": 1,
        "quality_flag_count": len(quality_flags),
        "quality_state": ",".join(quality_flags) if quality_flags else "ok",
    }
    baseline_field_count = len(fields)

    add_string(fields, "firmware_version", record.get("firmware_version"))
    add_float(fields, "battery_v", record.get("battery_v"))
    add_float(fields, "rssi_dbm", record.get("rssi_dbm"))
    add_float(fields, "snr_db", record.get("snr_db"))

    if station_type == "irrigation_head":
        flow = nested_mapping(record, "flow", {"pulse_count", "volume_total_gal", "flow_rate_gpm"})
        pressure = nested_mapping(record, "pressure", {"raw_v", "mpa", "psi"})
        valve = nested_mapping(record, "valve", {"command", "pulse_ms", "position_feedback_available"})
        add_int(fields, "pulse_count", flow.get("pulse_count"))
        add_float(fields, "volume_total_gal", flow.get("volume_total_gal"))
        add_float(fields, "flow_rate_gpm", flow.get("flow_rate_gpm"))
        add_float(fields, "pressure_raw_v", pressure.get("raw_v"))
        add_float(fields, "pressure_mpa", pressure.get("mpa"))
        add_float(fields, "pressure_psi", pressure.get("psi"))
        add_string(fields, "valve_command", valve.get("command"))
        add_int(fields, "valve_pulse_ms", valve.get("pulse_ms"))
        add_bool(fields, "valve_position_feedback_available", valve.get("position_feedback_available"))
        if fields.get("valve_command") not in {None, "open", "closed", "unknown"}:
            raise RecordError("valve.command must be open, closed, or unknown")

    elif station_type == "soil_profile":
        tension = nested_mapping(record, "soil_tension_kpa", {"shallow", "middle", "deep"})
        raw = nested_mapping(record, "raw_v", {"shallow", "middle", "deep", "temperature"})
        depths = nested_mapping(record, "depths_cm", {"shallow", "middle", "deep"})
        if any(value is not None for value in depths.values()):
            raise RecordError("depths_cm belongs in protected station metadata, not time-series records")
        add_float(fields, "tension_shallow_kpa", tension.get("shallow"))
        add_float(fields, "tension_middle_kpa", tension.get("middle"))
        add_float(fields, "tension_deep_kpa", tension.get("deep"))
        add_float(fields, "tension_shallow_raw_v", raw.get("shallow"))
        add_float(fields, "tension_middle_raw_v", raw.get("middle"))
        add_float(fields, "tension_deep_raw_v", raw.get("deep"))
        add_float(fields, "soil_temp_raw_v", raw.get("temperature"))
        add_float(fields, "soil_temp_c", record.get("soil_temp_c"))

    elif station_type == "met_sandbox":
        if "source_timestamp_not_sample_time" not in quality_flags:
            raise RecordError("WeatherLink records require source_timestamp_not_sample_time")
        received_text = record.get("received_at")
        received = parse_datetime(received_text, "received_at")
        if received < observed:
            raise RecordError("received_at cannot precede observed_at")
        add_string(fields, "received_at", format_timestamp(received))
        add_float(fields, "ingest_latency_s", (received - observed).total_seconds())
        for name in MET_FIELDS:
            add_float(fields, name, record.get(name))
        source_values = nested_mapping(
            record,
            "source_values",
            {"temp_f", "wind_speed_mph", "rain_size", "rainfall_daily_counts", "rain_rate_counts_per_hr"},
        )
        add_float(fields, "source_temp_f", source_values.get("temp_f"))
        add_float(fields, "source_wind_speed_mph", source_values.get("wind_speed_mph"))
        add_int(fields, "source_rain_size_code", source_values.get("rain_size"))
        add_int(fields, "source_rainfall_daily_counts", source_values.get("rainfall_daily_counts"))
        add_int(fields, "source_rain_rate_counts_per_hr", source_values.get("rain_rate_counts_per_hr"))
        if "model_unverified" in quality_flags:
            gated = sorted(
                name
                for name in set(MET_FIELDS)
                | {
                    "source_temp_f",
                    "source_wind_speed_mph",
                    "source_rain_size_code",
                    "source_rainfall_daily_counts",
                    "source_rain_rate_counts_per_hr",
                }
                if name in fields
            )
            if gated:
                raise RecordError(
                    "MET-01 model_unverified records must keep engineering and source values null: "
                    + ", ".join(gated)
                )

    elif station_type == "external_hobo":
        for name in ("air_temp_c", "relative_humidity_pct", "light_lux", "external_analog_raw_v"):
            add_float(fields, name, record.get(name))

    else:
        add_float(fields, "flow_rate_gpm", record.get("flow_rate_gpm"))
        add_int(fields, "pulse_count", record.get("pulse_count"))
        add_float(fields, "volume_total_gal", record.get("volume_total_gal"))
        add_bool(fields, "meter_alarm", record.get("meter_alarm"))
        add_float(fields, "signalizer_current_ma", record.get("signalizer_current_ma"))
        add_float(fields, "logger_input_v", record.get("logger_input_v"))

    if len(fields) == baseline_field_count and not quality_flags:
        raise RecordError("record must include a measurement, health field, or quality flag")
    return tags, fields, observed_ns, is_example


def escape_measurement(value: str) -> str:
    return value.replace("\\", "\\\\").replace(" ", "\\ ").replace(",", "\\,")


def escape_tag(value: str) -> str:
    return escape_measurement(value).replace("=", "\\=")


def escape_field_key(value: str) -> str:
    return escape_tag(value)


def encode_field(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return f"{value}i"
    if isinstance(value, float):
        return repr(value)
    if isinstance(value, str):
        escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        return f'"{escaped}"'
    raise RecordError(f"cannot encode field type {type(value).__name__}")


def line_protocol(record: dict[str, Any]) -> tuple[str, bool]:
    tags, fields, observed_ns, is_example = normalize_record(record)
    tag_text = ",".join(f"{escape_tag(key)}={escape_tag(value)}" for key, value in sorted(tags.items()))
    field_text = ",".join(f"{escape_field_key(key)}={encode_field(value)}" for key, value in sorted(fields.items()))
    return f"{escape_measurement('station_metrics')},{tag_text} {field_text} {observed_ns}", is_example


def load_records(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        raise RecordError(f"input is empty: {path}")
    if text.startswith("["):
        payload = json.loads(text)
        if not isinstance(payload, list):
            raise RecordError("JSON array input must contain records")
        records = payload
    elif text.startswith("{") and "\n{" not in text:
        payload = json.loads(text)
        if not isinstance(payload, dict):
            raise RecordError("JSON object input must be one record")
        records = [payload]
    else:
        records = []
        for line_number, line in enumerate(text.splitlines(), 1):
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError as exc:
                raise RecordError(f"invalid JSONL at line {line_number}: {exc.msg}") from exc
            if not isinstance(payload, dict):
                raise RecordError(f"JSONL line {line_number} is not an object")
            records.append(payload)
    if not records:
        raise RecordError(f"input contains no records: {path}")
    return records


def shift_example_records(records: list[dict[str, Any]], now: datetime | None = None) -> list[dict[str, Any]]:
    shifted = copy.deepcopy(records)
    if any("example_not_live" not in record.get("quality_flags", []) for record in shifted):
        raise RecordError("--shift-examples-to-now requires every record to include example_not_live")
    observed = [parse_datetime(record.get("observed_at")) for record in shifted]
    anchor = now or datetime.now(timezone.utc)
    if anchor.tzinfo is None:
        raise RecordError("fixture shift anchor must include a timezone")
    delta = anchor.astimezone(timezone.utc) - timedelta(minutes=1) - max(observed)
    for record in shifted:
        record["observed_at"] = format_timestamp(parse_datetime(record["observed_at"]) + delta)
        if record.get("received_at") is not None:
            record["received_at"] = format_timestamp(parse_datetime(record["received_at"], "received_at") + delta)
    return shifted


def is_test_bucket(bucket: str) -> bool:
    return bool(re.search(r"(^|[-_])test($|[-_])", bucket.lower()))


def validate_endpoint(endpoint: str) -> urllib.parse.ParseResult:
    parsed = urllib.parse.urlparse(endpoint)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise RecordError("InfluxDB endpoint must be an HTTP or HTTPS URL")
    if parsed.username is not None or parsed.password is not None:
        raise RecordError("InfluxDB endpoint must not contain credentials")
    if parsed.query or parsed.fragment:
        raise RecordError("InfluxDB endpoint must not contain a query or fragment")
    try:
        host = parsed.hostname
    except ValueError as exc:
        raise RecordError("InfluxDB endpoint has an invalid host") from exc
    if not host:
        raise RecordError("InfluxDB endpoint must include a host")
    if parsed.scheme == "http":
        try:
            loopback = ipaddress.ip_address(host).is_loopback
        except ValueError:
            loopback = host.lower() == "localhost"
        if not loopback:
            raise RecordError("plain HTTP is allowed only for a loopback InfluxDB endpoint")
    return parsed


def write_lines(endpoint: str, org: str, bucket: str, token: str, lines: Iterable[str]) -> int:
    validate_endpoint(endpoint)
    query = urllib.parse.urlencode({"org": org, "bucket": bucket, "precision": "ns"})
    url = f"{endpoint.rstrip('/')}/api/v2/write?{query}"
    body = ("\n".join(lines) + "\n").encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": "text/plain; charset=utf-8",
            "Accept": "application/json",
        },
    )
    opener = urllib.request.build_opener(RejectRedirects())
    with opener.open(request, timeout=30) as response:
        return response.status


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="JSON object, JSON array, or JSONL file")
    parser.add_argument("--write", action="store_true", help="Write validated line protocol to InfluxDB")
    parser.add_argument("--confirm-test-data", action="store_true", help="Required when writing example_not_live records")
    parser.add_argument("--confirm-production", action="store_true", help="Required when writing to a non-test bucket")
    parser.add_argument(
        "--shift-examples-to-now",
        action="store_true",
        help="Shift example timestamps so the newest record is one minute old",
    )
    parser.add_argument("--endpoint", default=os.environ.get("INFLUX_URL", "http://127.0.0.1:8086"))
    parser.add_argument("--org", default=os.environ.get("INFLUX_ORG", "fieldworks"))
    parser.add_argument("--bucket", default=os.environ.get("INFLUX_BUCKET", "fieldworks_test"))
    parser.add_argument("--token-env", default="INFLUX_TOKEN", help="Environment variable containing the API token")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        records = load_records(args.input)
        if args.shift_examples_to_now:
            records = shift_example_records(records)
        encoded = [line_protocol(record) for record in records]
        lines = [line for line, _ in encoded]
        has_example = any(is_example for _, is_example in encoded)
        if not args.write:
            sys.stdout.write("\n".join(lines) + "\n")
            print(f"DRY RUN: {len(lines)} validated record(s); no data written", file=sys.stderr)
            return 0

        test_bucket = is_test_bucket(args.bucket)
        if has_example and (not args.confirm_test_data or not test_bucket):
            raise RecordError("example_not_live records require --confirm-test-data and a test bucket")
        if not test_bucket and not args.confirm_production:
            raise RecordError("non-test writes require --confirm-production")
        token = os.environ.get(args.token_env)
        if not token:
            raise RecordError(f"missing InfluxDB token in environment variable {args.token_env}")
        status = write_lines(args.endpoint, args.org, args.bucket, token, lines)
        print(f"WROTE {len(lines)} record(s) to bucket {args.bucket}; HTTP {status}")
        return 0
    except urllib.error.HTTPError as exc:
        print(f"ERROR: InfluxDB returned HTTP {exc.code} {exc.reason}", file=sys.stderr)
        return 1
    except (OSError, json.JSONDecodeError, RecordError, urllib.error.URLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
