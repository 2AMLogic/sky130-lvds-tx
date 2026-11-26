"""Regression cases for the pre/post-isolation pairing (issue #179)."""

import json
from pathlib import Path
import tempfile
import unittest

from compare_isolation import main as compare_main
from summarize import read_json

HERE = Path(__file__).resolve().parent
BEFORE = HERE / "results/r2/fleet-attempt/report-1g.json.gz"
REPHASE_DIR = HERE / "results/r3-isolation/rephase-409ps"
NOMINAL = "tt/27C/1.80/3.30"


class PairingTests(unittest.TestCase):
    def run_compare(self, after_report, extra_args=(), before_report=BEFORE):
        with tempfile.TemporaryDirectory() as tmp:
            out_path = Path(tmp) / "out.json"
            argv = [str(before_report), str(after_report), str(out_path), *extra_args]
            compare_main(argv)
            return json.loads(out_path.read_text())

    def test_self_pair_reproduces_before_counts_with_zero_deltas(self):
        result = self.run_compare(BEFORE)
        before_receipt = read_json(HERE / "results/r2/fleet-attempt/batch-receipt-1g.json")
        self.assertEqual(result["pairing"]["request_sha256"], {
            "before": before_receipt["request_sha256"],
            "after": before_receipt["request_sha256"],
        })
        self.assertTrue(result["pairing"]["shared_request"])
        self.assertEqual(result["pairing"]["sample_phase_s"],
                         {"before": 3.6e-10, "after": 3.6e-10})
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

    def test_rephased_pairing_records_per_leg_request_sha256_and_phase(self):
        before_receipt = read_json(HERE / "results/r2/fleet-attempt/batch-receipt-1g.json")
        rephase_receipt = read_json(REPHASE_DIR / "batch-receipt-1g.json")
        result = self.run_compare(
            REPHASE_DIR / "report-1g.json.gz",
            extra_args=[
                "--request", str(REPHASE_DIR / "request-1g.json"),
                "--meta", str(REPHASE_DIR / "stim_meta_1g.json"),
                "--after-label", "after_409ps",
            ],
        )
        self.assertEqual(result["pairing"]["request_sha256"], {
            "before": before_receipt["request_sha256"],
            "after_409ps": rephase_receipt["request_sha256"],
        })
        self.assertFalse(result["pairing"]["shared_request"])
        self.assertEqual(result["pairing"]["sample_phase_s"],
                         {"before": 3.6e-10, "after_409ps": 4.09e-10})

    def test_synthetic_edge_and_height_changes_are_counted(self):
        report = read_json(BEFORE)
        corner = next(c for c in report["corners"] if c["temperature_c"] == 27
                      and c["process"] == "tt"
                      and c["supply_v"] == {"VVCCD": 1.8, "VVDDIO": 3.3})
        edge_seen = height_seen = width_seen = False
        for card in list(corner["measurements"]):
            if card["name"] == "seq.m_e5_pr133":
                # 500 ps keeps the recorded crossings in window but leaves the band.
                card["value"] = 5e-10
                edge_seen = True
            if card["name"] == "seq.m_eye_h_v":
                card["value"] += 0.01
                height_seen = True
            if card["name"] == "seq.m_eye_w_s":
                corner["measurements"].remove(card)
                width_seen = True
        self.assertTrue(edge_seen and height_seen and width_seen)
        with tempfile.TemporaryDirectory() as tmp:
            mutated = Path(tmp) / "mutated.json"
            mutated.write_text(json.dumps(report))
            result = self.run_compare(mutated)
        self.assertEqual(result["e5_edge_transitions"].get("pass->slow"), 1)
        self.assertEqual(result["e5_edge_summary"]["new_misses"], 1)
        cond = next(c for c in result["conditions"] if c["condition"] == NOMINAL)
        # Missing width leaves width_delta_s unreported without suppressing height_delta_v.
        self.assertIsNone(cond["width_delta_s"])
        self.assertAlmostEqual(cond["height_delta_v"], 0.01, places=12)
        self.assertEqual(result["e9_deltas"]["height_v"]["count"], 75)
        self.assertEqual(result["e9_deltas"]["width_s"]["count"], 74)

    def drop_card(self, name):
        # BEFORE with one card dropped at the nominal corner, derived cards kept.
        report = read_json(BEFORE)
        corner = next(c for c in report["corners"] if c["temperature_c"] == 27
                      and c["process"] == "tt"
                      and c["supply_v"] == {"VVCCD": 1.8, "VVDDIO": 3.3})
        cards = [m for m in corner["measurements"] if m["name"] == name]
        self.assertEqual(len(cards), 1)
        corner["measurements"].remove(cards[0])
        return report, corner

    def test_missing_height_sample_leaves_height_inconclusive_and_width_kept(self):
        report, corner = self.drop_card("seq.m_eh")
        # The derived eye card is present; only its supporting sample is gone.
        self.assertTrue(any(m["name"] == "seq.m_eye_h_v"
                            for m in corner["measurements"]))
        with tempfile.TemporaryDirectory() as tmp:
            mutated = Path(tmp) / "mutated.json"
            mutated.write_text(json.dumps(report))
            result = self.run_compare(mutated)
        cond = next(c for c in result["conditions"] if c["condition"] == NOMINAL)
        self.assertIsNone(cond["after"]["eye_height_v"])
        self.assertEqual(cond["after"]["eye_height_row"], "inconclusive")
        self.assertIsNone(cond["height_delta_v"])
        self.assertEqual(cond["after"]["e9_row"], "inconclusive")
        # Width keeps its grade and delta.
        self.assertEqual(cond["after"]["eye_width_row"], "pass")
        self.assertEqual(cond["width_delta_s"], 0.0)
        self.assertEqual(result["per_leg"]["after"]["E9_height"],
                         {"pass": 72, "fail": 2, "inconclusive": 1})
        self.assertEqual(result["e9_deltas"]["height_v"]["count"], 74)
        self.assertEqual(result["e9_deltas"]["width_s"]["count"], 75)

    def test_missing_crossing_phase_leaves_width_inconclusive_and_height_kept(self):
        report, corner = self.drop_card("seq.m_phase_first")
        # The derived eye card is present; only its supporting phase is gone.
        self.assertTrue(any(m["name"] == "seq.m_eye_w_s"
                            for m in corner["measurements"]))
        with tempfile.TemporaryDirectory() as tmp:
            mutated = Path(tmp) / "mutated.json"
            mutated.write_text(json.dumps(report))
            result = self.run_compare(mutated)
        cond = next(c for c in result["conditions"] if c["condition"] == NOMINAL)
        self.assertIsNone(cond["after"]["eye_width_s"])
        self.assertEqual(cond["after"]["eye_width_row"], "inconclusive")
        self.assertIsNone(cond["width_delta_s"])
        self.assertEqual(cond["after"]["e9_row"], "inconclusive")
        # Height keeps its grade and delta.
        self.assertEqual(cond["after"]["eye_height_row"], "pass")
        self.assertEqual(cond["height_delta_v"], 0.0)
        self.assertEqual(result["per_leg"]["after"]["E9_width"],
                         {"pass": 74, "inconclusive": 1})
        self.assertEqual(result["e9_deltas"]["height_v"]["count"], 75)
        self.assertEqual(result["e9_deltas"]["width_s"]["count"], 74)

    def test_renamed_step_grades_when_matched_and_fails_on_mismatch(self):
        req = read_json(HERE / "request-1g.json")
        req["analysis_steps"][0]["name"] = "tran_seq"
        rep = read_json(BEFORE)
        for corner in rep["corners"]:
            for s in corner["steps"]:
                s["name"] = "tran_seq"
            for m in corner["measurements"]:
                if m["name"].startswith("seq."):
                    m["name"] = "tran_seq." + m["name"][4:]
        with tempfile.TemporaryDirectory() as tmp:
            req_path = Path(tmp) / "req.json"
            rep_path = Path(tmp) / "rep.json"
            req_path.write_text(json.dumps(req))
            rep_path.write_text(json.dumps(rep))
            matched = self.run_compare(
                rep_path,
                extra_args=["--before-request", str(req_path), "--request", str(req_path)],
                before_report=rep_path,
            )
            self.assertEqual(matched["per_leg"]["after"]["E9_height"], {"pass": 73, "fail": 2})
            self.assertEqual(matched["per_leg"]["after"]["E9_width"], {"pass": 75})
            with self.assertRaises(ValueError):
                self.run_compare(BEFORE, extra_args=["--request", str(req_path)])

    def test_leg_with_a_missing_condition_is_rejected(self):
        report = read_json(BEFORE)
        report["corners"] = report["corners"][1:]
        with tempfile.TemporaryDirectory() as tmp:
            mutated = Path(tmp) / "mutated.json"
            mutated.write_text(json.dumps(report))
            with self.assertRaises(ValueError):
                self.run_compare(mutated)


if __name__ == "__main__":
    unittest.main()
