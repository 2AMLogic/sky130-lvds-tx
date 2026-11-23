#!/usr/bin/env python3
"""Pair the pre- and post-isolation 1 Gb/s G75 grids (issue #179).

Joins the two legs on the full 75-tuple G75 key and recomputes, from the
per-condition values in the two reports, the E5/E9 counts, per-edge
categories, signed after-minus-before deltas, limiting corners and the
pre-existing-vs-new miss split that the issue's acceptance criteria ask
for. By default both legs share request-1g.json and stim_meta_1g.json so
only design/lvds_tx_analog.spice differs; a re-phased after leg passes its
own --request and --meta while --before-request/--before-meta stay on the
before leg's inputs.

Usage:
  compare_isolation.py BEFORE_REPORT AFTER_REPORT OUTPUT_JSON [OUTPUT_MD]

Reports are the graded summaries' underlying klt reports (.json.gz or
.json). The legs are labelled by directory: the before leg is the #168
fleet report under results/r2/fleet-attempt, the after leg is the
isolation-commit run under results/r3-isolation.
"""

from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path

from summarize import corner_key, fmt_c, measure_value, pad_duration, read_json

E5_CATS = ("pass", "fast", "slow", "missing")
CAT_LABEL = {"pass": "in band", "fast": "below 100 ps", "slow": "above 400 ps",
             "missing": "unmeasurable"}
PS = 1e-12


def load_report(path):
    report = read_json(path)
    by_key = {}
    for c in report["corners"]:
        k = corner_key(c)
        if k in by_key:
            raise ValueError(f"duplicate condition {fmt_c(k)} in {path}")
        by_key[k] = c
    return report, by_key


def leg_edges(corner, request, meta):
    """Per-edge {name: (category, duration_s)} exactly as summarize grades."""
    step = request["analysis_steps"][0]
    prefix = step["name"] + "."
    expected = [m for m in step["measurements"] if not m.get("intermediate")]
    ran = any(s["name"] == step["name"] and s["status"] == "ok"
              for s in corner.get("steps", []))
    returned = {m["name"]: m for m in corner.get("measurements", [])} if ran else {}
    values = {m["name"]: measure_value(returned.get(prefix + m["name"], {}))
              for m in expected}
    out = {}
    for m in expected:
        if m.get("spec_row") != "E5":
            continue
        value = pad_duration(m["name"], values, meta["ui_s"])
        limits = m["limits"]
        cat = ("missing" if value is None else "fast" if value < limits["min"]
               else "slow" if value > limits["max"] else "pass")
        out[m["name"]] = (cat, value)
    return out, values


def request_sha256(path):
    raw = dict(read_json(path))
    raw.pop("batch", None)
    canonical = json.dumps(raw, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(canonical).hexdigest()


def request_grid(req):
    grid = [(p, t, *pair)
            for p in req["corners"]["process"]
            for t in req["corners"]["temperature_c"]
            for pair in zip(req["corners"]["supply_v"]["VVCCD"],
                            req["corners"]["supply_v"]["VVDDIO"])]
    if len(grid) != 75 or len(set(grid)) != 75:
        raise ValueError("request grid is not the 75-tuple G75 set")
    return grid


def metric(corner, step_name, name):
    target = f"{step_name}.{name}"
    for m in corner.get("measurements", []):
        if m["name"] == target:
            return measure_value(m)
    return None


def row_status(value, lo, hi):
    if value is None:
        return "inconclusive"
    if value < lo:
        return "fail"
    if value > hi:
        return "fail"
    return "pass"


def eye_centre_ps(values):
    """Centre of the folded opening, in ps past the bit-launch edge."""
    first, last = values.get("m_phase_first"), values.get("m_phase_last")
    if first is None or last is None:
        return None
    ui_ps = meta_ui * 1e12
    return ((last + 1.0 + first) / 2.0 % 1.0) * ui_ps


meta_ui = None


def main(argv=None):
    global meta_ui
    ap = argparse.ArgumentParser()
    ap.add_argument("before_report")
    ap.add_argument("after_report")
    ap.add_argument("out_json")
    ap.add_argument("out_md", nargs="?")
    here = Path(__file__).resolve().parent
    ap.add_argument("--before-request", default=str(here / "request-1g.json"),
                    help="before-leg request (expected cards and canonical hash)")
    ap.add_argument("--request", default=str(here / "request-1g.json"),
                    help="after-leg request (expected cards and canonical hash); "
                         "pass the re-phased variant for a re-phased after leg")
    ap.add_argument("--before-meta", default=str(here / "stim_meta_1g.json"))
    ap.add_argument("--meta", default=str(here / "stim_meta_1g.json"))
    ap.add_argument("--before-desc",
                    default="results/r2/fleet-attempt/report-1g.json.gz "
                            "(#168 fleet run, netlist e27999f)")
    ap.add_argument("--after-desc",
                    default="results/r3-isolation/report-1g.json.gz "
                            "(isolation commit 45ebd2d3)")
    ap.add_argument("--after-label", default="after")
    args = ap.parse_args(argv)
    before_path, after_path = args.before_report, args.after_report
    out_json, out_md = args.out_json, args.out_md
    before_request = read_json(args.before_request)
    request = read_json(args.request)
    before_meta = read_json(args.before_meta)
    meta = read_json(args.meta)
    before_req_sha256 = request_sha256(args.before_request)
    after_req_sha256 = request_sha256(args.request)
    labels = ("before", args.after_label)
    if before_meta["ui_s"] != meta["ui_s"] or before_meta["limits"] != meta["limits"]:
        raise ValueError("before and after stimulus metadata UI/limits do not match")
    meta_ui = meta["ui_s"]
    limits = meta["limits"]
    h_lo = limits["e9_h_min"]
    w_lo = limits["e9_w_ui"] * meta_ui

    grid = request_grid(request)
    if request_grid(before_request) != grid:
        raise ValueError("before and after request grids do not match")
    leg_requests = {"before": before_request, labels[1]: request}
    leg_metas = {"before": before_meta, labels[1]: meta}

    legs = {}
    for label, path in (("before", before_path), (labels[1], after_path)):
        report, by_key = load_report(path)
        missing = [fmt_c(k) for k in grid if k not in by_key]
        extra = [fmt_c(k) for k in by_key if k not in set(grid)]
        if missing or extra:
            raise ValueError(f"{label} leg key mismatch: missing={missing} extra={extra}")
        legs[label] = {"report": report, "by_key": by_key}

    conditions = []
    edge_transitions = Counter()
    edge_deltas = []
    height_deltas, width_deltas = [], []
    nominal_key = ("tt", 27, 1.8, 3.3)
    per_leg = {label: {
        "E5_row": Counter(), "E5_edges": Counter(),
        "E9_height": Counter(), "E9_width": Counter(), "E9_row": Counter(),
        "height_values": [], "width_values": [], "failed_steps": 0,
    } for label in labels}

    for key in grid:
        cond = fmt_c(key)
        entry = {"condition": cond}
        for label in labels:
            corner = legs[label]["by_key"][key]
            leg_req = leg_requests[label]
            leg_meta = leg_metas[label]
            step_name = leg_req["analysis_steps"][0]["name"]
            steps = corner.get("steps", [])
            if steps and not any(s["name"] == step_name for s in steps):
                raise ValueError(
                    f"{label} leg {cond}: expected step {step_name!r}, "
                    f"got {[s['name'] for s in steps]}"
                )
            step_ok = any(s["name"] == step_name and s["status"] == "ok"
                          for s in steps)
            if not step_ok:
                per_leg[label]["failed_steps"] += 1
            edges, values = leg_edges(corner, leg_req, leg_meta)
            h = metric(corner, step_name, "m_eye_h_v") if step_ok else None
            w = metric(corner, step_name, "m_eye_w_s") if step_ok else None
            cats = Counter(cat for cat, _ in edges.values())
            for cat in E5_CATS:
                per_leg[label]["E5_edges"][cat] += cats[cat]
            e5_row = ("fail" if (cats["fast"] or cats["slow"])
                      else "inconclusive" if (cats["missing"] or not step_ok)
                      else "pass")
            h_row = row_status(h, h_lo, float("inf"))
            w_row = row_status(w, w_lo, float("inf"))
            e9_row = ("fail" if "fail" in (h_row, w_row)
                      else "inconclusive" if "inconclusive" in (h_row, w_row)
                      else "pass")
            per_leg[label]["E5_row"][e5_row] += 1
            per_leg[label]["E9_height"][h_row] += 1
            per_leg[label]["E9_width"][w_row] += 1
            per_leg[label]["E9_row"][e9_row] += 1
            if h is not None:
                per_leg[label]["height_values"].append((h, cond))
            if w is not None:
                per_leg[label]["width_values"].append((w, cond))
            entry[label] = {
                "step_ok": step_ok,
                "e5_edges": {cat: cats[cat] for cat in E5_CATS},
                "e5_row": e5_row,
                "eye_height_v": h, "eye_height_row": h_row,
                "eye_width_s": w, "eye_width_row": w_row,
                "e9_row": e9_row,
                "eye_centre_ps": eye_centre_ps(values),
                "power_mw": metric(corner, step_name, "m_pw_analog_mw") if step_ok else None,
            }
            entry[label + "_edges"] = edges
        b, a = entry["before"], entry[labels[1]]
        if set(entry["before_edges"]) != set(entry[labels[1] + "_edges"]):
            raise ValueError("before and after requests do not define the same E5 edges")
        for name in entry["before_edges"]:
            bc = entry["before_edges"][name][0]
            ac = entry[labels[1] + "_edges"][name][0]
            edge_transitions[f"{bc}->{ac}"] += 1
            dv = None
            bt = entry["before_edges"][name][1]
            at = entry[labels[1] + "_edges"][name][1]
            if bt is not None and at is not None:
                dv = (at - bt) / PS
                edge_deltas.append((dv, name, cond))
        entry["height_delta_v"] = (None if b["eye_height_v"] is None
                                   or a["eye_height_v"] is None
                                   else a["eye_height_v"] - b["eye_height_v"])
        entry["width_delta_s"] = (None if b["eye_width_s"] is None
                                  or a["eye_width_s"] is None
                                  else a["eye_width_s"] - b["eye_width_s"])
        if entry["height_delta_v"] is not None:
            height_deltas.append((entry["height_delta_v"], cond))
        if entry["width_delta_s"] is not None:
            width_deltas.append((entry["width_delta_s"], cond))
        for label in labels:
            entry.pop(label + "_edges")
        conditions.append(entry)

    def binding(values, worst="min"):
        finite = [v for v in values if v is not None]
        if not finite:
            return None
        return (min(finite) if worst == "min" else max(finite))

    new_edge_misses = sum(n for t, n in edge_transitions.items()
                          if t.startswith("pass->") and not t.endswith("pass"))
    recovered_edges = sum(n for t, n in edge_transitions.items()
                          if t.endswith("->pass") and not t.startswith("pass"))
    preexisting_edge_misses = sum(
        n for t, n in edge_transitions.items()
        if t.split("->")[0] in ("fast", "slow") and t.split("->")[1] in ("fast", "slow"))
    became_unmeasurable = sum(n for t, n in edge_transitions.items()
                              if t.split("->")[1] == "missing"
                              and t.split("->")[0] != "missing")
    newly_measurable = sum(n for t, n in edge_transitions.items()
                           if t.split("->")[0] == "missing" and t.split("->")[1] != "missing")

    def delta_stats(deltas):
        if not deltas:
            return None
        vals = sorted(d for d, *_ in deltas)
        n = len(vals)
        return {"count": n, "min": vals[0], "max": vals[-1],
                "median": vals[n // 2] if n % 2 else (vals[n // 2 - 1] + vals[n // 2]) / 2,
                "mean": sum(vals) / n}

    edge_delta_stats = delta_stats(edge_deltas)
    slower = sum(1 for d, _, _ in edge_deltas if d > 0)
    faster = sum(1 for d, _, _ in edge_deltas if d < 0)
    unchanged = sum(1 for d, _, _ in edge_deltas if d == 0)

    def extreme(deltas, pick):
        return pick(deltas, key=lambda d: d[0]) if deltas else None

    summary = {
        "bench": "sim/driver-tran", "rate": "1g", "simulated": True,
        "pairing": {
            "conditions": len(conditions),
            "legs": {
                "before": args.before_desc,
                labels[1]: args.after_desc,
            },
            "request_sha256": {
                "before": before_req_sha256,
                labels[1]: after_req_sha256,
            },
            "shared_request": before_req_sha256 == after_req_sha256,
            "sample_phase_s": {
                "before": before_meta["sample_phase_s"],
                labels[1]: meta["sample_phase_s"],
            },
        },
        "per_leg": {
            label: {
                "E5_row": dict(per_leg[label]["E5_row"]),
                "E5_edges": {CAT_LABEL[c]: per_leg[label]["E5_edges"][c] for c in E5_CATS},
                "E9_height": dict(per_leg[label]["E9_height"]),
                "E9_width": dict(per_leg[label]["E9_width"]),
                "E9_row": dict(per_leg[label]["E9_row"]),
                "failed_steps": per_leg[label]["failed_steps"],
                "min_eye_height_v": binding([v for v, _ in per_leg[label]["height_values"]]),
                "min_eye_height_corner": binding(
                    [(v, c) for v, c in per_leg[label]["height_values"]]
                )[1] if per_leg[label]["height_values"] else None,
                "min_eye_width_s": binding([v for v, _ in per_leg[label]["width_values"]]),
                "min_eye_width_corner": binding(
                    [(v, c) for v, c in per_leg[label]["width_values"]]
                )[1] if per_leg[label]["width_values"] else None,
            } for label in labels
        },
        "e5_edge_transitions": {t: n for t, n in sorted(edge_transitions.items())},
        "e5_edge_summary": {
            "new_misses": new_edge_misses,
            "recovered": recovered_edges,
            "preexisting_misses": preexisting_edge_misses,
            "became_unmeasurable": became_unmeasurable,
            "newly_measurable": newly_measurable,
            "measured_in_both": len(edge_deltas),
            "slower_after": slower, "faster_after": faster,
            "unchanged": unchanged,
            "delta_ps": edge_delta_stats,
            "largest_slowdown_ps": extreme(edge_deltas, max),
            "largest_speedup_ps": extreme(edge_deltas, min),
        },
        "e9_deltas": {
            "height_v": delta_stats(height_deltas),
            "width_s": delta_stats(width_deltas),
            "worst_height_loss_v": extreme(height_deltas, min),
            "worst_width_loss_s": extreme(width_deltas, min),
            "largest_height_gain_v": extreme(height_deltas, max),
            "largest_width_gain_s": extreme(width_deltas, max),
        },
        "nominal_eye_centre_ps": {
            label: next((c[label]["eye_centre_ps"] for c in conditions
                         if c["condition"] == fmt_c(nominal_key)), None)
            for label in labels
        },
        "conditions": conditions,
    }

    with open(out_json, "w") as f:
        json.dump(summary, f, indent=1)
        f.write("\n")

    if out_md:
        p = summary["per_leg"]
        lines = []
        for label in labels:
            lines.append(f"### {label} leg")
            lines.append("")
            lines.append(f"- E5 rows: {dict(p[label]['E5_row'])} of 75")
            lines.append(f"- E5 edges: {p[label]['E5_edges']}")
            lines.append(f"- E9 height: {dict(p[label]['E9_height'])} of 75; "
                         f"min {p[label]['min_eye_height_v']*1e3:.2f} mV at "
                         f"{p[label]['min_eye_height_corner']}")
            lines.append(f"- E9 width: {dict(p[label]['E9_width'])} of 75; "
                         f"min {p[label]['min_eye_width_s']*1e12:.1f} ps at "
                         f"{p[label]['min_eye_width_corner']}")
            lines.append("")
        e = summary["e5_edge_summary"]
        lines.append("### Edge transitions (before -> after)")
        lines.append("")
        lines.append(f"- new misses {e['new_misses']}, recovered {e['recovered']}, "
                     f"pre-existing {e['preexisting_misses']}, "
                     f"became unmeasurable {e['became_unmeasurable']}")
        d = e["delta_ps"]
        lines.append(f"- {e['measured_in_both']} edges measurable in both: "
                     f"{e['slower_after']} slower, {e['faster_after']} faster; "
                     f"median delta {d['median']:.1f} ps, "
                     f"range [{d['min']:.1f}, {d['max']:.1f}] ps" if d else "- no common edges")
        lines.append("")
        Path(out_md).write_text("\n".join(lines) + "\n")
        print("\n".join(lines))


if __name__ == "__main__":
    main()
