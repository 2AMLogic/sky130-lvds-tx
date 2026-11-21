# Powered driver transient record

The schematic misses the proposed 1 Gb/s target and the 400 Mb/s fallback. These are **simulated** results over G75. The proposed spec awaits ratification, E4 still needs its Monte Carlo evidence, and W1 still needs the serializer contribution. T1 item 5 remains open.

## Results

The current reports use the corrected per-pad and folded-eye graders. Each rate covers the 75 process, temperature and paired-rail tuples in the DC request, including both crossed supplies. The control runs at a separate corner outside those totals. [1 Gb/s summary](results/r2/summary-1g.json) · [400 Mb/s summary](results/r2/summary-400m.json) · [Control summary](results/r2/control/summary.json)

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

**58 paired edges detect the load change**, 30 on PADP and 28 on PADN. For bit 139, PADP rise goes from 163.9 to 1084.8 ps and PADN fall goes from 112.2 to 1002.1 ps. The control summary lists all 58 edge IDs. [Control report](results/r2/control/report.json.gz)

## Reproduction

The r2 reports were produced with ngspice 47, klt `0.9.3.dev2575+g6bd18bbc8637` and klayout `0.30.12`. The pinned sky130A PDK is open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7`. Its `sky130.lib.spice` has SHA-256 `17c208a699228f5acb87bf59c09c22a4c4d3937b6766b4957737d34e8e075f64`. The requests use `set wnflag=1` and one ngspice thread. The sense-resistor models remain typical across G75. [Target spec](../../spec/target-spec.md)

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

For a fleet rerun, use `--backend batch --wait-for-capacity 600` in place of the local options. First dry-run each request with `--backend batch --dry-run` and check the expansions of 75, 75 and 1 units. Then retain each collected job's receipt and report. On the host that produced r2, submission stopped before upload because the AWS profile `batch-runner-submit` was unavailable. The corrected runs have local provenance. [1 Gb/s report](results/r2/report-1g.json.gz) · [400 Mb/s report](results/r2/report-400m.json.gz)

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
