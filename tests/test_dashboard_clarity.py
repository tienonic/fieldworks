from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_PATH = ROOT / "deploy" / "grafana" / "dashboards" / "student-farm-sensors.json"
REPOSITORY_URL = "https://github.com/tienonic/fieldworks"
NO_DATA_TEXT = "No accepted records in selected window"
SERIES_DISPLAY_NAME = "${__field.labels.station_id} ${__field.name}"


class DashboardClarityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.dashboard = json.loads(DASHBOARD_PATH.read_text(encoding="utf-8"))

    def test_dashboard_keeps_33_panels_and_stable_identity(self) -> None:
        self.assertEqual(self.dashboard["uid"], "student-farm-sensors")
        self.assertEqual(len(self.dashboard["panels"]), 33)
        panel_ids = [panel["id"] for panel in self.dashboard["panels"]]
        self.assertEqual(len(panel_ids), len(set(panel_ids)))

    def test_read_first_panel_is_short_and_explicit(self) -> None:
        panel = self.dashboard["panels"][0]
        content = panel["options"]["content"]

        self.assertEqual(panel["title"], "Read first")
        self.assertEqual(panel["gridPos"]["h"], 5)
        self.assertEqual(len(content.split("\n\n")), 3)
        self.assertLessEqual(len(content.split()), 70)
        for required in (
            "not evidence of field deployment",
            "`example_not_live`",
            "not field observations",
            "Quality state",
            "[Repository record](" + REPOSITORY_URL + ")",
        ):
            self.assertIn(required, content)

    def test_data_panels_have_clear_no_data_text_and_series_labels(self) -> None:
        data_panels = [
            panel
            for panel in self.dashboard["panels"]
            if panel["type"] in {"stat", "table", "timeseries", "state-timeline"}
        ]
        self.assertEqual(len(data_panels), 27)
        for panel in data_panels:
            self.assertEqual(panel["fieldConfig"]["defaults"]["noValue"], NO_DATA_TEXT)
        for panel in data_panels:
            if panel["type"] == "timeseries":
                self.assertEqual(
                    panel["fieldConfig"]["defaults"]["displayName"],
                    SERIES_DISPLAY_NAME,
                )

    def test_quality_table_prioritizes_flags_and_keeps_query_contract(self) -> None:
        quality = next(panel for panel in self.dashboard["panels"] if panel["title"] == "Quality state")
        self.assertEqual(quality["gridPos"]["h"], 10)
        overrides = {
            override["matcher"]["options"]: {
                prop["id"]: prop["value"]
                for prop in override["properties"]
                if "value" in prop
            }
            for override in quality["fieldConfig"]["overrides"]
        }
        self.assertEqual(overrides["_time"]["displayName"], "Observed")
        self.assertEqual(overrides["_value"]["displayName"], "Quality flags")
        self.assertEqual(overrides["station_id"]["displayName"], "Station")
        self.assertTrue(overrides["station_type"]["custom.hidden"])
        self.assertTrue(overrides["source_system"]["custom.hidden"])

        query_text = "\n".join(
            target.get("query", "")
            for panel in self.dashboard["panels"]
            for target in panel.get("targets", [])
        )
        self.assertIn('r["station_id"] =~ /^${station_id:regex}$/', query_text)
        for source_system in ("nodeflow_lorawan", "weatherlink", "hobo_mx", "signalizer"):
            self.assertIn(f'r["source_system"] == "{source_system}"', query_text)
        self.assertNotIn('r["data_source"]', query_text)


if __name__ == "__main__":
    unittest.main()
