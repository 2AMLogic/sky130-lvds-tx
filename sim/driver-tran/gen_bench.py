#!/usr/bin/env python3
"""Generate the driver transient bench artifacts (issue #168).

Deterministic: the PRBS-7 stream, the stimulus PWL sources, the deck and the
`klt sim` request JSONs are all pure functions of (rate, sample phase), so the
committed artifacts are byte-reproducible from this script.

  python3 gen_bench.py --rate 1g --sample-phase-ps 360

Emits into the current directory (run it from sim/driver-tran/):

  prbs7_stim_<rate>.spice   ideal-source PRBS-7 stimulus + strobe gates
  driver_tran_<rate>.spice  the bench deck (circuit body; klt sim composes)
  request-<rate>.json       the 75-condition G75 fleet request
  request-control.json      single-corner negative-control request (1 Gb/s)
  stim_meta_<rate>.json     the bit/crossing/edge map the summary re-derives

The 400 Mb/s fallback set (--rate 400m) is generated only if the 1 Gb/s bench
misses, per the issue text; its request is not committed otherwise.

Stimulus conventions (recorded in RECORD.md):

  * PRBS-7, Fibonacci LFSR x^7 + x^6 + 1, seed 0x01, period 127 bits.
  * b[i] is bit i on the wire; b[i] = lfsr[i mod 127].
  * Bit i occupies the ideal window [(i+1)*UI, (i+2)*UI): the first DDR clock
    rising edge, at t = UI, launches bit 0. Even-index bits ride D0 (launched
    by rising edges), odd-index bits ride D1 (falling edges), matching
    rtl/serializer.v's "bit 0 first on the DDR mux" (dout[0] = first bit).
  * Data lines update at (idx+0.5)*UI, midway through the UI before the
    launching edge: 0.25 UI setup and 0.25 UI hold against the capture.
  * The DDR mux is combinational (Q = D0 when CLK = 1, Q = D1 when CLK = 0),
    so pad bit boundaries sit on the clock edges plus the chain latency.
  * Settling interval [0, 128*UI); measurement window bits 127..253 inclusive,
    exactly one full 127-bit period, spanning [128*UI, 255*UI).
  * Sample phase: bit i is strobed at (i+1.5)*UI + t_samp; t_samp is the
    chain latency measured at the nominal tt/27C probe, so the strobe sits at
    the eye centre at nominal. The phase is fixed at all 75 conditions.

Measurement definitions (the load-bearing choices; see RECORD.md):

  * E5 is graded on the DIFFERENTIAL pad transition, 20-80 % of the window
    excursion of v(PADP)-v(PADN), measured per edge by two td-scoped WHEN
    cards and their expr difference. With a quiet common mode this is identical,
    by construction, to 20-80 % of each pad's own swing (pad thresholds at
    V_OS +- 0.3*V_OD are the same crossings); with this schematic's
    common-mode ripple (E4 dynamic) a per-pad fixed threshold is ill-defined
    edge by edge -- an individual pad can move against the data while the
    pair transitions -- so the differential transition is the well-defined
    reading of "rise/fall time at the pad". Each card covers one boundary:
    a rising card is PADP rising and PADN falling, and vice versa.
    Normalization uses the window's absolute vd extremes, which cannot
    invert at any corner; the settled eye levels are reported separately
    (m_eh/m_el/m_eye_h_v).
  * E9 width is graded per consecutive zero-crossing gap of the differential
    over the window: every bit's eye interval is bounded by its adjacent
    crossings, and the isolated-bit gaps (nominal 1 UI) carry the 0.75 UI
    limit; run gaps get the same +-0.25 UI window as anomaly guards.
  * E9 height is the worst 1-bit strobe sample minus the worst 0-bit strobe
    sample at the stated sampling phase (strobe = 2 ps flat + 0.5 ps ramps;
    PWL corners guarantee solver points inside every strobe).
  * E4 dynamic is the peak-to-peak of (PADP+PADN)/2 over the window.
  * W1 is the time-weighted mean of the delivered rail power over the window,
    i.e. mean of -(i(VVCCD)*v(VCCD) + i(VVDDIO)*v(VDDIO)). The serializer
    share is NOT included: m_pw_analog_mv is the analog subtotal and W1's
    total-power acceptance stays open (see RECORD.md).
"""

import argparse
import json

SEED = 0x01
N_BITS = 256          # bits 0..255 on the wire
SETTLE_LAST = 126     # bits 0..126 settle (127 bits)
WIN_FIRST = 127       # measured bits 127..253 (127 bits = one PRBS period)
WIN_LAST = 253
TAIL_UI = 2.5         # bit 255 ends at 257*UI; run to 257.5*UI

RATES = {
    "1g": dict(ui=1.0e-9, te=50e-12, tstep=2e-12, tmax=10e-12,
               e5_min=100e-12, e5_max=400e-12,
               e9_h_min=0.150, e9_w_isolated=0.75, guard_ui=0.25,
               w1_any_max=30.0, w1_nom_max=20.0),
    "400m": dict(ui=2.5e-9, te=125e-12, tstep=5e-12, tmax=25e-12,
                 e5_min=100e-12, e5_max=1000e-12,
                 e9_h_min=0.120, e9_w_isolated=0.60, guard_ui=0.25,
                 w1_any_max=30.0, w1_nom_max=18.0),
}


def prbs7():
    """Fibonacci LFSR x^7+x^6+1, seed SEED; returns one 127-bit period."""
    state = SEED
    out = []
    for _ in range(127):
        out.append((state >> 6) & 1)
        fb = ((state >> 6) ^ (state >> 5)) & 1
        state = ((state << 1) | fb) & 0x7F
    assert len(set(out)) == 2 and any(out)
    return out


def fmt_t(t):
    return f"{t:.6e}"


def pwl(pairs):
    body = " ".join(f"{fmt_t(t)} {v:.6g}" for t, v in pairs)
    return f"pwl({body})"


def clock_pairs(ui, te, tstop):
    """CLK: 0 during the quiet first UI, rising at odd UI multiples."""
    pairs = [(0.0, 0)]
    n = int(tstop / ui) + 1
    for k in range(1, n + 1):
        t = k * ui
        if t >= tstop:
            break
        level = 1 if k % 2 == 1 else 0
        pairs.append((t - te / 2, pairs[-1][1]))
        pairs.append((t + te / 2, level))
    pairs.append((tstop, pairs[-1][1]))
    return pairs


def data_pairs(bits, ui, te, tstop, parity):
    """Data pattern for one DDR phase. Bit idx rides this line from just
    after (idx+0.5)*UI -- midway through the UI before its launch edge --
    giving 0.25 UI setup and hold against the capturing clock edge."""
    val = bits[parity]
    pairs = [(0.0, val)]
    idx = parity + 2
    while idx <= N_BITS - 1:
        t_upd = (idx + 0.5) * ui
        val = bits[idx]
        pairs.append((t_upd - te / 2, pairs[-1][1]))
        pairs.append((t_upd + te / 2, val))
        idx += 2
    pairs.append((tstop, pairs[-1][1]))
    return pairs


def gate_pairs(bits, ui, tsamp, want, tstop):
    """Narrow strobes at each measured bit's sample point, 0/1 valued."""
    half, ramp = 2e-12, 0.5e-12
    pairs = [(0.0, 0)]
    for i in range(WIN_FIRST, WIN_LAST + 1):
        if bits[i] != want:
            continue
        c = (i + 1.5) * ui + tsamp
        pairs.append((c - half - ramp, 0))
        pairs.append((c - half, 1))
        pairs.append((c + half, 1))
        pairs.append((c + half + ramp, 0))
    pairs.append((tstop, 0))
    return pairs


def window_pairs(ui, tstop):
    """Measurement-window gate: 1 during [128*UI, 255*UI)."""
    w0, w1, ramp = 128 * ui, 255 * ui, 1e-12
    return [(0.0, 0), (w0 - ramp, 0), (w0, 1), (w1, 1), (w1 + ramp, 0),
            (tstop, 0)]


def write_stim(rate, bits, ui, te, tsamp, tstop):
    lines = [
        "* Ideal-source PRBS-7 stimulus and measurement strobe gates for the",
        f"* driver transient bench, {rate} rate (UI = {ui*1e9:g} ns). GENERATED BY",
        "* gen_bench.py -- do not edit by hand; regenerate instead.",
        "*",
        "* DR-007: every source here is IDEAL. The V-sources below drive unloaded",
        "* pattern/gate nodes (referenced only by the B-sources and the request's",
        "* measurement expressions); the B-sources scale the 0/1 patterns to the",
        "* corner's own VCCD so the DUT inputs always swing 0..VCCD.",
        "*",
        f"* PRBS-7: Fibonacci LFSR x^7 + x^6 + 1, seed 0x{SEED:02x}, period 127.",
        "* Bit i occupies [(i+1)*UI, (i+2)*UI); even bits on D0, odd bits on D1;",
        "* data lines update at (idx+0.5)*UI, 0.25 UI off each capture edge.",
        f"* Strobes: bit i sampled at (i+1.5)*UI + {fmt_t(tsamp)} s (s1 gates",
        "* 1-bits, s0 gates 0-bits); sw gates the measurement window",
        f"* [{fmt_t(128*ui)}, {fmt_t(255*ui)}] s. Gate fills are +-5 V so the",
        "* vecmin/vecmax reductions in the request are ramp-robust.",
        "",
        "VP0   p0    0 " + pwl(data_pairs(bits, ui, te, tstop, 0)),
        "VP1   p1    0 " + pwl(data_pairs(bits, ui, te, tstop, 1)),
        "VPCLK pclk  0 " + pwl(clock_pairs(ui, te, tstop)),
        "VS1   s1    0 " + pwl(gate_pairs(bits, ui, tsamp, 1, tstop)),
        "VS0   s0    0 " + pwl(gate_pairs(bits, ui, tsamp, 0, tstop)),
        "VSW   sw    0 " + pwl(window_pairs(ui, tstop)),
        "*",
        "* Ideal rail-tracking drivers for the DUT inputs (DR-007: ideal).",
        "BD0   d0    0 V = v(vccd)*v(p0)",
        "BD0B  d0b   0 V = v(vccd)*(1 - v(p0))",
        "BD1   d1    0 V = v(vccd)*v(p1)",
        "BD1B  d1b   0 V = v(vccd)*(1 - v(p1))",
        "BCLK  clk   0 V = v(vccd)*v(pclk)",
        "",
    ]
    path = f"prbs7_stim_{rate}.spice"
    with open(path, "w") as f:
        f.write("\n".join(lines))
    return path


DECK = """\
* Driver transient bench -- E5 (pad rise/fall), E9 (PRBS-7 eye), E4 dynamic
* (V_OS peak-to-peak) and W1 (lane power), spec rows of the PROPOSED
* spec/target-spec.md. Simulated, not measured; a schematic-level baseline,
* not a pass claim: the spec is PROPOSED, E4 still owes its Monte Carlo half
* and W1's serializer share is measured by a separate bench (see RECORD.md).
*
* Instantiates design/lvds_tx_analog.spice ONCE: both DDR muxes, predriver,
* driver with CMFB, and both pad cells. No device, bias or schematic change;
* the stimulus, load and references are ideal and DR-007-labelled.
*
* Bias: the driver DC bench's frozen values (IREF = 54.3 uA, VCMREF = 1.25 V,
* EN = VCCD, EM0 = EM1 = 0 V; sim/driver-dc/RECORD.md), so a miss here is a
* recorded miss, not a tuned-away one.
*
* Load: 100 ohm differential + 1.0 pF per side, the E5/E9 row's load. CLP/CLN
* are the negative control's handle: request-control.json alters them to
* 10 pF, which must push E5 beyond its upper limit at the same corner.
*
* Circuit body only: klt sim supplies .lib/.temp/.control (no .end here).

.include ../../design/lvds_tx_analog.spice
.include prbs7_stim_{rate}.spice

* ---------------------------------------------------------------------------
* Rails. corners.supply_v in the request is keyed by these two source names,
* so the five G75 (VCCD, VDDIO) pairs move as a set.
* ---------------------------------------------------------------------------
VVCCD  vccd  0 DC 1.8
VVDDIO vddio 0 DC 3.3

* ---------------------------------------------------------------------------
* Ideal external references (DR-007), frozen from sim/driver-dc:
*   vcmref -- CMFB target, 1.25 V at every condition.
*   iref   -- 54.3 uA forced into the driver's diode-connected XMNB1.
* ---------------------------------------------------------------------------
VVCMREF vcmref 0 DC 1.25
IIREF   0 iref  DC 54.3u

* ---------------------------------------------------------------------------
* The DUT: one lvds_tx_analog. Port order:
*   D0 D0B D1 D1B CLK EN EM0 EM1 IREF VCMREF PADP PADN VCCD VDDIO VSSIO
* EN ties to the vccd node (tracks the swept rail); pre-emphasis is off.
* ---------------------------------------------------------------------------
xtx d0 d0b d1 d1b clk vccd 0 0 iref vcmref padp padn vccd vddio 0 lvds_tx_analog

* ---------------------------------------------------------------------------
* The E5/E9 row load: 100 ohm across the pair, 1.0 pF from each pad to
* ground. The pad cells are inside the DUT (shunt-only, no series element),
* so PADP/PADN here are the pad nodes.
* ---------------------------------------------------------------------------
RL  padp padn 100
CLP padp 0 1p
CLN padn 0 1p
"""


def write_deck(rate):
    path = f"driver_tran_{rate}.spice"
    with open(path, "w") as f:
        f.write(DECK.format(rate=rate))
    return path


def measurements(bits, ui, tsamp, p):
    """The ordered measurement list for one tran step."""
    w0 = 128 * ui
    w1 = 255 * ui
    m = []

    def add(name, kind, val, unit, comment, spec_row=None, limits=None,
            intermediate=False):
        entry = dict(name=name, comment=comment, unit=unit)
        entry[kind] = val
        if intermediate:
            entry["intermediate"] = True
        if spec_row:
            entry["spec_row"] = spec_row
        if limits:
            entry["limits"] = limits
        m.append(entry)

    # 1. vector intermediates (let only; never printed or graded).
    add("m_vd", "expr", "v(padp)-v(padn)", "V",
        "intermediate: differential pad voltage", intermediate=True)
    add("m_vos", "expr", "(v(padp)+v(padn))/2", "V",
        "intermediate: instantaneous common mode", intermediate=True)
    add("m_pwr", "expr", "-i(vvccd)*v(vccd)-i(vvddio)*v(vddio)", "W",
        "intermediate: instantaneous delivered power; ngspice source current "
        "is positive into the + terminal, so the minus signs make sourcing "
        "positive", intermediate=True)
    for nm, expr, cm in [
        ("m_s1p", "v(s1)*v(padp)+(1-v(s1))*5",
         "PADP over 1-bit strobes, +5 V fill"),
        ("m_s0p", "v(s0)*v(padp)+(1-v(s0))*(-5)",
         "PADP over 0-bit strobes, -5 V fill"),
        ("m_s1n", "v(s1)*v(padn)+(1-v(s1))*(-5)",
         "PADN over 1-bit strobes, -5 V fill"),
        ("m_s0n", "v(s0)*v(padn)+(1-v(s0))*5",
         "PADN over 0-bit strobes, +5 V fill"),
        ("m_s1d", "v(s1)*(v(padp)-v(padn))+(1-v(s1))*5",
         "differential over 1-bit strobes, +5 V fill"),
        ("m_s0d", "v(s0)*(v(padp)-v(padn))+(1-v(s0))*(-5)",
         "differential over 0-bit strobes, -5 V fill"),
        ("m_vdwhi", "v(sw)*(v(padp)-v(padn))+(1-v(sw))*(-5)",
         "differential over the measurement window, -5 V fill (max basis)"),
        ("m_vdwlo", "v(sw)*(v(padp)-v(padn))+(1-v(sw))*5",
         "differential over the measurement window, +5 V fill (min basis)"),
    ]:
        add(nm, "expr", expr, "V", f"intermediate: {cm}", intermediate=True)

    # 2. levels (printed observers, ungraded).
    add("m_hi_p", "expr", "vecmin(m_s1p)", "V",
        "observer: worst settled high on PADP across 1-bit strobes; under "
        "common-mode ripple this can fall below m_lo_p -- that inversion is "
        "data (the E4 finding), not a bench error, and nothing is graded on it")
    add("m_lo_p", "expr", "vecmax(m_s0p)", "V",
        "observer: worst settled low on PADP across 0-bit strobes")
    add("m_hi_n", "expr", "vecmin(m_s0n)", "V",
        "observer: worst settled high on PADN across 0-bit strobes")
    add("m_lo_n", "expr", "vecmax(m_s1n)", "V",
        "observer: worst settled low on PADN across 1-bit strobes")
    add("m_eh", "expr", "vecmin(m_s1d)", "V",
        "eye high level: worst differential 1-bit sample at the stated phase")
    add("m_el", "expr", "vecmax(m_s0d)", "V",
        "eye low level: worst differential 0-bit sample at the stated phase")
    add("m_vhi", "expr", "vecmax(m_vdwhi)", "V",
        "observer: differential window maximum")
    add("m_vlo", "expr", "vecmin(m_vdwlo)", "V",
        "observer: differential window minimum")

    # 3. E9 height, graded.
    add("m_eye_h_v", "expr", "m_eh - m_el", "V",
        "E9 eye height at the stated sampling phase = worst 1-bit sample "
        "minus worst 0-bit sample", spec_row="E9",
        limits={"min": p["e9_h_min"], "max": 1.0})

    # 4. normalized differential vector for E5. Basis: the differential's
    # window EXTREMES (cannot invert at any corner). Because the per-edge
    # cards below are td-scoped, an edge whose amplitude never reaches the
    # 0.8-of-extremes level (ISI- or CMFB-corrupted corners) errors ONLY its
    # own cards -- recorded as an unmeasured edge, no cascade -- while at
    # well-behaved corners every edge completes and the reading is the
    # 20-80 % time of the full swing. (An eye-level basis was tried and
    # rejected: its thresholds shrink with the achieved swing, so load
    # changes stop moving the measured edge time and the E5 grader loses
    # its load sensitivity -- see RECORD.md, negative control.)
    add("m_vdn", "expr", "(v(padp)-v(padn)-m_vlo)/(m_vhi-m_vlo)", "V",
        "intermediate: differential normalized to its window extremes",
        intermediate=True)

    # 5. E5 per-boundary cards on the differential transition (see the
    # module docstring for why per-pad fixed thresholds are ill-defined).
    # Each edge gets two td-scoped WHEN cards (first 20 % and 80 % crossing
    # of the normalized signal after Tm = boundary - 0.25*UI) and an expr
    # difference, so the pairing is event-local: ngspice's td= on a WHEN
    # card scopes the rise/fall count (verified), unlike on trig/targ cards
    # where it silently mispairs. An edge that never completes a level
    # errors its own card only; nothing else shifts.
    e5 = []
    e5_map = []
    tm_off = 0.25 * ui
    for i in range(WIN_FIRST - 1, WIN_LAST):
        if bits[i] == bits[i + 1]:
            continue
        bit = i + 1
        tm = fmt_t((i + 2) * ui - tm_off)
        rising = bits[i] == 0
        lo_lvl, hi_lvl = ("0.2", "0.8") if rising else ("0.8", "0.2")
        kind = "rise=1" if rising else "fall=1"
        tag = "r" if rising else "f"
        desc = ("PADP rising / PADN falling" if rising
                else "PADP falling / PADN rising")
        add(f"m_e5{tag}t20b{bit}", "spice",
            f".meas tran m_e5{tag}t20b{bit} when m_vdn={lo_lvl} {kind} "
            f"td={tm}", "s",
            f"20 % point of bit {bit} entry ({desc}); observer, the graded "
            "quantity is m_e5{tag}b{bit}")
        add(f"m_e5{tag}t80b{bit}", "spice",
            f".meas tran m_e5{tag}t80b{bit} when m_vdn={hi_lvl} {kind} "
            f"td={tm}", "s",
            f"80 % point of bit {bit} entry ({desc}); observer")
        add(f"m_e5{tag}b{bit}", "expr",
            f"m_e5{tag}t80b{bit} - m_e5{tag}t20b{bit}", "s",
            f"E5: 20-80 % of bit {bit} entry ({desc})",
            spec_row="E5", limits={"min": p["e5_min"], "max": p["e5_max"]})
        e5.append((f"m_e5{tag}b{bit}", "", f"bit {bit} entry ({desc})"))
        e5_map.append({"name": f"m_e5{tag}b{bit}", "spec_row": "E5"})

    # 6. E9 width: consecutive zero-crossing gaps of the differential, with
    # the same global crossing indices as the E5 cards.
    g_crossings = [i for i in range(0, N_BITS - 1) if bits[i] != bits[i + 1]]
    win_first_idx = next(k for k, i in enumerate(g_crossings)
                         if i >= WIN_FIRST - 1)
    gap_cards = []
    for j in range(win_first_idx, len(g_crossings) - 1):
        i0, i1 = g_crossings[j], g_crossings[j + 1]
        if i1 > WIN_LAST - 1:
            break
        gap = (i1 - i0) * ui
        lo = gap - p["guard_ui"] * ui
        hi = gap + p["guard_ui"] * ui
        isolated = (i1 - i0) == 1
        gap_cards.append((j, i0, i1, gap, lo, hi, isolated))
    for j, i0, i1, gap, lo, hi, isolated in gap_cards:
        comment = (f"bit {i0+1}..{i1} crossing gap, nominal {gap*1e9:g} ns"
                   + ("; isolated bit, carries the E9 width limit"
                      if isolated else "; run guard, window only"))
        add(f"m_e9w{j+1}", "spice",
            f".meas tran m_e9w{j+1} trig m_vd val=0 cross={j+1} "
            f"targ m_vd val=0 cross={j+2}", "s", comment,
            spec_row="E9" if isolated else None,
            limits={"min": lo, "max": hi})

    # 7. E4 dynamic half.
    add("m_vos_pp", "spice",
        f".meas tran m_vos_pp pp m_vos from={fmt_t(w0)} to={fmt_t(w1)}",
        "V", "E4 dynamic half: peak-to-peak V_OS over the settled PRBS window",
        spec_row="E4", limits={"min": 0.0, "max": 0.15})

    # 8. W1 (analog subtotal; see RECORD.md for the open serializer share).
    add("m_i_vccd_avg", "spice",
        f".meas tran m_i_vccd_avg avg i(vvccd) from={fmt_t(w0)} to={fmt_t(w1)}",
        "A", "observer: mean VCCD source current (negative = sourcing)")
    add("m_i_vddio_avg", "spice",
        f".meas tran m_i_vddio_avg avg i(vvddio) from={fmt_t(w0)} to={fmt_t(w1)}",
        "A", "observer: mean VDDIO source current (negative = sourcing)")
    add("m_p_avg", "spice",
        f".meas tran m_p_avg avg m_pwr from={fmt_t(w0)} to={fmt_t(w1)}",
        "W", "observer: time-weighted mean delivered power over the window")
    add("m_pw_analog_mv", "expr", "m_p_avg*1e3", "mW",
        "W1 analog subtotal (muxes + predriver + driver + CMFB + pad cells, "
        "both rails), graded against the <= 30 mW any-G75-condition cap. NOT "
        "the full W1: the serializer share is not included, and the "
        f"<= {p['w1_nom_max']:g} mW nominal-TT leg is reported from this same "
        "grid's tt/27C/1.80/3.30 row by summarize.py (RECORD.md)",
        spec_row="W1", limits={"min": 0.0, "max": p["w1_any_max"]})

    # 9. Bit-order observers: the differential at declared sample points.
    for i in [127, 128, 133, 135, 136, 137, 190, 252, 253]:
        t = (i + 1.5) * ui + tsamp
        add(f"m_bit{i}", "spice",
            f".meas tran m_bit{i} find m_vd at={fmt_t(t)}", "V",
            f"bit-order observer, bit {i}: expected {bits[i]} "
            f"({'positive' if bits[i] else 'negative'} differential)")

    # 10. Latency observer: absolute time of one isolated-bit entry crossing
    # (global crossing index; see the E5 note above).
    lat_j = None
    for j in range(len(g_crossings) - 1):
        if g_crossings[j + 1] - g_crossings[j] == 1 \
                and WIN_FIRST - 1 <= g_crossings[j] <= WIN_LAST - 1:
            lat_j = j
            break
    lat_meta = None
    if lat_j is not None:
        i0 = g_crossings[lat_j]
        t_nom = (i0 + 2) * ui
        lat_meta = {"measurement": "m_xlat", "crossing_global": lat_j + 1,
                    "bit": i0 + 1, "nominal_s": t_nom}
        add("m_xlat", "spice",
            f".meas tran m_xlat when m_vd=0 cross={lat_j+1}", "s",
            f"chain-latency observer: absolute time of crossing {lat_j+1} "
            f"(bit {i0+1} entry, nominal {fmt_t(t_nom)} s)")

    return m, dict(crossings=g_crossings, e5_cards=e5, e5_map=e5_map,
                   gap_cards=gap_cards, latency=lat_meta)


def g75_corners():
    return {
        "process": ["tt", "ff", "ss", "sf", "fs"],
        "temperature_c": [-40, 27, 125],
        "supply_v": {
            "VVCCD": [1.62, 1.8, 1.98, 1.62, 1.98],
            "VVDDIO": [2.97, 3.3, 3.63, 3.63, 2.97],
        },
    }


def base_options():
    return {
        "timeout_s": 900,
        "stage_model_inputs": True,
        "ngspice_init": ["set wnflag=1", "set num_threads=1"],
        "node_voltage_bounds": {"min": -0.5, "max": 4.0},
        "save_vectors": [
            "v(padp)", "v(padn)", "v(vccd)", "v(vddio)",
            "v(s1)", "v(s0)", "v(sw)", "i(vvccd)", "i(vvddio)",
        ],
    }


def write_requests(rate, bits, ui, tsamp, p, control_corner, control_cap,
                   control_ref_cap):
    tstop = (N_BITS + 1 + TAIL_UI - 1) * ui  # 257.5 * UI
    m, maps = measurements(bits, ui, tsamp, p)
    tran = {"kind": "tran",
            "args": f"{fmt_t(p['tstep'])} {fmt_t(tstop)} 0 {fmt_t(p['tmax'])}"}

    main = {
        "netlist": f"driver_tran_{rate}.spice",
        "netlist_source": "schematic",
        "models": {"pdk": "sky130A",
                   "lib": "libs.tech/ngspice/sky130.lib.spice"},
        "corners": g75_corners(),
        "analysis_steps": [{"name": "seq", "analysis": tran, "measurements": m}],
        "options": base_options(),
        "batch": {"capacity_wait_s": 600},
    }
    with open(f"request-{rate}.json", "w") as f:
        json.dump(main, f, indent=1)
        f.write("\n")

    # Negative control fixture (E5 grader detection), RECORD.md "Checks run
    # on the bench itself". Built from the 400 Mb/s stimulus: at that rate
    # the 22 pF step's edges are clean single RC transitions well past the
    # 1.0 ns upper limit, while the 2 pF reference lands inside the
    # 100 ps - 1.0 ns window -- increasing ONLY the external capacitance
    # flips the E5 verdict. (At 1 Gb/s the nominal 1 pF edges
    # are ~89 ps, below the lower bound, so no 1 Gb/s load demonstrates the
    # pass-to-fail change; at 10 pF/1 Gb/s the ringing dominates and the
    # first-crossing definition stops reading a settling edge.)
    proc, temp, vccd, vddio = control_corner
    m_ref, _ = measurements(bits, ui, tsamp, p)
    m_ctl, _ = measurements(bits, ui, tsamp, p)
    control = {
        "netlist": f"driver_tran_{rate}.spice",
        "netlist_source": "schematic",
        "models": {"pdk": "sky130A",
                   "lib": "libs.tech/ngspice/sky130.lib.spice"},
        "corners": {
            "process": [proc],
            "temperature_c": [temp],
            "supply_v": {"VVCCD": [vccd], "VVDDIO": [vddio]},
        },
        "analysis_steps": [
            {"name": "ref", "analysis": dict(tran),
             "alter": {"CLP": control_ref_cap, "CLN": control_ref_cap},
             "measurements": m_ref},
            {"name": "ctl", "analysis": dict(tran), "reset": True,
             "alter": {"CLP": control_cap, "CLN": control_cap},
             "measurements": m_ctl},
        ],
        "options": base_options(),
        "batch": {"capacity_wait_s": 600},
    }
    with open("request-control.json", "w") as f:
        json.dump(control, f, indent=1)
        f.write("\n")

    meta = {
        "rate": rate,
        "control_fixture": {
            "corner": f"{proc}/{temp}C/{vccd}/{vddio}",
            "ref_cap_f_per_side": control_ref_cap,
            "ctl_cap_f_per_side": control_cap,
        },
        "ui_s": ui,
        "seed_hex": f"0x{SEED:02x}",
        "prbs": "x^7 + x^6 + 1, Fibonacci",
        "period_bits": 127,
        "n_bits": N_BITS,
        "settle_bits": [0, SETTLE_LAST],
        "window_bits": [WIN_FIRST, WIN_LAST],
        "window_s": [128 * ui, 255 * ui],
        "sample_phase_s": tsamp,
        "input_edge_s": p["te"],
        "tstop_s": tstop,
        "tmax_s": p["tmax"],
        "bits": bits[:N_BITS],
        "crossings": [
            {"global": j + 1, "left_bit": i, "bit": i + 1,
             "in_window": WIN_FIRST - 1 <= i <= WIN_LAST - 1,
             "nominal_s": (i + 2) * ui}
            for j, i in enumerate(maps["crossings"])],
        "e5_edges": [
            {"name": n, "comment": c} for n, _c, c in maps["e5_cards"]],
        "latency_observer": maps["latency"],
        "limits": {k: p[k] for k in
                   ["e5_min", "e5_max", "e9_h_min", "w1_any_max",
                    "w1_nom_max"]},
    }
    # the report envelope does not echo spec_row/limits back onto each
    # measurement, so the summary joins through this map
    row_map = {e["name"]: e["spec_row"] for e in maps["e5_map"]}
    row_map.update({f"m_e9w{j+1}": "E9" for j, _i0, _i1, _g, _lo, _hi, s
                    in maps["gap_cards"] if s})
    row_map["m_eye_h_v"] = "E9"
    row_map["m_vos_pp"] = "E4"
    row_map["m_pw_analog_mv"] = "W1"
    meta["row_map"] = row_map
    iso = [gc for gc in maps["gap_cards"] if gc[6]]
    meta["e9_isolated_gaps"] = [
        {"measurement": f"m_e9w{j+1}", "nominal_s": gap,
         "limits_s": [lo, hi]} for j, _i0, _i1, gap, lo, hi, _s in iso]
    with open(f"stim_meta_{rate}.json", "w") as f:
        json.dump(meta, f, indent=1)
        f.write("\n")
    return maps


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rate", choices=list(RATES), default="1g")
    ap.add_argument("--sample-phase-ps", type=float, required=True,
                    help="chain latency from the nominal probe, in ps; the "
                         "strobes sit at (i+1.5)*UI + this")
    ap.add_argument("--control-corner", default="tt,27,1.8,3.3",
                    help="process,tempC,VCCD,VDDIO for the negative-control "
                         "fixture (see RECORD.md)")
    ap.add_argument("--control-ref-cap-f", type=float, default=2e-12,
                    help="per-side load cap of the control REFERENCE step "
                         "(default 2 pF: at tt/27C all 64 edges land inside "
                         "the 100-400 ps E5 window, a passing reference)")
    ap.add_argument("--control-cap-f", type=float, default=2.2e-11,
                    help="per-side load cap of the control step (default "
                         "22 pF: pushes every edge past the 1.0 ns upper "
                         "limit -- increasing ONLY the external capacitance)")
    args = ap.parse_args()
    p = RATES[args.rate]
    ui = p["ui"]
    tsamp = args.sample_phase_ps * 1e-12
    period = prbs7()
    bits = [period[i % 127] for i in range(N_BITS)]
    tstop = (N_BITS + 1 + TAIL_UI - 1) * ui
    write_stim(args.rate, bits, ui, p["te"], tsamp, tstop)
    write_deck(args.rate)
    proc, temp, vccd, vddio = args.control_corner.split(",")
    control_corner = (proc, int(temp), float(vccd), float(vddio))
    write_requests(args.rate, bits, ui, tsamp, p, control_corner,
                   args.control_cap_f, args.control_ref_cap_f)
    print(f"wrote {args.rate} bench: UI={ui*1e9:g}ns tstop={tstop*1e9:g}ns "
          f"tsamp={args.sample_phase_ps:g}ps")


if __name__ == "__main__":
    main()
