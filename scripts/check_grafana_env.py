#!/usr/bin/env python3
"""Validate Grafana and InfluxDB environment configuration without printing secrets."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


REQUIRED = {
    "INFLUX_ADMIN_USER",
    "INFLUX_ADMIN_PASSWORD",
    "INFLUX_ADMIN_TOKEN",
    "INFLUX_GRAFANA_TOKEN",
    "INFLUX_ORG",
    "INFLUX_BUCKET",
    "INFLUX_RETENTION",
    "GRAFANA_ADMIN_USER",
    "GRAFANA_ADMIN_PASSWORD",
    "GRAFANA_BIND_ADDRESS",
    "GRAFANA_PORT",
    "INFLUX_BIND_ADDRESS",
    "INFLUX_PORT",
}
PLACEHOLDER = "change-before-starting"
TEST_BUCKET = re.compile(r"(^|[-_])test($|[-_])", re.IGNORECASE)


class EnvError(ValueError):
    """The environment file is incomplete or unsafe."""


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise EnvError(f"line {line_number} is not KEY=VALUE")
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if key in values:
            raise EnvError(f"duplicate key: {key}")
        if not re.fullmatch(r"[A-Z][A-Z0-9_]*", key):
            raise EnvError(f"invalid key at line {line_number}")
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[key] = value
    return values


def validate_env(values: dict[str, str], *, allow_production_bucket: bool = False) -> None:
    missing = sorted(REQUIRED - set(values))
    if missing:
        raise EnvError("missing required keys: " + ", ".join(missing))
    unsafe = sorted(key for key in REQUIRED if not values[key] or PLACEHOLDER in values[key].lower())
    if unsafe:
        raise EnvError("unset or placeholder values: " + ", ".join(unsafe))
    for key in ("INFLUX_ADMIN_PASSWORD", "GRAFANA_ADMIN_PASSWORD"):
        if len(values[key]) < 16:
            raise EnvError(f"{key} must contain at least 16 characters")
    for key in ("INFLUX_ADMIN_TOKEN", "INFLUX_GRAFANA_TOKEN"):
        if len(values[key]) < 24:
            raise EnvError(f"{key} must contain at least 24 characters")
    if values["INFLUX_ADMIN_TOKEN"] == values["INFLUX_GRAFANA_TOKEN"]:
        raise EnvError("INFLUX_ADMIN_TOKEN and INFLUX_GRAFANA_TOKEN must differ")
    for key in ("GRAFANA_BIND_ADDRESS", "INFLUX_BIND_ADDRESS"):
        if values[key] != "127.0.0.1":
            raise EnvError(f"{key} must remain on IPv4 loopback 127.0.0.1")
    for key in ("GRAFANA_PORT", "INFLUX_PORT"):
        try:
            port = int(values[key])
        except ValueError as exc:
            raise EnvError(f"{key} must be an integer") from exc
        if not 1 <= port <= 65535:
            raise EnvError(f"{key} must be between 1 and 65535")
    if values["GRAFANA_PORT"] == values["INFLUX_PORT"]:
        raise EnvError("Grafana and InfluxDB ports must differ")
    if not allow_production_bucket and not TEST_BUCKET.search(values["INFLUX_BUCKET"]):
        raise EnvError("local startup requires a test bucket unless --allow-production-bucket is explicit")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--env-file", required=True, type=Path)
    parser.add_argument("--allow-production-bucket", action="store_true")
    args = parser.parse_args(argv)
    try:
        values = parse_env(args.env_file)
        validate_env(values, allow_production_bucket=args.allow_production_bucket)
    except (OSError, EnvError) as exc:
        print(f"ENV CHECK FAILED: {exc}", file=sys.stderr)
        return 1
    print(f"ENV CHECK OK: {len(REQUIRED)} required keys; secrets not displayed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
