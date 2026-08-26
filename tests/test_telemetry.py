from __future__ import annotations

import importlib.util
import io
import json
import unittest
from contextlib import redirect_stderr
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


INGEST = load_module("ingest_telemetry", ROOT / "scripts" / "ingest_telemetry.py")


class TelemetryTests(unittest.TestCase):
    def fixture_records(self) -> list[dict]:
        return INGEST.load_records(ROOT / "tests" / "fixtures" / "telemetry.jsonl")

    def test_fixture_covers_all_dashboard_source_types(self) -> None:
        records = self.fixture_records()
        self.assertEqual(len(records), 5)
        self.assertEqual(
            {record["station_type"] for record in records},
            {"irrigation_head", "soil_profile", "met_sandbox", "external_hobo", "external_meter"},
        )
        lines = [INGEST.line_protocol(record)[0] for record in records]
        self.assertTrue(all("example_not_live" in line for line in lines))
        self.assertTrue(all("source_system=" in line for line in lines))

    def test_irrigation_record_encodes_command_not_position(self) -> None:
        line, is_example = INGEST.line_protocol(self.fixture_records()[0])
        self.assertTrue(is_example)
        self.assertIn("station_id=IH-01", line)
        self.assertIn("pulse_count=1042i", line)
        self.assertIn("flow_rate_gpm=8.0", line)
        self.assertIn('valve_command="open"', line)
        self.assertIn("valve_position_feedback_available=false", line)

    def test_measurement_numbers_have_stable_float_type(self) -> None:
        record = {
            "station_id": "IH-01",
            "station_type": "irrigation_head",
            "observed_at": "2026-08-01T18:00:00Z",
            "flow": {"flow_rate_gpm": 8},
            "quality_flags": ["example_not_live"],
        }
        line, _ = INGEST.line_protocol(record)
        self.assertIn("flow_rate_gpm=8.0", line)
        self.assertNotIn("flow_rate_gpm=8i", line)

    def test_station_type_mismatch_is_rejected(self) -> None:
        record = {
            "station_id": "IH-01",
            "station_type": "soil_profile",
            "observed_at": "2026-08-01T18:00:00Z",
            "quality_flags": ["example_not_live"],
        }
        with self.assertRaises(INGEST.RecordError):
            INGEST.line_protocol(record)

    def test_empty_record_is_rejected(self) -> None:
        record = {
            "station_id": "IH-01",
            "station_type": "irrigation_head",
            "observed_at": "2026-08-01T18:00:00Z",
            "quality_flags": [],
        }
        with self.assertRaises(INGEST.RecordError):
            INGEST.line_protocol(record)

    def test_unknown_field_is_rejected(self) -> None:
        record = {
            "station_id": "IH-01",
            "station_type": "irrigation_head",
            "observed_at": "2026-08-01T18:00:00Z",
            "flow": {"flowrate_gpm": 8.0},
            "quality_flags": ["example_not_live"],
        }
        with self.assertRaises(INGEST.RecordError):
            INGEST.line_protocol(record)

    def test_quality_flags_are_machine_readable(self) -> None:
        record = {
            "station_id": "IH-01",
            "station_type": "irrigation_head",
            "observed_at": "2026-08-01T18:00:00Z",
            "quality_flags": ["Not ready"],
        }
        with self.assertRaises(INGEST.RecordError):
            INGEST.line_protocol(record)

    def test_weatherlink_contract_retains_timestamps_and_source_values(self) -> None:
        line, is_example = INGEST.line_protocol(self.fixture_records()[2])
        self.assertTrue(is_example)
        self.assertIn("source_system=weatherlink", line)
        self.assertIn('received_at="2026-08-01T18:00:24Z"', line)
        self.assertIn("ingest_latency_s=4.0", line)
        self.assertIn("rainfall_daily_mm=1.0", line)
        self.assertIn("solar_radiation_wm2=522.0", line)
        self.assertIn("source_rain_size_code=1i", line)
        self.assertIn("source_rainfall_daily_counts=10i", line)

    def test_weatherlink_timestamp_semantics_flag_is_required(self) -> None:
        record = dict(self.fixture_records()[2])
        record["quality_flags"] = ["example_not_live"]
        with self.assertRaises(INGEST.RecordError):
            INGEST.line_protocol(record)

    def test_met_model_gate_rejects_engineering_value(self) -> None:
        record = dict(self.fixture_records()[2])
        record["quality_flags"] = [
            "example_not_live",
            "model_unverified",
            "source_timestamp_not_sample_time",
        ]
        with self.assertRaises(INGEST.RecordError):
            INGEST.line_protocol(record)

    def test_source_alias_conflict_is_rejected(self) -> None:
        record = {
            "station_id": "HOBO-EXAMPLE-01",
            "station_type": "external_hobo",
            "source_system": "hobo_mx",
            "data_source": "signalizer",
            "observed_at": "2026-08-01T18:00:00Z",
            "quality_flags": ["example_not_live"],
        }
        with self.assertRaises(INGEST.RecordError):
            INGEST.line_protocol(record)

    def test_external_source_mismatch_is_rejected(self) -> None:
        record = {
            "station_id": "HOBO-EXAMPLE-01",
            "station_type": "external_hobo",
            "source_system": "signalizer",
            "observed_at": "2026-08-01T18:00:00Z",
            "quality_flags": ["example_not_live"],
        }
        with self.assertRaises(INGEST.RecordError):
            INGEST.line_protocol(record)

    def test_signalizer_alarm_requires_boolean(self) -> None:
        record = dict(self.fixture_records()[4])
        record["meter_alarm"] = 0
        with self.assertRaises(INGEST.RecordError):
            INGEST.line_protocol(record)

    def test_fixture_shift_moves_latest_record_into_default_window(self) -> None:
        records = self.fixture_records()
        now = datetime(2026, 8, 24, 22, 0, tzinfo=timezone.utc)
        shifted = INGEST.shift_example_records(records, now)
        newest = max(INGEST.parse_datetime(record["observed_at"]) for record in shifted)
        self.assertEqual(newest, now - timedelta(minutes=1))
        original_spacing = (
            INGEST.parse_datetime(records[-1]["observed_at"])
            - INGEST.parse_datetime(records[0]["observed_at"])
        )
        shifted_spacing = (
            INGEST.parse_datetime(shifted[-1]["observed_at"])
            - INGEST.parse_datetime(shifted[0]["observed_at"])
        )
        self.assertEqual(shifted_spacing, original_spacing)
        self.assertEqual(
            INGEST.parse_datetime(shifted[2]["received_at"])
            - INGEST.parse_datetime(shifted[2]["observed_at"]),
            timedelta(seconds=4),
        )

    def test_fixture_shift_rejects_unlabeled_data(self) -> None:
        records = self.fixture_records()
        records[0]["quality_flags"] = []
        with self.assertRaises(INGEST.RecordError):
            INGEST.shift_example_records(records)

    def test_test_bucket_detection_uses_token_boundaries(self) -> None:
        self.assertTrue(INGEST.is_test_bucket("fieldworks_test"))
        self.assertTrue(INGEST.is_test_bucket("fieldworks-test-sandbox"))
        self.assertFalse(INGEST.is_test_bucket("fieldworkstest"))
        self.assertFalse(INGEST.is_test_bucket("fieldworks"))

    def test_non_test_write_requires_production_confirmation(self) -> None:
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            result = INGEST.main(
                [
                    "--input",
                    str(ROOT / "tests" / "fixtures" / "telemetry.jsonl"),
                    "--write",
                    "--bucket",
                    "fieldworks",
                ]
            )
        self.assertEqual(result, 1)
        self.assertIn("--confirm-test-data", stderr.getvalue())

    def test_plain_http_write_endpoint_must_be_loopback(self) -> None:
        with self.assertRaises(INGEST.RecordError):
            INGEST.validate_endpoint("http://influx.example.invalid:8086")
        self.assertEqual(INGEST.validate_endpoint("http://127.0.0.1:8086").hostname, "127.0.0.1")

    def test_write_endpoint_rejects_embedded_credentials_and_query(self) -> None:
        credential_endpoint = "https://example-user" + ":example-password@" + "influx.example.invalid"
        with self.assertRaises(INGEST.RecordError):
            INGEST.validate_endpoint(credential_endpoint)
        with self.assertRaises(INGEST.RecordError):
            INGEST.validate_endpoint("https://influx.example.invalid?token=secret")

    def test_write_redirect_is_rejected_before_token_forwarding(self) -> None:
        with self.assertRaises(INGEST.RecordError):
            INGEST.RejectRedirects().redirect_request(
                None,
                None,
                307,
                "Temporary Redirect",
                {},
                "https://other.example.invalid/api/v2/write",
            )


class DashboardContractTests(unittest.TestCase):
    def dashboard(self) -> dict:
        path = ROOT / "deploy" / "grafana" / "dashboards" / "student-farm-sensors.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def test_dashboard_has_stable_identity_and_unique_panel_ids(self) -> None:
        dashboard = self.dashboard()
        self.assertEqual(dashboard["uid"], "student-farm-sensors")
        panel_ids = [panel["id"] for panel in dashboard["panels"]]
        self.assertEqual(len(panel_ids), len(set(panel_ids)))

    def test_dashboard_uses_source_system_contract(self) -> None:
        query_text = "\n".join(
            target.get("query", "")
            for panel in self.dashboard()["panels"]
            for target in panel.get("targets", [])
        )
        self.assertIn("source_system", query_text)
        self.assertNotIn('r["data_source"]', query_text)
        self.assertNotIn('from(bucket: "', query_text)
        self.assertIn("v.defaultBucket", query_text)

    def test_dashboard_covers_every_engineering_section(self) -> None:
        query_text = "\n".join(
            target.get("query", "")
            for panel in self.dashboard()["panels"]
            for target in panel.get("targets", [])
        )
        for field in (
            "flow_rate_gpm",
            "pressure_psi",
            "volume_total_gal",
            "valve_command",
            "tension_shallow_kpa",
            "tension_middle_kpa",
            "tension_deep_kpa",
            "soil_temp_c",
            "light_lux",
            "meter_alarm",
            "rainfall_daily_mm",
            "rain_rate_mm_hr",
            "solar_radiation_wm2",
            "uv_index",
        ):
            self.assertIn(field, query_text)

    def test_alarm_is_not_mixed_with_numeric_signalizer_fields(self) -> None:
        for panel in self.dashboard()["panels"]:
            query_text = "\n".join(target.get("query", "") for target in panel.get("targets", []))
            if "meter_alarm" in query_text:
                self.assertNotIn("flow_rate_gpm", query_text)
                self.assertNotIn("volume_total_gal", query_text)

    def test_timeseries_legends_use_compact_station_labels(self) -> None:
        for panel in self.dashboard()["panels"]:
            if panel.get("type") == "timeseries":
                self.assertEqual(
                    panel["fieldConfig"]["defaults"]["displayName"],
                    "${__field.labels.station_id} ${__field.name}",
                )


if __name__ == "__main__":
    unittest.main()
