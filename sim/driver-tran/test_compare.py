"""Regression cases for the pre/post-isolation pairing (issue #179)."""

import json
from pathlib import Path
import tempfile
import unittest

from compare_isolation import main as compare_main
from summarize import read_json

HERE = Path(__file__).resolve().parent
BEFORE = HERE / "results/r2/fleet-attempt/report-1g.json.gz"
NOMINAL = "tt/27C/1.80/3.30"


class PairingTests(unittest.TestCase):
    def run_compare(self, after_report):
        out = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        out.close()
        argv = [str(BEFORE), str(after_report), out.name]
        compare_main(argv)
        return json.loads(Path(out.name).read_text())

    def test_self_pair_reproduces_before_counts_with_zero_deltas(self):
        result = self.run_compare(BEFORE)
        before = result["per_leg"]["before"]
        self.assertEqual(before["E5_row"], {"fail": 75})
        self.assertEqual(before["E5_edges"], {"in band": 3331, "below 100 ps": 5180,
                                              "above 400 ps": 475, "unmeasurable": 614})
        self.assertEqual(before["E9_height"], {"pass": 73, "fail": 2})
        self.assertEqual(before["E9_width"], {"pass": 75})
        summary = result["e5_edge_summary"]
        self.assertEqual(summary["measured_in_both"], 8986)
        self.assertEqual(summary["new_misses"], 0)
        self.assertEqual(summary["delta_ps"]["min"], 0.0)
        self.assertEqual(result["e9_deltas"]["height_v"]["max"], 0.0)
        self.assertEqual(result["e9_deltas"]["width_s"]["max"], 0.0)

    def test_synthetic_edge_and_height_changes_are_counted(self):
        report = read_json(BEFORE)
        corner = next(c for c in report["corners"] if c["temperature_c"] == 27
                      and c["process"] == "tt"
                      and c["supply_v"] == {"VVCCD": 1.8, "VVDDIO": 3.3})
        edge_seen = height_seen = False
        for card in corner["measurements"]:
            if card["name"] == "seq.m_e5_pr133":
                # 500 ps keeps the recorded crossings in window but leaves the band.
                card["value"] = 5e-10
                edge_seen = True
            if card["name"] == "seq.m_eye_h_v":
                card["value"] += 0.01
                height_seen = True
        self.assertTrue(edge_seen and height_seen)
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as out:
            json.dump(report, out)
            mutated = out.name
        result = self.run_compare(mutated)
        self.assertEqual(result["e5_edge_transitions"].get("pass->slow"), 1)
        self.assertEqual(result["e5_edge_summary"]["new_misses"], 1)
        cond = next(c for c in result["conditions"] if c["condition"] == NOMINAL)
        self.assertAlmostEqual(cond["height_delta_v"], 0.01, places=12)

    def test_leg_with_a_missing_condition_is_rejected(self):
        report = read_json(BEFORE)
        report["corners"] = report["corners"][1:]
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as out:
            json.dump(report, out)
            mutated = out.name
        with self.assertRaises(ValueError):
            self.run_compare(mutated)


if __name__ == "__main__":
    unittest.main()
