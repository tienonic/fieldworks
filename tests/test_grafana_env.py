from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_grafana_env", ROOT / "scripts" / "check_grafana_env.py")
assert SPEC and SPEC.loader
ENV = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ENV)


def valid_values() -> dict[str, str]:
    return {
        "INFLUX_ADMIN_USER": "fieldworks-admin",
        "INFLUX_ADMIN_PASSWORD": "a-secure-password-value",
        "INFLUX_ADMIN_TOKEN": "admin-token-with-more-than-24-characters",
        "INFLUX_GRAFANA_TOKEN": "read-token-with-more-than-24-characters",
        "INFLUX_ORG": "fieldworks",
        "INFLUX_BUCKET": "fieldworks_test",
        "INFLUX_RETENTION": "90d",
        "GRAFANA_ADMIN_USER": "fieldworks-admin",
        "GRAFANA_ADMIN_PASSWORD": "another-secure-password",
        "GRAFANA_BIND_ADDRESS": "127.0.0.1",
        "GRAFANA_PORT": "3000",
        "INFLUX_BIND_ADDRESS": "127.0.0.1",
        "INFLUX_PORT": "8086",
    }


class GrafanaEnvTests(unittest.TestCase):
    def test_valid_test_environment_passes(self) -> None:
        ENV.validate_env(valid_values())

    def test_placeholder_is_rejected(self) -> None:
        values = valid_values()
        values["GRAFANA_ADMIN_PASSWORD"] = "change-before-starting-grafana-password"
        with self.assertRaises(ENV.EnvError):
            ENV.validate_env(values)

    def test_shared_operator_and_read_tokens_are_rejected(self) -> None:
        values = valid_values()
        values["INFLUX_GRAFANA_TOKEN"] = values["INFLUX_ADMIN_TOKEN"]
        with self.assertRaises(ENV.EnvError):
            ENV.validate_env(values)

    def test_non_loopback_bind_is_rejected(self) -> None:
        values = valid_values()
        values["GRAFANA_BIND_ADDRESS"] = "0.0.0.0"
        with self.assertRaises(ENV.EnvError):
            ENV.validate_env(values)

    def test_unbracketed_ipv6_loopback_is_rejected_for_compose_port_syntax(self) -> None:
        values = valid_values()
        values["GRAFANA_BIND_ADDRESS"] = "::1"
        with self.assertRaises(ENV.EnvError):
            ENV.validate_env(values)

    def test_production_bucket_requires_explicit_override(self) -> None:
        values = valid_values()
        values["INFLUX_BUCKET"] = "fieldworks"
        with self.assertRaises(ENV.EnvError):
            ENV.validate_env(values)
        ENV.validate_env(values, allow_production_bucket=True)


if __name__ == "__main__":
    unittest.main()
