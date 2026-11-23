# Powered driver transient record

The schematic misses the proposed 1 Gb/s target and the 400 Mb/s fallback. These are **simulated** results over G75. The proposed spec awaits ratification, E4 still needs its Monte Carlo evidence, and W1 still needs the serializer contribution. T1 item 5 remains open.

## Results

The results below come from grading the corrected batch reports for per-pad E5 and folded E9. Each rate covers the 75 process, temperature and paired-rail tuples in the DC request, including both crossed supplies. The control runs at a separate corner outside those totals. [1 Gb/s fleet summary](results/r2/fleet-attempt/summary-1g.json) · [400 Mb/s fleet summary](results/r2/fleet-attempt/summary-400m.json) · [Control fleet summary](results/r2/fleet-attempt/summary-control.json)

| Binding limit | 1 Gb/s value (signed margin), corner | 400 Mb/s value (signed margin), corner |
|---|---|---|
| E5 100 ps minimum | 0.10 ps (-99.90) at `sf/-40C/1.62/3.63`, PADP bit 145 | 0.10 ps (-99.90) at `tt/-40C/1.62/3.63`, PADP bit 223 |
| E5 maximum (400 ps / 1 ns) | 662.50 ps (-262.50) at `ss/125C/1.62/2.97`, PADN bit 228 | 2197.40 ps (-1197.40) at `ff/-40C/1.98/3.63`, PADP bit 239 |
| E9 height minimum (150 / 120 mV) | 101.16 mV (-48.84) at `sf/-40C/1.62/2.97` | 103.81 mV (-16.19) at `sf/-40C/1.62/2.97` |
| E9 width minimum (0.75 / 1.50 ns) | 0.9083 ns (+0.1583) at `sf/-40C/1.62/2.97` | 2.4023 ns (+0.9023) at `sf/-40C/1.62/2.97` |
| E4 dynamic maximum (150 mV) | 1668.39 mV (-1518.39) at `sf/-40C/1.62/2.97` | 1666.97 mV (-1516.97) at `sf/-40C/1.62/2.97` |
| W1 subtotal, 30 mW at any corner | 14.40 mW (+15.60) at `ff/27C/1.98/3.63` | No applicable limit |
| W1 subtotal, 20 / 18 mW at nominal TT | 12.44 mW (+7.56) at `tt/27C/1.80/3.30` | 12.18 mW (+5.82) at `tt/27C/1.80/3.30` |

| Measure | 1 Gb/s | 400 Mb/s |
|---|---:|---:|
| E5 conditions passing all 128 pad edges | 0 / 75 | 0 / 75 |
| E5 edges in band | 3331 | 3071 |
| E5 edges below 100 ps | 5180 | 3636 |
| E5 edges above the maximum | 475 | 1538 |
| E5 edges unmeasurable | 614 | 1355 |
| E9 height passes | 73 / 75 | 73 / 75 |
| E9 folded width passes | 75 / 75 | 75 / 75 |
| E4 dynamic passes | 0 / 75 | 0 / 75 |
| E9 conditions passing both limits | 73 / 75 | 73 / 75 |
| W1 total power unverified | 75 / 75 | 75 / 75 |

Each rate has 9,600 expected E5 pad edges. The nine PRBS observers matched the expected bits at all 675 corner/sample combinations per rate. The 0.10 ps E5 minimum at 1 Gb/s comes from an interpolated crossing of a 0.264 mV local PADP excursion. The timestamps and endpoint levels identify this near-flat bit. The E4 excursion exceeds the 150 mV cap at every corner. The folded eye height is weakest at the low-core, low-I/O, cold SF corner at both rates.

## What was measured

One instance of `design/lvds_tx_analog.spice` includes both DDR muxes, predriver, driver with CMFB and both pad cells. The netlist at `e27999f` has SHA-256 `b90b61fd221bb1d46e3a4aad0b670331218d43be473d03a08ab84e86af19d28f`. The schematic predates the sizing work in #166. The design load is 100 Ω across the pair and 1.0 pF from each pad to ground. The ideal stimulus, load and references follow DR-007. IREF is 54.3 µA, VCMREF is 1.25 V, EN tracks VCCD and pre-emphasis is off, as in the [driver DC bench](../driver-dc/RECORD.md).

The PRBS-7 sequence uses x⁷ + x⁶ + 1 and seed `0x01`. Bit 0 launches at one unit interval (UI). Even bits use D0 on rising clock edges and odd bits use D1 on falling edges. After settling, bits 127–253 span one full period with 64 transitions. The UI is 1 ns or 2.5 ns. The fixed sampling time for bit *i* is `(i + 1.5) × UI + 360 ps`. The nominal chain latency sets the 360 ps offset. Nine signed differential samples per corner check the seeded sequence across word boundaries and the wrap.

- **E5** measures PADP and PADN independently. Each pad's voltages at the assigned launch and the following launch define its local starting and ending levels. The first 20% and 80% crossings must occur in order within that interval, with the expected polarity. The report retains the endpoint voltages and timestamps. A reversed excursion or unavailable crossing is an unmeasurable edge. The duration describes the achieved local swing and has to be interpreted with the eye height.
- **E9 width** uses every settled sign change of PADP − PADN, including recrossings. The grader linearly interpolates each zero between adjacent solver samples, then folds the crossing time modulo one UI relative to the launch clock. The common opening is `UI × (1 − latest_phase + earliest_phase)`. Each expected PRBS transition also needs a directed crossing within its assigned bit. The only width limits are the proposed minima of 0.75 ns and 1.50 ns.
- **E9 height** is the lowest differential one level minus the highest differential zero level over all 127 sample strobes. Each strobe has a 4 ps flat top and 0.5 ps ramps. The height minima are 150 and 120 mV.
- **E4 dynamic** measures the peak-to-peak value of (PADP + PADN)/2 over the settled period. The 150 mV cap applies at both rates. The DC bench covers static behavior. The local-mismatch Monte Carlo run is outstanding.
- **W1** reports the time average of −(I(VVCCD) × VCCD + I(VVDDIO) × VDDIO). The analog subtotal is available at every corner. At 1 Gb/s it is compared with 30 mW everywhere and 20 mW at nominal TT. At 400 Mb/s only nominal TT has a limit, 18 mW. Total lane power is marked `unverified` at every condition. The serializer estimate in `flow/serializer/sta.response.json` uses engine-default activity; a serializer contribution at matching activity, rate and core corner is outstanding.

The summaries enumerate the requested cards for each expected step and corner. A row passes only when every required measure is present and passes. A known violation yields a failed row, with missing counts also retained. With no known violation, an incomplete row is marked missing. Binding corners minimize the signed margin separately for each limit, in the quantity's own unit. For a lower limit the margin is value minus limit. For an upper limit it is limit minus value.

## Negative control

At nominal TT and 400 Mb/s the reference uses 2 pF per pad. The control increases only that capacitance to 22 pF. Detection requires the same bit on the same pad to move from inside 100–1000 ps to above 1000 ps, on both pads. The 2 pF reference itself has misses, so the comparison is paired by edge.

| Step | In band | Below 100 ps | Above 1 ns | Unmeasurable |
|---|---:|---:|---:|---:|
| Reference, 2 pF | 66 | 47 | 10 | 5 |
| Control, 22 pF | 12 | 0 | 116 | 0 |

**58 paired edges detect the load change**, 30 on PADP and 28 on PADN. For bit 139, PADP rise goes from 163.9 to 1084.8 ps and PADN fall goes from 112.2 to 1002.1 ps. The control summary lists all 58 edge IDs. [Fleet control report](results/r2/fleet-attempt/report-control.json.gz)

## Reproduction

The fleet and local r2 reports use ngspice 47 and record client klayout `0.30.12`. The fleet reports identify klt client `0.9.3.dev2586+g9bac82596e2f` and runner `0.9.0`. The local comparison reports identify klt `0.9.3.dev2575+g6bd18bbc8637`. The pinned sky130A PDK is open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7`. Its `sky130.lib.spice` has SHA-256 `17c208a699228f5acb87bf59c09c22a4c4d3937b6766b4957737d34e8e075f64`. The requests use `set wnflag=1` and one ngspice thread. The sense-resistor models remain typical across G75. [Target spec](../../spec/target-spec.md)

Run from the repository root in Bash with `PDK_ROOT` pointing to the pinned ciel root. The generator writes to its current directory. The commands below keep simulation outputs in a fresh directory. The two grids use the local-parallel backend and the control uses local. Klt exits 3 for a spec miss and can exit 4 when a required measurement is unavailable. Both outcomes produce a report for inspection.

```bash
cd sim/driver-tran
python3 gen_bench.py --rate 1g --sample-phase-ps 360
python3 gen_bench.py --rate 400m --sample-phase-ps 360
out=$(mktemp -d)
for run in 1g 400m control; do
    options=(--backend local-parallel --max-workers 6)
    rate=$run
    label=$run
    if [[ $run == control ]]; then
        options=(--backend local)
        rate=400m
        label=400m-control
    fi
    rc=0
    klt sim "request-$run.json" "${options[@]}" -o "$out/$run" \
        --report-out "$out/report-$run.json.gz" --format json > /dev/null || rc=$?
    [[ $rc == 0 || $rc == 3 || $rc == 4 ]] || exit "$rc"
    python3 summarize.py "$out/report-$run.json.gz" "stim_meta_$rate.json" \
        "$label" "$out/summary-$run.json"
done
python3 -m unittest discover
```

For a fleet rerun, use `--backend batch --wait-for-capacity 600` in place of the local options. First dry-run each request with `--backend batch --dry-run` and check the expansions of 75, 75 and 1 units.

### Fleet evidence for the corrected requests

All three receipts record `failed` and the reports record `error` (runner exit 4). Within those reports each of the 152 analysis steps records `ok`. The grader uses the returned values and lists each missing measurement by corner and step. The runner diagnostic `expr_runner_may_predate` names expressions with missing values. The two design reports still provide 8,986 and 8,245 measurable pad edges respectively and a folded width at every corner. The control provides 58 matched pass-to-slow edges. [Runner diagnostic report](https://github.com/2AMLogic/klayout-tools/issues/7113)

| Request | Fleet job and receipt | Report | Request SHA-256 prefix | Steps with status `ok` | Missing measurements |
|---|---|---|---|---:|---:|
| 1 Gb/s | [`klt-sim-4df82c75d805`](results/r2/fleet-attempt/batch-receipt-1g.json) | [report](results/r2/fleet-attempt/report-1g.json.gz) | `eb705e41` | 75 | 621 |
| 400 Mb/s | [`klt-sim-1f98a90710b4`](results/r2/fleet-attempt/batch-receipt-400m.json) | [report](results/r2/fleet-attempt/report-400m.json.gz) | `63890e5d` | 75 | 1,373 |
| Control | [`klt-sim-3c3a4015e044`](results/r2/fleet-attempt/batch-receipt-control.json) | [report](results/r2/fleet-attempt/report-control.json.gz) | `3b267611` | 2 | 5 |

Each receipt's job ID matches `environment.remote.job_id` in its report. Its full SHA-256 matches the current request after dropping the top-level `batch` object and serializing sorted keys with compact JSON separators. Both rate reports cover the exact 75 tuples in the DC request. Running the grader on the three fleet reports reproduces every field of the corresponding local summary except `backend`. [1 Gb/s local summary](results/r2/summary-1g.json) · [400 Mb/s local summary](results/r2/summary-400m.json) · [Local control summary](results/r2/control/summary.json)

Run the following in `sim/driver-tran/` to reproduce the fleet summaries from the committed reports.

```bash
fleet=results/r2/fleet-attempt
out=$(mktemp -d)
for run in 1g 400m control; do
    rate=$run
    label=$run
    if [[ $run == control ]]; then rate=400m; label=400m-control; fi
    python3 summarize.py "$fleet/report-$run.json.gz" "stim_meta_$rate.json" \
        "$label" "$out/summary-$run.json"
    cmp "$out/summary-$run.json" "$fleet/summary-$run.json" || exit 1
done
```

## Nominal waveform check and eye

Both nominal captures use TT, 27 °C, 1.8 V and 3.3 V, with the same netlist, stimulus and pinned models as the grids. At each rate, `request-wave-{1g,400m}.json` saves the mux outputs `v(xtx.q)` and `v(xtx.qb)` along with the pads. The committed waveforms were produced locally with ngspice 47 and klt `0.9.2.dev111+g978f7464fae1`. The separate `request-nominal-{1g,400m}.json` observer requests read PADP − PADN through 11 measurement cards, adding bits 126 and 254 to the nine observed across G75.

`eye_plot.py` interpolates Q − QB at the specified sample time for each of bits 126–254 and compares its sign with the seeded PRBS-7 bit. It records the mux voltage and match alongside the downstream PADP − PADN voltage and match. Both signals match all 129 expected bits at each rate, including the word boundary at bits 127/128 and the sequence wrap at bits 253/254. The two-UI eye folds PADP − PADN over bits 127–252 and marks the sampling phase.

| Rate | Bit-order check | Folded eye (**simulated**) | Raw waveform |
|---|---|---|---|
| 1 Gb/s | [11 observers](results/r2/nominal/bit-order-report-1g.json.gz), [129 mux and pad samples](results/r2/nominal/bit-order-1g.json) | [eye-1g.svg](results/r2/nominal/eye-1g.svg) | [waveform](results/r2/nominal/waveform-1g.json.gz) |
| 400 Mb/s | [11 observers](results/r2/nominal/bit-order-report-400m.json.gz), [129 mux and pad samples](results/r2/nominal/bit-order-400m.json) | [eye-400m.svg](results/r2/nominal/eye-400m.svg) | [waveform](results/r2/nominal/waveform-400m.json.gz) |

```bash
cd sim/driver-tran
for r in 1g 400m; do
    klt sim request-wave-$r.json --backend local -o "$out/wave-$r" --format json > /dev/null || true
    klt sim request-nominal-$r.json --backend local -o "$out/nom-$r" \
        --report-out "$out/nom-$r/report.json.gz" --format json > /dev/null || true
    python3 eye_plot.py "$out"/wave-$r/tt_*/waveform.raw.json "stim_meta_$r.json" \
        "$out/eye-$r.svg" "$out/bit-order-$r.json"
done
```

(Klt exits 4 for the measurement-less waveform request and 3 or 4 for a spec miss; each still writes its output.)

## Earlier fleet evidence

The original reports, summaries and receipts remain under `results/` and `results/control/`. They used differential E5 crossings and isolated-pulse gaps. Use r2 for per-pad E5, folded E9, signed margins and W1 applicability. Across all 150 conditions, the original fleet values for height, common-mode excursion and analog power agree with r2 to the reports’ printed precision. Independently reconstructing the phase spread from the original differential crossing gaps agrees with the r2 folded width within 0.000004 UI at every corner. The original reports contain no per-pad edge timestamps. The three original job IDs were `klt-sim-c99eee14c6df` (1 Gb/s), `klt-sim-cdc1aae98ed2` (400 Mb/s) and `klt-sim-e4bd8b0658d2` (control).

The submit-only receipt hashes the parsed request after removing submission-only fields from `batch` and retaining the resulting empty object. Klt serializes sorted JSON keys with compact separators and hashes the UTF-8 bytes with SHA-256. From the repository root, the following compares each original request at the reviewed commit with its receipt.

```bash
python3 - <<'PY'
import hashlib, json, subprocess
from pathlib import Path

bench = Path("sim/driver-tran")
for run in ("1g", "400m", "control"):
    path = bench / f"request-{run}.json"
    request = json.loads(subprocess.check_output(["git", "show", f"6d2bf91:{path}"]))
    for field in ("capacity_wait_s", "max_concurrent_jobs"):
        request["batch"].pop(field, None)
    canonical = json.dumps(request, sort_keys=True, separators=(",", ":")).encode()
    digest = hashlib.sha256(canonical).hexdigest()
    receipt = ("control/batch-receipt.json" if run == "control"
               else f"batch-receipt-{run}.json")
    assert digest == json.loads((bench / "results" / receipt).read_text())["request_sha256"]
    print(run, digest)
PY
```

The matching prefixes are `7da33cac`, `8a20385a` and `0b97ead6`. The upstream issue records the klt eye-measurement and step-card limitations observed while developing this bench. [klayout-tools #7068](https://github.com/2AMLogic/klayout-tools/issues/7068)

## Isolation-gate paired run (r3, issue #179)

These are **simulated** paired results measuring the DR-010 floating-well transmission gates' effect on the loaded pad eye at 1 Gb/s over the same 75 G75 conditions. The **before** leg is the #168 fleet run above unchanged: netlist `e27999f`, SHA-256 `b90b61fd221bb1d46e3a4aad0b670331218d43be473d03a08ab84e86af19d28f`. The **after** leg is commit `45ebd2d3` (branch `feature/issue-167`, PR #175), whose `design/lvds_tx_analog.spice` has SHA-256 `1885eec576235f7be805b403ae0d6ff5b3bd8d0aa50ba89a4c579e122c601032`. Both legs share one bench: request `eb705e41…` (hash-verified against the #168 receipt), the same PRBS-7 stimulus, 100 Ω across the pads, 1.0 pF per side, IREF 54.3 µA, VCMREF 1.25 V and the 360 ps sample phase. The #166 driver sizing is **not** applied to either leg; both stay at the pre-#166 sizing, as the issue's dependencies require. Each rate has 9,600 expected E5 pad edges; the nine PRBS observers matched the expected bits at all 675 corner/sample combinations in the after leg too. No simulation failed, so no condition is inconclusive; unmeasurable edges (614 before, 629 after) leave their per-edge delta unreported by design.

| Measure (1 Gb/s, fixed 360 ps phase) | Before, `e27999f` | After, `45ebd2d3` | Signed change |
|---|---:|---:|---:|
| E5 conditions passing all 128 pad edges | 0 / 75 | 17 / 75 | +17 |
| E5 edges in band (100–400 ps) | 3331 | 7285 | +3954 |
| E5 edges below 100 ps | 5180 | 1212 | −3968 |
| E5 edges above 400 ps | 475 | 474 | −1 |
| E5 edges unmeasurable | 614 | 629 | +15 |
| E9 height passes (≥ 150 mV) | 73 / 75 | 72 / 75 | −1 |
| E9 height minimum | 101.16 mV at `sf/-40C/1.62/2.97` | −7.29 mV at `ss/-40C/1.62/2.97` | worst −493.06 mV at `ss/-40C/1.62/3.63` |
| E9 width passes (≥ 750 ps) | 75 / 75 | 75 / 75 | 0 |
| E9 width minimum | 908.3 ps at `sf/-40C/1.62/2.97` | 774.9 ps at `sf/-40C/1.62/2.97` | −133.4 ps at `sf/-40C/1.62/2.97` |
| Median E5 edge delta (8746 edges in both) | — | — | +53.2 ps (7611 slower, 1134 faster) |

The isolation gates turn most of the before leg's sub-100 ps near-flat excursions into in-band edges: 4338 edges recover into the band against 384 new out-of-band misses (158 too fast, 136 too slow, 90 becoming unmeasurable), and 240 previously measurable edges became unmeasurable while 225 newly resolved. The remaining 1264 out-of-band edges already missed before isolation. The slowest new edge is `m_e5_pr151` at `ss/-40C/1.62/2.97`, +619.6 ps; the fastest change is `m_e5_pf183` at `ff/-40C/1.98/3.63`, −535.9 ps. The before leg's E5 misses at every condition were an absolute failure of the 100 ps floor; isolation converts that row from 0/75 to 17/75 passing and shifts the binding edge from 0.10 ps to 0.20 ps (`ff/-40C/1.62/3.63`, `m_e5_nf139`), while the 400 ps ceiling is essentially unchanged (723.2 ps at `ss/125C/1.62/3.63`, `m_e5_pf222`, was 662.5 ps before).

**Eye height is the penalty.** The folded-eye nominal centre moves from 854.5 ps to 908.6 ps after the launch edge (+54.1 ps of chain latency), so the frozen 360 ps convention samples the after netlist off-centre at slow corners. A second after run at the re-centred 409 ps phase ([re-phased leg](results/r3-isolation/rephase-409ps/), labelled separately) reopens the worst corner from −7.29 mV to +88.96 mV, confirming the fixed-phase closure at `ss/-40C/1.62/2.97` is mostly sampling phase — but the re-centred value still misses the 150 mV floor where the before leg passed with 168.66 mV. That one corner is therefore a **measured penalty that became an absolute miss**: even sampled at its own eye centre the isolated driver loses more than half its eye at `ss` with low core and I/O rails at −40 °C (before 168.66 mV → after 88.96 mV). The other two height misses (`sf/-40C/1.62/2.97` at 102.77 mV and `sf/-40C/1.98/2.97` at 106.19 mV, re-phased values) already missed before isolation (101.16 and 108.57 mV) and are pre-existing. E9 width passes at every condition in both legs, but its margin at `sf/-40C/1.62/2.97` shrinks from +158.3 to +24.9 ps; width is crossing-based and identical to the reports' printed precision in the re-phased run (≤ 2.9 fs solver-timestep drift from the moved strobe PWL across 37 of 75 conditions), while all E5 edge categories and per-condition counts are identical (≤ 0.2 ps edge-duration drift across 285 of 9,600 edges).

Per-condition absolute values, signed deltas, edge transitions and both legs' binding corners are enumerated in the [paired comparison](results/r3-isolation/comparison.json) ([re-phased](results/r3-isolation/rephase-409ps/comparison.json)); [after summary](results/r3-isolation/summary-1g.json); [fleet receipts](results/r3-isolation/batch-receipt-1g.json) job `klt-sim-23c387e2a2b9` and `klt-sim-a9eacf891cfa`, 75 units each, request hashes `eb705e41…` (fixed phase) and `37ef1864…` (re-phased). The runner again records `error` overall (runner exit 4) with all 150 analysis steps `ok`, exactly as the #168 fleet runs do.

```bash
# after leg, fixed 360 ps phase (design/ at 45ebd2d3, bench at this revision)
klt sim request-1g.json --backend batch --wait-for-capacity 600 \
    -o out-1g --report-out out-1g/report-1g.json.gz --format json || rc=$?
[[ $rc == 0 || $rc == 3 || $rc == 4 ]] || exit $rc
python3 summarize.py out-1g/report-1g.json.gz stim_meta_1g.json 1g summary-1g.json
# re-phased leg: python3 gen_bench.py --rate 1g --sample-phase-ps 409, then the same run
python3 compare_isolation.py results/r2/fleet-attempt/report-1g.json.gz \
    results/r3-isolation/report-1g.json.gz results/r3-isolation/comparison.json
python3 compare_isolation.py results/r2/fleet-attempt/report-1g.json.gz \
    results/r3-isolation/rephase-409ps/report-1g.json.gz \
    results/r3-isolation/rephase-409ps/comparison.json \
    --request results/r3-isolation/rephase-409ps/request-1g.json \
    --meta results/r3-isolation/rephase-409ps/stim_meta_1g.json \
    --after-label after_409ps \
    --after-desc "results/r3-isolation/rephase-409ps/report-1g.json.gz (isolation commit 45ebd2d3, sample phase re-centred to 409 ps)"
```
