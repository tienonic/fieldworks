import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('dashboard_display', ROOT / 'scripts/build_dashboard.py')
BUILDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BUILDER)

class DashboardDisplayTests(unittest.TestCase):
    def test_quality_hides_only_redundant_columns_at_display_time(self):
        panel = next(p for p in BUILDER.build_dashboard()['panels'] if p['title'] == 'Quality state')
        options = panel['transformations'][0]['options']
        self.assertEqual(options['excludeByName'], {'station_type': True, 'source_system': True})
        self.assertEqual(options['indexByName'], {'station_id': 0, '_time': 1, '_value': 2})
        self.assertIn('"source_system"', panel['targets'][0]['query'])
        self.assertTrue(panel['fieldConfig']['defaults']['custom']['wrapText'])

    def test_data_panels_do_not_overlap_and_last_seen_fits_rows(self):
        panels = [p for p in BUILDER.build_dashboard()['panels'] if p['type'] not in ('row', 'text')]
        self.assertGreaterEqual(next(p for p in panels if p['title'] == 'Last seen')['gridPos']['h'], 8)
        for i, p in enumerate(panels):
            a = p['gridPos']
            for q in panels[i + 1:]:
                b = q['gridPos']
                overlaps = (a['x'] < b['x'] + b['w'] and b['x'] < a['x'] + a['w']
                            and a['y'] < b['y'] + b['h'] and b['y'] < a['y'] + a['h'])
                self.assertFalse(overlaps, (p['title'], q['title']))

if __name__ == '__main__':
    unittest.main()
