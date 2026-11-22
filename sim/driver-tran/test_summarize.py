"""Regression cases for missing measurements and bit-local E5 timestamps."""

from pathlib import Path
import unittest

from summarize import NOMINAL, grade_step, read_json, summarize

HERE = Path(__file__).resolve().parent


class GradingTests(unittest.TestCase):
    def setUp(self):
        self.request = read_json(HERE / "request-control.json")
        self.report = read_json(HERE / "results/r2/control/report.json.gz")
        self.meta = read_json(HERE / "stim_meta_400m.json")
        self.corner = self.report["corners"][0]

    def test_absent_height_prevents_eye_pass(self):
        # A failed height is the only E9 miss, just as at the weakest G75 corner.
        height = next(m for m in self.corner["measurements"] if m["name"] == "ref.m_eye_h_v")
        height.update(value=0.10, status="fail")
        step = self.request["analysis_steps"][0]
        before, _ = grade_step(self.corner, step, NOMINAL, self.meta, {})
        self.assertEqual(before["rows"]["E9"], "fail")
        self.corner["measurements"].remove(height)
        result = summarize(self.report, self.request, self.meta, "400m-control")
        ref, ctl = result["conditions"]
        self.assertEqual(ref["rows"]["E9"], "missing")
        self.assertEqual(ref["measurement_counts"]["E9"]["missing"], 1)
        self.assertIn("m_eye_h_v", ref["missing_measurements"])
        self.assertEqual(ctl["rows"]["E9"], "pass")
        self.assertNotIn("ref.E9.height.min", result["binding_corners"])

    def test_later_bits_crossings_cannot_pass_as_current_edge(self):
        edge = "m_e5_nr134"
        step = self.request["analysis_steps"][0]
        _, original = grade_step(self.corner, step, NOMINAL, self.meta, {})
        self.assertEqual(original[edge], "pass")
        for card in self.corner["measurements"]:
            if card["name"] in (f"ref.{edge}_t20", f"ref.{edge}_t80"):
                card["value"] += 2 * self.meta["ui_s"]
        ref, edges = grade_step(self.corner, step, NOMINAL, self.meta, {})
        self.assertEqual(edges[edge], "missing")
        self.assertIn(edge, ref["e5_unmeasurable"])

    def test_absent_step_keeps_its_own_expected_card_counts(self):
        self.corner["measurements"] = [m for m in self.corner["measurements"]
                                       if m["step"] == "ref"]
        result = summarize(self.report, self.request, self.meta, "400m-control")
        ctl = result["conditions"][1]
        self.assertEqual(ctl["measurement_counts"]["E5"]["missing"], 128)
        self.assertEqual(ctl["rows"]["E9"], "missing")
        self.assertFalse(result["negative_control"][0]["detected_on_both_pads"])


if __name__ == "__main__":
    unittest.main()
