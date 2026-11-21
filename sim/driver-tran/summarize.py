#!/usr/bin/env python3
"""Grade a klt sim report against the cards requested for each corner and step.

Usage: summarize.py REPORT[.gz] STIM_META RATE_LABEL OUTPUT
Use 1g, 400m or 400m-control. The request sits beside the stimulus metadata.
"""

from collections import Counter
import gzip
import json
import math
from pathlib import Path
import re
import sys

NOMINAL = ("tt", 27, 1.8, 3.3)
EDGE = re.compile(r"m_e5_([pn])([rf])(\d+)")


def read_json(path):
    opener = gzip.open if str(path).endswith(".gz") else open
    with opener(path, "rt") as stream:
        return json.load(stream)


def corner_key(c):
    return (c["process"], c["temperature_c"], c["supply_v"]["VVCCD"],
            c["supply_v"]["VVDDIO"])


def fmt_c(k):
    return f"{k[0]}/{k[1]}C/{k[2]:.2f}/{k[3]:.2f}"


def measure_value(card):
    if card.get("status") in ("pass", "fail"):
        value = card.get("value")
        if isinstance(value, (int, float)) and math.isfinite(value):
            return value
    return None


def verdict(counts):
    if counts["fail"]:
        return "fail"
    return "missing" if counts["missing"] or not counts["pass"] else "pass"


def compare(value, limit, side):
    margin = None
    if value is not None:
        margin = value - limit if side == "min" else limit - value
    return {"value": value, "limit": limit, "margin": margin,
            "status": "missing" if margin is None else
                      "pass" if margin >= 0 else "fail"}


def record_binding(binding, key, result, condition, name, unit):
    margin = result["margin"]
    if margin is not None and (key not in binding or margin < binding[key]["margin"]):
        binding[key] = {**result, "condition": condition, "measurement": name,
                        "unit": unit}


def pad_duration(name, values, ui):
    _, direction, bit_label = EDGE.fullmatch(name).groups()
    bit = int(bit_label)
    start, end = values[name+"_start"], values[name+"_end"]
    t20, t80 = values[name+"_t20"], values[name+"_t80"]
    if None in (start, end, t20, t80):
        return None
    if (direction == "r" and end <= start) or (direction == "f" and end >= start):
        return None
    if (bit+1)*ui <= t20 < t80 <= (bit+2)*ui:
        return values[name]
    return None


def grade_step(corner, step, key, meta, binding):
    prefix = step["name"] + "."
    expected = [m for m in step["measurements"] if not m.get("intermediate")]
    ran = any(s["name"] == step["name"] and s["status"] == "ok"
              for s in corner.get("steps", []))
    returned = {m["name"]: m for m in corner.get("measurements", [])} if ran else {}
    values = {m["name"]: measure_value(returned.get(prefix + m["name"], {}))
              for m in expected}
    missing = [name for name, value in values.items() if value is None]
    condition = fmt_c(key)
    ui = meta["ui_s"]
    counts = {row: Counter({"pass": 0, "fail": 0, "missing": 0})
              for row in ("E5", "E9", "E4")}
    metrics = {}
    edges = {}
    bits = Counter()
    zeroes = [f"m_z{i}" for i in meta["crossings"]]
    for m in expected:
        name = m["name"]
        value = values[name]
        if name.startswith("m_bit"):
            bit = meta["bits"][int(name[5:])]
            bits["missing" if value is None else
                 "ok" if (value > 0 if bit else value < 0) else "bad"] += 1
        row = m.get("spec_row")
        if row not in counts:
            continue
        if row == "E5":
            value = pad_duration(name, values, ui)
        elif name == "m_eye_h_v" and None in (values["m_eh"], values["m_el"]):
            value = None
        elif name == "m_eye_w_s" and any(values[n] is None for n in
                                         ["m_phase_first", "m_phase_last", *zeroes]):
            value = None
        statuses = []
        for side, limit in m["limits"].items():
            result = compare(value, limit, side)
            statuses.append(result["status"])
            metric = {"m_eye_w_s": "E9.width", "m_eye_h_v": "E9.height"}.get(name, row)
            record_binding(binding, f"{prefix}{metric}.{side}", result,
                           condition, name, m["unit"])
            if row != "E5":
                metrics[metric] = {**result, "unit": m["unit"]}
        status = "missing" if value is None else "fail" if "fail" in statuses else "pass"
        counts[row][status] += 1
        if row == "E5":
            edges[name] = ("fast" if status == "fail" and value < m["limits"]["min"]
                           else "slow" if status == "fail" else status)

    power = values["m_pw_analog_mw"]
    limits = meta["limits"]
    power_checks = {}
    for leg, limit in (("any", limits["w1_any_max"]),
                       ("nominal", limits["w1_nom_max"] if key == NOMINAL else None)):
        if limit is not None:
            result = compare(power, limit, "max")
            power_checks[leg] = result
            record_binding(binding, f"{prefix}W1.subtotal.{leg}.max", result,
                           condition, "m_pw_analog_mw", "mW")

    rows = {row: verdict(count) for row, count in counts.items()}
    rows["W1"] = "unverified"
    return {
        "condition": condition, "step": step["name"], "rows": rows,
        "measurement_counts": counts, "e5_edges": dict(Counter(edges.values())),
        "e5_unmeasurable": [n for n, st in edges.items() if st == "missing"],
        "metrics": metrics, "crossing_phase_ui": [values["m_phase_first"], values["m_phase_last"]],
        "analog_subtotal_mw": power, "subtotal_comparisons_mw": power_checks,
        "bit_order": bits, "missing_measurements": missing,
    }, edges


def summarize(report, request, meta, rate):
    corners = request["corners"]
    rails = list(zip(corners["supply_v"]["VVCCD"], corners["supply_v"]["VVDDIO"], strict=True))
    grid = [(p, t, *pair) for p in corners["process"] for t in corners["temperature_c"]
            for pair in rails]
    by_key = {corner_key(c): c for c in report["corners"]}
    if len(by_key) != len(report["corners"]) or set(by_key).difference(grid):
        raise ValueError("duplicate or unexpected condition in report")
    binding = {}
    conditions = []
    step_totals = {}
    control = []
    steps = request["analysis_steps"]
    for key in grid:
        corner = by_key.get(key, {})
        edge_results = {}
        for step in steps:
            entry, edges = grade_step(corner, step, key, meta, binding)
            conditions.append(entry)
            step_name = step["name"]
            edge_results[step_name] = edges
            totals = step_totals.setdefault(step_name, {
                "rows": {}, "measurements": {}, "e5_edges": Counter(), "bit_order": Counter(),
            })
            for row, status in entry["rows"].items():
                totals["rows"].setdefault(row, Counter())[status] += 1
            for row, counts in entry["measurement_counts"].items():
                totals["measurements"].setdefault(row, Counter()).update(counts)
            totals["e5_edges"].update(entry["e5_edges"])
            totals["bit_order"].update(entry["bit_order"])
        if "ref" in edge_results:
            # The reference may have independent fast, slow or missing edges.
            # Only a same-pad, same-bit pass -> slow pair demonstrates detection.
            paired = [n for n, status in edge_results["ref"].items()
                      if status == "pass" and edge_results["ctl"][n] == "slow"]
            control.append({"condition": fmt_c(key), "ref_pass_ctl_slow": paired,
                            "detected_on_both_pads": {EDGE.fullmatch(n)[1] for n in paired}
                            == {"p", "n"}})
    summary = {
        "bench": "sim/driver-tran", "rate": rate, "simulated": True,
        "spec_status": "PROPOSED", "closes_no_spec_row": True,
        "backend": report["environment"]["backend"]["resolved"],
        "ui_s": meta["ui_s"], "window_bits": meta["window_bits"],
        "sample_phase_s": meta["sample_phase_s"],
        "grid": {"expected_conditions": len(grid), "distinct_tuples": len(by_key),
                 "missing": [fmt_c(k) for k in grid if k not in by_key], "rail_pairs": rails},
        "steps": step_totals, "binding_corners": binding,
        "w1_total": {"status": "unverified", "missing_contribution": "serializer share "
                     "at matching rate, activity and core corner"}, "conditions": conditions,
    }
    if control:
        summary["negative_control"] = control
    return summary


def main():
    report_path, meta_path, rate, out_path = sys.argv[1:]
    request_label = "control" if rate.endswith("-control") else rate
    request = read_json(Path(meta_path).with_name(f"request-{request_label}.json"))
    summary = summarize(read_json(report_path), request, read_json(meta_path), rate)
    Path(out_path).write_text(json.dumps(summary, indent=1, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
