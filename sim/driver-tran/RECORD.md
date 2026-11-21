# Driver transient bench — PRBS-7 eye, edges, dynamic V_OS and lane power record

**Simulated, not measured.** No silicon exists. Every number below is an
ngspice transient on the committed `lvds_tx_analog` netlist, against a
**PROPOSED** spec (`spec/target-spec.md` is a proposal, not a ratified
datasheet). The stimulus, references and load are **ideal**, DR-007-labelled.

**This bench closes no spec row.** Three reasons, each independent:

1. The spec is PROPOSED, not ratified; nothing here makes item 5 graded `met`.
2. **E4 is a statistical row** (G75 + local-mismatch Monte Carlo). This bench
   supplies the deterministic G75 transient half of E4 only; the Monte Carlo
   remains open (as does re-joining it with `sim/driver-dc/`'s DC half).
3. **W1's serializer share is not measured.** `m_pw_analog_mv` is the *analog
   subtotal* (both DDR muxes + predriver + driver + CMFB + pad cells, both
   rails). `flow/serializer/sta.response.json` carries `engine_default`
   -activity power estimates at its own corner set — applying one of those
   across G75 would not verify W1, so the total-power acceptance stays
   **open**: the missing contribution is a gate-level serializer SPICE run at
   matching rate, activity and core corner, counted once.

**It changes no device size, bias or schematic.** The bias is the driver DC
bench's frozen values (`IREF` = 54.3 µA, `VCMREF` = 1.25 V, `EN` = VCCD,
`EM0` = `EM1` = 0 V, `sim/driver-dc/RECORD.md`), so a miss below is a
recorded miss, not a tuned-away one. This baseline was recorded **before**
the sizing work of #166 lands; re-run it unchanged afterwards.

Schematic revision: `lvds_tx_analog.spice` as committed at `e27999f`
(sha256 `b90b61fd…`), which is the revision the DC baseline recorded.

## Headline

Both rates were run because the 1 Gb/s target **misses** (E4 below); the
400 Mb/s fallback request was then submitted and both result sets are
committed. Per row, over all 75 G75 conditions (150 measured edges'
worth of per-edge cards per rate; see "What ran"):

| Spec row | Limit (1 Gb/s) | 1 Gb/s verdict | Limit (400 Mb/s) | 400 Mb/s verdict |
|---|---|---|---|---|
| E5 rise/fall 20–80 % | 100–400 ps | **miss** — 2270 / 4800 edges in band; 3 / 75 conditions pass every edge | 100–1000 ps | **miss** — 2468 / 4800 in band; 3 / 75 conditions |
| E9 height at sampling phase | ≥ 150 mV | **73 / 75** pass (worst 101 mV) | ≥ 120 mV | **pass 73 / 75** (same two corners miss) |
| E9 width (isolated-bit gap) | ≥ 0.75 UI | **pass 2400 / 2400** graded gaps | ≥ 0.60 UI | **pass 2400 / 2400** |
| E4 dynamic, V_OS(PP) | ≤ 150 mV | **miss at all 75** (min 196 mV) | ≤ 150 mV | **miss at all 75** (min 180 mV) |
| W1 analog subtotal | ≤ 30 mW any condition | **pass 75 / 75** (max 14.4 mW) | ≤ 30 mW | **pass 75 / 75** (max 14.1 mW) |
| W1 nominal-TT leg | ≤ 20 mW at tt/27C/1.80/3.30 | **pass**, 12.44 mW | ≤ 18 mW | **pass**, 12.18 mW |

W1's rows grade the **analog subtotal only**; total lane power is open
(point 3 above). The W1 budget arithmetic in `spec/target-spec.md` allocates
3 mW of core-domain headroom, and `sta.response.json`'s engine_default
estimates are ≤ 0.82 mW — consistent with headroom existing — but that is
not a measurement at matching activity and is not applied.

### The dominant finding: the common-mode feedback limit cycle

E4's dynamic half fails at **every** condition at both rates, and the
mechanism is visible in the waveforms: the common mode holds its **mean** at
the 1.25 V target (nominal window mean 1.2477 V — the loop regulates the
average, exactly what the DC bench saw) while executing a slow limit cycle
of **±0.37 V** around it. During a run of identical bits V_OS drifts at
~45 mV/ns for nanoseconds at a time; the differential pair stays clean
(±0.375 V nominal) because the wobble is common to both pads, which is also
why E9 passes almost everywhere despite E4 failing everywhere. The cycle is
rate-driven: it persists at 400 Mb/s (V_OS(PP) 180 mV – 1.67 V) essentially
unchanged from 1 Gb/s (196 mV – 1.67 V).

The observed V_OS(PP) range over the grid: **0.196 – 1.668 V** (1 Gb/s), worst
at `sf/-40C/1.62/2.97` — the same low-VDDIO conditions that miss E1 in the
DC bench. The best corner (`fs/125C/1.62/2.97`, 196 mV) still exceeds the
150 mV limit. This is a **schematic-level stability finding for the sizing
follow-up (#166)**, not a bench artefact: the stimulus is ideal, the load is
the spec's own 100 Ω ‖ 1 pF, and the DC half of E4 is a non-event by
comparison (|ΔV_OS| ≤ 0.11 mV in `driver-dc`).

### E5: too fast at strong corners, unmeasurable at the weakest

The E5 edge population (per-edge 20–80 % cards, 64 edges × 75 conditions =
4800 per rate):

| Classification | 1 Gb/s | 400 Mb/s |
|---|---:|---:|
| in band (100–400 / 100–1000 ps) | 2270 | 2468 |
| **below the 100 ps lower bound** | 2377 | 2174 |
| above the upper bound | 8 | 34 |
| anomalous pairing (see below) | 133 | 124 |
| unmeasured (edge never completes) | 12 | 0 |

The dominant miss is the **lower** bound: at strong corners the committed
driver's differential edge into the spec load is ~85–95 ps, faster than the
proposed 100 ps coupling limit (nominal ~89 ps, measured on the raw waveform
before any grading). The 12 unmeasured edges (1 Gb/s only) are isolated-bit
entries at `sf` low-rail corners whose differential amplitude never reaches
80 % of the window excursion — the E4 limit cycle eats the swing; those
corners miss E9 height anyway (below). The 133/124 "anomalous" values are
pairing artefacts at the same eight CMFB-corrupted corners (value ≤ 0 or
> 2 UI): the two `td`-scoped WHEN cards caught different physical features.
They are recorded as failures in the envelope (the limits reject them) and
classified out of the statistics in `results/summary-*.json`
(`e5_edge_classification`); the eight corners are named there.

### E9: the differential eye itself is wide open where the driver has swing

Eye height at the stated sampling phase (see "Stimulus") misses at exactly
two conditions at both rates: `sf/-40C/1.62/2.97` (101 mV) and
`sf/-40C/1.98/2.97` (109 mV) — the DC bench's two weakest-V_OD corners
(117.1 / 117.5 mV DC V_OD). Everywhere else the eye is 0.13 – 0.63 V.
The isolated-bit crossing-gap width — the lower bound on every bit's eye
interval at 0 V differential — passes all 2400 graded gaps per rate with
the worst margins reported in the summaries; the run-gap guards
(±0.25 UI windows on multi-bit gaps, 2475 − 2400 = 75+... precisely: 31 run
guards per condition) tripped **zero** times, so no spurious extra
zero-crossings went undetected anywhere in the grid.

### W1: the analog subtotal fits every cap with margin

4.04 – 14.40 mW over the grid (worst `ff/27C/1.98/3.63`), 12.44 mW at
nominal — inside both the ≤ 30 mW any-condition cap and the ≤ 20 / ≤ 18 mW
nominal legs. The serializer share (open, above) is the only thing between
these numbers and a total-power verdict. Rail-current observers
(`m_i_vccd_avg`, `m_i_vddio_avg`) confirm the sign convention: both read
negative (sourcing), and `m_pwr = −(i·v)` sums positive.

## Provenance

| Field | Value |
|---|---|
| Repo base commit | `e27999f5593527e2116531d0583843666698fd85` (inputs content-hashed below) |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (`docs/environment.md`, `~/.ciel` via `PDK_ROOT`) |
| Model library sha256 | `17c208a699228f5acb87bf59c09c22a4c4d3937b6766b4957737d34e8e075f64` (`sky130.lib.spice`, same pin as `driver-dc`) |
| DUT netlist sha256 | `b90b61fd…` (`design/lvds_tx_analog.spice`, `.include`d, not copied; muxes/predriver/driver/pad cells all inside) |
| Testbench sha256 | `7f33ab03…` (`driver_tran_1g.spice`), `41226b55…` (`driver_tran_400m.spice`) |
| Stimulus sha256 | `4e54adaf…` (`prbs7_stim_1g.spice`), `16742e61…` (`prbs7_stim_400m.spice`), generated by `gen_bench.py` (`393f2d70…`) |
| Requests sha256 | in `results/batch-receipt-*.json` (`request_sha256`, tying each job to its request bytes) |
| Client | klt `0.9.3.dev2575+g6bd18bbc8637`, klayout 0.30.13 |
| Engine | ngspice **47** on the batch workers (`c7i.4xlarge` / `m7i.4xlarge` spots), `set wnflag=1`, `set num_threads=1` declared in the requests — load-bearing for the same reason as `driver-dc`'s wnflag trap |
| Backend | `batch`: 1 Gb/s job `klt-sim-c99eee14c6df` (75 units), 400 Mb/s job `klt-sim-cdc1aae98ed2` (75 units), control job `klt-sim-e4bd8b0658d2` (1 unit), `options.stage_model_inputs: true`, `batch.capacity_wait_s: 600` |

Reproduce (from the repo root, `PDK_ROOT` at the pinned ciel root):

```console
python3 sim/driver-tran/gen_bench.py --rate 1g --sample-phase-ps 360
python3 sim/driver-tran/gen_bench.py --rate 400m --sample-phase-ps 360
PDK_ROOT=<pinned ciel root> klt sim sim/driver-tran/request-1g.json \
    --backend batch --wait-for-capacity 600 \
    --report-out sim/driver-tran/results/report-1g.json
# same for request-400m.json and request-control.json, then
python3 sim/driver-tran/summarize.py <report> <stim_meta> <label> <out>
```

The two `gen_bench.py` invocations are ordered: the second writes
`request-control.json` from the 400 Mb/s stimulus (see the negative control).
Results committed verbatim: `results/report-{1g,400m}.json.gz`,
`results/summary-{1g,400m}.json`, `results/control/`.

## What ran

Three `klt sim` requests over the **G75** grid (`spec/target-spec.md`
§"The PVT grid"): process `tt, ff, ss, sf, fs` × −40, 27, 125 °C × the five
index-zipped (VCCD, VDDIO) pairs = **75 conditions each**, both crossed rail
pairs included — reconciled in the summaries (`grid.distinct_tuples: 75`,
`rail_pairs` listed). One `analysis_steps` sequence per corner: a single
`tran` (`2p 258.5n 0 10p` at 1 Gb/s; `5p 646.25n 0 25p` at 400 Mb/s) whose
step carries the whole measurement set; the negative control runs two steps
(`ref`, `ctl`) at one corner.

Measurements are `expr` lets (reductions over saved vectors), step-scoped
`.meas` cards, and derived exprs — 291 entries per corner per rate. The
per-measurement rollups above count **graded measurement instances**
(e.g. E5: 64 edge exprs × 75 corners = 4800); a row's per-condition verdict
is the conjunction of its instances at that condition, and the summaries
carry both views (`rows` = instance counts, `conditions[].rows` = the
per-condition conjunction).

## Stimulus, and why each value

| Item | Value | Why |
|---|---|---|
| Pattern | PRBS-7, Fibonacci LFSR x⁷+x⁶+1, seed `0x01`, period 127 | the E4/E9 rows' named pattern; max run 7, 64 transitions per period |
| Rate | 1 Gb/s (UI 1 ns) and 400 Mb/s (UI 2.5 ns) | target + fallback; the fallback ran because the target missed |
| Launch | bit *i* occupies [(i+1)·UI, (i+2)·UI); even bits on D0 (rising edges), odd bits on D1 (falling edges) | matches `rtl/serializer.v`'s "bit 0 first on the DDR mux" (`dout[0]` first, bit 0 of each word out first); the mux is combinational, `Q = D0` when `CLK = 1` |
| Input updates | (idx+0.5)·UI, i.e. 0.25 UI off each capture edge | 0.25 UI setup / 0.25 UI hold on both phases |
| Input edges | 50 ps (1 Gb/s) / 125 ps (400 Mb/s) ramps, 0→VCCD via B-sources | ideal-but-finite drive; swings track the corner's VCCD |
| Settling | bits 0–126 (one full period, 128·UI of simulated time) | generous against the CMFB cycle |
| Measurement window | bits 127–253 = exactly one full 127-bit period, [128·UI, 255·UI) | ≥ 1 complete period after settling, incl. the 127-bit wrap and word boundaries |
| Sampling phase | (i+1.5)·UI + **360 ps** (both rates) | the chain latency measured at nominal (observer `m_xlat`: 134.36 ns against a 134 ns nominal crossing ⇒ 0.36 ns); fixed at all 75 conditions; grid latency range 234–687 ps, so the strobe sits ≤ 0.33 UI off centre at the extremes and stays inside the eye (E9 passes bear this out) |
| Strobes | 2 ps flat + 0.5 ps ramps at each sample point; PWL corners guarantee solver points inside every strobe | grid-robust worst-case min/max sampling |
| Load | 100 Ω across the pair, 1.0 pF per side to ground | the E5/E9 row's load; CLP/CLN are the control's handle |
| Bias | IREF 54.3 µA, VCMREF 1.25 V, EN = VCCD, EM0 = EM1 = 0 | frozen from `sim/driver-dc/RECORD.md` |

Bit-order verification: nine `FIND ... AT` observers per corner read the
differential at declared sample points spanning word boundaries (bits
135/136/137) and the 127-bit wrap (bit 127 = bit 0 of the next period).
**675 of 675 corner×observer samples match the seeded sequence** at both
rates (0 mismatches; `bit_order_observers` in each summary).

## Measurement definitions, and the two load-bearing choices

- **E5 is graded on the differential transition.** With a quiet common mode,
  20–80 % of v(PADP)−v(PADN) *is* each pad's 20–80 % (pad thresholds at
  V_OS ± 0.3·V_OD are the same crossings). Under this schematic's E4 limit
  cycle a per-pad fixed threshold is ill-defined edge by edge — an individual
  pad can move against the data while the pair transitions, and the
  worst-case settled high can sit **below** the worst-case settled low
  (observed: PADP worst-high 1.16 V vs worst-low 1.45 V at nominal with a
  mis-phased strobe). Each card covers one boundary: a rising card is PADP
  rising and PADN falling simultaneously, and vice versa.
- **The normalization basis is the window extremes of the differential**
  (cannot invert at any corner). An eye-level basis was tried and rejected:
  its thresholds shrink with the achieved swing, so load changes stop moving
  the measured edge time and the E5 grader loses its load sensitivity — the
  negative control below is what exposed that. The cost of the extremes
  basis is the 12 unmeasured edges above, recorded as unmeasured rather
  than mis-normalized.
- **E9 width is graded per isolated-bit crossing gap** (nominal 1 UI,
  limit 0.75 / 0.60 UI): every bit's eye interval at 0 V differential is
  bounded by its adjacent zero crossings, so min-gap ≥ limit ⟹ every bit's
  eye width ≥ limit. Multi-bit run gaps carry ±0.25 UI guard windows
  instead of the spec limit; they also double as ringback detectors.
- **E9 height** is the worst 1-bit strobe sample minus the worst 0-bit
  strobe sample at the stated sampling phase — the worst-case vertical eye
  opening at that phase, not a best-bit figure.
- **E4 dynamic** is the peak-to-peak of (PADP+PADN)/2 over the settled
  window (time-windowed by `.meas FROM/TO`, not gated).
- **W1** is the time-weighted mean of −(i(VVCCD)·V(VCCD) +
  i(VVDDIO)·V(VDDIO)) over the window — per-rail current × that rail's own
  corner voltage, summed. The nominal-only legs (≤ 20 / ≤ 18 mW) are graded
  by the summaries from the tt/27C/1.80/3.30 row; the envelope grades only
  the any-condition ≤ 30 mW cap because one measurement cannot carry two
  corner-conditional limit sets.

## Checks run on the bench itself

### Negative control — the E5 grader detects a too-slow edge

At `tt/27C/1.80/3.30` on the 400 Mb/s stimulus, two steps in one job
(`klt-sim-e4bd8b0658d2`): the reference steps the load to **2 pF** per side
(at the spec's own 1 pF the nominal edge is ~89 ps, *below* the 100 ps lower
bound, so no 1 Gb/s-rate load demonstrates a passing reference at nominal),
the control raises **only the external capacitance** to 22 pF:

| Step | Load | E5 edges (64 cards) | Verdict |
|---|---|---|---|
| `ref` | 2 pF ‖ 100 Ω | 145 – 220 ps, **64 / 64 pass** | reference passes |
| `ctl` | 22 pF ‖ 100 Ω | 1484 – 2053 ps, **0 / 64 pass** | detected: every edge beyond the 1.0 ns upper limit |

The same grader, same corner, same pattern — only C<sub>LOAD</sub> changed.
(Raw-waveform cross-checks of both steps were taken before the fleet run;
the 22 pF edges are single monotone RC transitions at this rate, which is
why the fixture runs at 400 Mb/s: at 1 Gb/s a 10–22 pF load makes the
ringing dominate and the first-crossing definition stops reading a settling
edge at all.)

### Grid shape and self-checks

- `--dry-run` before each submit: `unit_count: 75`, one job of ≤ 75 units.
- Summaries reconcile **75 distinct tuples** per rate, both crossed pairs
  present (`grid.rail_pairs`).
- Bit-order observers: 675/675 correct per rate (above).
- Latency observer: 0.234 – 0.687 ns across the grid (both rates), which is
  the stated sampling phase's validity band.
- Sign checks: rail currents negative (sourcing), power positive, E4 window
  mean V_OS 1.2477 V at nominal against the 1.25 V target.
- The local single-corner nominal probe (the control's `ref` step at 2 pF,
  plus raw-waveform dumps at 1 pF) preceded every fleet submit; every
  request byte submitted is reproduced by the committed `gen_bench.py`
  invocations above.

## Prior attempts recorded, then discarded (kept honest here)

- Per-pad fixed-threshold E5: inverted levels under the CMFB cycle (see
  above) — replaced by the differential reading.
- Global rise/fall-count pairing: ngspice applies `td=` to the TRIG clause
  only on trig/targ cards, which silently mispairs events; replaced by
  per-edge `td`-scoped WHEN cards + expr differences.
- Eye-level E5 normalization: self-compressing under load changes; replaced
  by the window-extremes basis.
- 10 pF-at-1 Gb/s negative control: ringing-dominated, demonstrated nothing;
  replaced by the 400 Mb/s 2 pF → 22 pF fixture.

## Stated limitations of this grid

- **No Monte Carlo** (E4's statistical half, as above).
- **No serializer share in W1** (as above; total-power acceptance open).
- **The strobe phase is fixed**, chosen at nominal: at grid extremes the
  sample sits up to ~0.33 UI off the local eye centre. A per-corner optimal
  phase would read slightly larger eyes; the stated phase is the honest,
  reproducible one.
- **E5's edge set is per-boundary over the window**; at the eight
  CMFB-corrupted corners some pairings are anomalous (classified, listed)
  and 12 edges at 1 Gb/s never complete. No number from those corners is
  counted as a pass anywhere in this record.
- The `res_high_po_1p41` sense resistors remain typical at all 75 conditions
  (same `r+c/res_typical` inclusion as `driver-dc`; same caveat).
- Pre-emphasis disabled (`EM0` = `EM1` = 0): D3's enabled settings are not
  exercised; the pre-emphasis slices are present and off.

## Tool friction filed

Filed generically as
[`2AMLogic/klayout-tools#7068`](https://github.com/2AMLogic/klayout-tools/issues/7068)
for this bench: the eye/edge graders had to be hand-built from `.meas` cards
and `expr` reductions because `klt sim` has no sampled-reduction or
eye-measurement primitive; `td=` on trig/targ cards mispairs silently; and
`on_unreached` is unavailable for step-scoped cards (kept generic per the
friction protocol; design detail stays here).

The G75 grid itself again needed no new `klt` capability beyond
`analysis_steps` (runner-supported on this fleet): `corners.supply_v`
index-zips the pairs, `save_vectors` keeps the transient's saved set small,
and `batch.capacity_wait_s` covered the fleet burst.
