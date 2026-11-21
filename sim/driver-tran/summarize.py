#!/usr/bin/env python3
"""Distil a driver-tran fleet report into a committed summary.

  python3 summarize.py <report.json> <stim_meta.json> <rate-label> <out.json>

Reads the klt sim report envelope, reconciles the grid against the 75
distinct G75 tuples, and emits per-row pass counts, binding corners, worst
margins, per-corner compact rows, and the bench self-checks (bit-order
observers vs the expected PRBS bits, latency, negative-control reconciliation
when the report carries ref/ctl steps). Records misses as misses; an errored
measurement is a missing measurement and never a pass.
"""

import json
import sys

NOMINAL = ("tt", 27, 1.8, 3.3)
G75_PAIRS = [(1.62, 2.97), (1.8, 3.3), (1.98, 3.63), (1.62, 3.63),
             (1.98, 2.97)]


def corner_key(c):
    sup = c.get("supply_v", {})
    return (c.get("process"), c.get("temperature_c"),
            sup.get("VVCCD"), sup.get("VVDDIO"))


def fmt_c(k):
    return (f"{k[0]}/{k[1]}C/{k[2]:.2f}/{k[3]:.2f}")


def main():
    report_path, meta_path, rate, out_path = sys.argv[1:5]
    d = json.load(open(report_path))
    meta = json.load(open(meta_path))
    bits = meta["bits"]
    ui = meta["ui_s"]
    row_map = meta.get("row_map", {})
    row_limits = {
        "E5": {"min": meta["limits"]["e5_min"],
               "max": meta["limits"]["e5_max"]},
        "E9": {"min": meta["limits"]["e9_h_min"]},
        "E4": {"max": 0.15},
        "W1": {"max": meta["limits"]["w1_any_max"]},
    }
    rows = ("E5", "E9", "E4", "W1")

    is_control = False
    steps = ["seq"]
    for c in d.get("corners", []):
        prefixes = {m["name"].split(".", 1)[0]
                    for m in c.get("measurements", []) if "." in m["name"]}
        if prefixes & {"ref", "ctl"}:
            is_control = True
            steps = sorted(prefixes)
        break

    res = {r: {"pass": 0, "fail": 0, "error": 0} for r in rows}
    binding = {}
    conditions = []
    tuples = set()
    rail_pairs = set()
    bit_checks = {"ok": 0, "bad": 0, "detail": []}
    for c in d.get("corners", []):
        k = corner_key(c)
        tuples.add(k)
        rail_pairs.add((k[2], k[3]))
        row_flag = {r: None for r in rows}
        rowval = {}
        cond = {"condition": fmt_c(k), "status": c.get("status")}
        for m in c.get("measurements", []):
            n = m["name"]
            base = n.split(".", 1)[1] if "." in n else n
            step = n.split(".", 1)[0] if "." in n else steps[0]
            sr = row_map.get(base)
            st = m.get("status")
            if sr in rows:
                if st == "pass":
                    res[sr]["pass"] += 1
                elif st == "fail":
                    res[sr]["fail"] += 1
                else:
                    res[sr]["error"] += 1
                if st == "pass" and row_flag[sr] in (None, "pass"):
                    row_flag[sr] = "pass"
                elif st == "error" and row_flag[sr] != "fail":
                    row_flag[sr] = "error"
                else:
                    row_flag[sr] = "fail"
                mg = m.get("margin")
                v = m.get("value")
                lim = row_limits.get(sr, {})
                # E5 binding: anomalous pairings (different physical features)
                # are classified, never "binding" -- the binding corner is
                # the worst in-class miss.
                if sr == "E5" and v is not None and (v <= 0 or v > 2 * ui):
                    continue
                if v is not None and lim:
                    span = None
                    if lim.get("min") is not None and lim.get("max") is not None:
                        span = lim["max"] - lim["min"]
                    elif lim.get("min") is not None:
                        span = lim["min"]
                    elif lim.get("max") is not None:
                        span = lim["max"]
                    if span:
                        frac = abs(mg) / abs(span)
                        cur = binding.get((step, sr))
                        if cur is None or frac > cur[0]:
                            binding[(step, sr)] = (
                                frac, fmt_c(k), base, v, mg, lim)
            if base.startswith("m_bit"):
                idx = int(base[5:])
                exp = bits[idx]
                got = m.get("value")
                if got is None:
                    continue
                ok = (got > 0) == (exp == 1)
                bit_checks["ok" if ok else "bad"] += 1
                if not ok:
                    bit_checks["detail"].append(
                        {"bit": idx, "expected": exp, "vd": got,
                         "condition": fmt_c(k)})
            if base in ("m_eye_h_v", "m_vos_pp", "m_pw_analog_mv", "m_xlat"):
                rowval[base] = m.get("value")
            if base.startswith("m_e5") and "t2" not in base and "t8" not in base:
                rowval.setdefault("e5", []).append(m.get("value"))
        cond["rows"] = row_flag
        cond["eye_h_v"] = rowval.get("m_eye_h_v")
        cond["vos_pp_v"] = rowval.get("m_vos_pp")
        cond["pw_analog_mv"] = rowval.get("m_pw_analog_mv")
        e5v = [v for v in rowval.get("e5", []) if v is not None]
        if e5v:
            cond["e5_ps"] = {
                "n": len(e5v),
                "min": min(e5v) * 1e12,
                "max": max(e5v) * 1e12,
            }
        conditions.append(cond)

    # W1 nominal leg: the tt/27C/1.80/3.30 row's analog subtotal against the
    # nominal-only limit (the envelope grades only the any-G75 cap).
    nom_row = next((c for c in conditions
                    if c["condition"] == fmt_c(NOMINAL)), None)
    w1_nom = None
    if nom_row and nom_row.get("pw_analog_mv") is not None:
        lim = meta["limits"]["w1_nom_max"]
        w1_nom = {"condition": fmt_c(NOMINAL),
                  "pw_analog_mv": nom_row["pw_analog_mv"],
                  "limit_mv": lim,
                  "verdict": "pass" if nom_row["pw_analog_mv"] <= lim
                  else "fail"}

    lat = meta.get("latency_observer") or {}
    # E5 edge classification: an edge time <= 0 or > 2*UI means the two
    # td-scoped WHEN cards caught different physical features (level
    # recrossings at a CMFB-corrupted corner) -- an anomalous pairing,
    # recorded as such and never counted as an in-band or out-of-band edge.
    e5_lo = meta["limits"]["e5_min"]
    e5_hi = meta["limits"]["e5_max"]
    e5_all = []
    for c in d.get("corners", []):
        for m in c.get("measurements", []):
            base = m["name"].split(".", 1)[-1]
            if base.startswith("m_e5") and "t2" not in base \
                    and "t8" not in base:
                e5_all.append((c, m))
    e5_stats = {"in_band": 0, "fast": 0, "slow": 0, "anomalous": 0,
                "missing": 0, "anomalous_corners": sorted({
                    fmt_c(corner_key(c)) for c, m in e5_all
                    if m.get("value") is not None and
                    (m["value"] <= 0 or m["value"] > 2 * ui)})}
    for c, m in e5_all:
        v = m.get("value")
        if v is None:
            e5_stats["missing"] += 1
        elif v <= 0 or v > 2 * ui:
            e5_stats["anomalous"] += 1
        elif v < e5_lo:
            e5_stats["fast"] += 1
        elif v > e5_hi:
            e5_stats["slow"] += 1
        else:
            e5_stats["in_band"] += 1
    summary = {
        "bench": "sim/driver-tran",
        "rate": rate,
        "what": ("Powered driver transient bench: PRBS-7 into 100 ohm with "
                 "1.0 pF per side, both DDR muxes + predriver + driver + "
                 "CMFB + pad cells via one lvds_tx_analog instance. E5 "
                 "(differential 20-80 % edges), E9 (eye height at the "
                 "stated sampling phase, isolated-bit crossing-gap width), "
                 "E4 dynamic (V_OS peak-to-peak), W1 (analog rail-power "
                 "subtotal)."),
        "simulated": True,
        "measured_in_silicon": False,
        "spec_status": "PROPOSED",
        "closes_no_spec_row": True,
        "closes_no_spec_row_reason": (
            "The spec is PROPOSED, not ratified; E4 is statistical and this "
            "bench supplies only its deterministic G75 transient half (the "
            "Monte Carlo remains); W1's serializer share is not measured, "
            "so total lane power is not graded here. Baseline, not a pass "
            "claim."),
        "grid": {
            "expected_conditions": 75,
            "seen_conditions": len(tuples),
            "distinct_tuples": len(tuples),
            "includes_crossed_pairs": all(
                p in rail_pairs for p in [(1.62, 3.63), (1.98, 2.97)]),
            "rail_pairs": sorted(rail_pairs),
        },
        "stimulus": {
            "prbs": meta["prbs"],
            "seed": meta["seed_hex"],
            "period_bits": meta["period_bits"],
            "ui_s": ui,
            "window_bits": meta["window_bits"],
            "window_s": meta["window_s"],
            "sample_phase_s": meta["sample_phase_s"],
            "input_edge_s": meta["input_edge_s"],
        },
        "rows": {
            r: {"measurements_pass": res[r]["pass"],
                "measurements_fail": res[r]["fail"],
                "measurements_error_or_missing": res[r]["error"]}
            for r in rows
        },
        "e5_edge_classification": e5_stats,
        "binding_corners": {
            f"{step}.{sr}": {"condition": b[1], "measurement": b[2],
                             "value": b[3], "margin": b[4], "limits": b[5]}
            for (step, sr), b in binding.items()},
        "w1_nominal_leg": w1_nom,
        "w1_serializer_share": {
            "included": False,
            "reason": ("flow/serializer/sta.response.json carries "
                       "engine_default-activity estimates only; the "
                       "gate-level serializer SPICE contribution at "
                       "matching rate/activity/core corner is future work. "
                       "Total lane power acceptance stays OPEN; "
                       "pw_analog_mv is the analog subtotal."),
        },
        "bit_order_observers": bit_checks,
        "latency_observer": lat,
        "conditions": conditions,
    }
    json.dump(summary, open(out_path, "w"), indent=1)
    print(f"wrote {out_path}: {len(conditions)} conditions, "
          f"tuples={len(tuples)}, rows={ {r: (res[r]['pass'], res[r]['fail'], res[r]['error']) for r in rows} }")


if __name__ == "__main__":
    main()
