#!/usr/bin/env python3
"""Fold a nominal PADP - PADN waveform into a labelled two-UI eye (SVG).

Usage: eye_plot.py WAVEFORM.raw.json STIM_META.json OUT.svg OUT.json

SIMULATED data (ngspice, nominal TT, 27 C, 1.8 V / 3.3 V). Dependency-free.
Besides the plot, OUT.json records the sign of PADP - PADN at the sample
point of every bit 126..254 against the seeded PRBS-7 value, so the check
covers both sides of the sequence wrap (bits 253/254 and 126/127).
"""

import json
import sys


def main(wave_path, meta_path, svg_path, json_path):
    wave = json.load(open(wave_path))
    meta = json.load(open(meta_path))
    names = [v["name"] for v in wave["variables"]]
    ip, in_ = names.index("v(padp)"), names.index("v(padn)")
    pts = [(p[0], p[ip] - p[in_]) for p in wave["points"]]
    ui, tsamp, bits = meta["ui_s"], meta["sample_phase_s"], meta["bits"]
    first, last = meta["window_bits"]

    def at(t):
        lo, hi = 0, len(pts) - 1
        while hi - lo > 1:
            mid = (lo + hi) // 2
            lo, hi = (mid, hi) if pts[mid][0] <= t else (lo, mid)
        (t0, v0), (t1, v1) = pts[lo], pts[hi]
        return v0 + (v1 - v0) * (t - t0) / (t1 - t0)

    order = []
    for i in range(first - 1, last + 2):
        v = at((i + 1.5) * ui + tsamp)
        order.append({"bit": i, "expected": bits[i], "vd_v": round(v, 6),
                      "ok": (v > 0) == bool(bits[i]) and v != 0})
    result = {
        "corner": "tt/27C/1.8/3.3", "simulated": True, "ui_s": ui,
        "sample_phase_after_launch_s": 0.5 * ui + tsamp,
        "bits_checked": [first - 1, last + 1],
        "bit_order_ok": all(o["ok"] for o in order), "samples": order,
    }
    json.dump(result, open(json_path, "w"), indent=1)

    # Fold: launch of bit i is at (i + 1) UI; plot two UI starting 0.5 UI before launch.
    w, h, mx, my, vmax = 760, 420, 60, 40, 0.8
    X = lambda ph: mx + (ph / 2.0) * (w - 2 * mx)
    Y = lambda v: my + (1 - (v + vmax) / (2 * vmax)) * (h - 2 * my)
    stride = 1  # solver steps are already adaptive (~8 ps average)
    paths = []
    for i in range(first, last):
        t0 = (i + 1) * ui - 0.5 * ui
        seg = [(p[0] - t0) / ui for p in pts[::stride] if t0 <= p[0] <= t0 + 2 * ui]
        vs = [p[1] for p in pts[::stride] if t0 <= p[0] <= t0 + 2 * ui]
        d = " ".join(f"{'M' if k == 0 else 'L'}{X(s):.1f},{Y(v):.1f}"
                     for k, (s, v) in enumerate(zip(seg, vs)))
        paths.append(f'<path d="{d}"/>')
    xs = X(0.5 + (0.5 * ui + tsamp) / ui)  # sample phase after launch (+0.5 UI lead-in)
    xs2 = X(1.5 + (0.5 * ui + tsamp) / ui)
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'font-family="sans-serif" font-size="12">',
        f'<rect width="{w}" height="{h}" fill="white"/>',
        f'<text x="{w/2}" y="20" text-anchor="middle" font-size="14">SIMULATED eye, '
        f'PADP - PADN, {ui*1e9:g} ns UI, nominal TT 27 C 1.8 V / 3.3 V, '
        f'PRBS-7 bits {first}-{last}</text>',
        f'<g fill="none" stroke="#1f77b4" stroke-opacity="0.25" stroke-width="1">'
        + "".join(paths) + "</g>",
        f'<line x1="{mx}" x2="{w-mx}" y1="{Y(0):.1f}" y2="{Y(0):.1f}" stroke="#888"/>',
    ]
    for x in (xs, xs2):
        if mx <= x <= w - mx:
            svg.append(f'<line x1="{x:.1f}" x2="{x:.1f}" y1="{my}" y2="{h-my}" '
                       f'stroke="#d62728" stroke-dasharray="4 3"/>')
    svg.append(f'<text x="{xs+4:.1f}" y="{my+12}" fill="#d62728">sampling phase</text>')
    for v in (-0.6, -0.3, 0, 0.3, 0.6):
        svg.append(f'<text x="{mx-6}" y="{Y(v)+4:.1f}" text-anchor="end">{v*1000:.0f}</text>')
    svg.append(f'<text x="14" y="{h/2}" transform="rotate(-90 14,{h/2})" '
               f'text-anchor="middle">differential (mV)</text>')
    for k in range(5):
        svg.append(f'<text x="{X(k*0.5):.1f}" y="{h-my+18}" text-anchor="middle">'
                   f'{(k*0.5-0.5):+.1f} UI</text>')
    svg.append(f'<text x="{w/2}" y="{h-6}" text-anchor="middle">time relative to bit launch</text>')
    svg.append("</svg>")
    open(svg_path, "w").write("\n".join(svg) + "\n")
    print("bit_order_ok", result["bit_order_ok"], "bits", result["bits_checked"])


if __name__ == "__main__":
    main(*sys.argv[1:5])
