# Driver DC bench — V_OD and V_OS record

**Simulated, not measured.** No silicon exists. Every number below is an ngspice
operating point on the committed `driver` netlist, against a **PROPOSED** spec
(`spec/target-spec.md` is a proposal, not a ratified datasheet). The external
bias and reference sources are **ideal**, as `DR-007` requires every ideal
source to be labelled.

**This bench closes no spec row.** E1–E4 are *statistical* rows: the spec
requires G75 **plus** a local-mismatch Monte Carlo (`spec/target-spec.md`
§"Rows marked statistical"). The Monte Carlo is out of scope here, and E4's
second half — the dynamic peak-to-peak `V_OS(PP)` under PRBS-7 — is a transient
quantity also out of scope. What follows is the deterministic half of the
evidence for E1, E2, E3 and the DC half of E4, and nothing more.

**It changes no device size, bias or schematic.** `IREF` was derived once and
then frozen, so a failing condition is recorded as a miss rather than tuned
away. Sizing closure is the follow-up that starts from this record.

## Headline

**51 of the 75 conditions pass every row. 24 miss at least one.**
No condition errored and none was graded inconclusive.

Those 24 any-miss conditions, by process: `ss` 8, `fs` 7, `sf` 5, `tt` 4,
`ff` 0. This is the *any-miss* distribution — a condition counts here for
missing any row, so it is not a per-row count. `fs` is second on this list
almost entirely through E2 (7 of its 7 any-misses miss the V_OS window, 2 miss
E1), which is why the per-row breakdowns below are the ones to size against.

| Spec row | What it grades | Limits | Conditions passing |
|---|---|---|---:|
| E1 | V_OD, both data states | 247–454 mV | **60 / 75** |
| E2 | V_OS, TIA/EIA-644 window | 1.125–1.375 V | **62 / 75** |
| E2/D2 | V_OS, regulation band (1.25 V ± 75 mV) | 1.175–1.325 V | **62 / 75** |
| E3 | ΔV_OD between complementary states | ≤ 50 mV | 75 / 75 |
| E4 (DC half) | ΔV_OS between complementary states | ≤ 50 mV | 75 / 75 |

Observed ranges over the grid: V_OD **117.1 – 368.3 mV**, V_OS
**1.2471 – 2.5929 V**, |ΔV_OD| ≤ 0.014 mV, |ΔV_OS| ≤ 0.059 mV.

### Read E3 and E4 with care — they pass for a structural reason

ΔV_OD and ΔV_OS are ≈ 0 (tens of nV to tens of µV) at **every** condition, far
inside the 50 mV budget. That is not evidence of a good design: in a
deterministic, perfectly-matched deck the two data states are exact mirror
images of each other, so their difference is zero by construction and the
residual is solver noise. The 50 mV budget in E3/E4 exists to cover **device
mismatch and layout asymmetry**, neither of which this bench contains. The
informative part of those two rows is the Monte Carlo that is out of scope here.
**Do not read 75/75 as E3/E4 being met.**

## Provenance

| Field | Value |
|---|---|
| Repo base commit | `d7da34a8c017a4fedbe845816668cdb4bbf5653a` (inputs below are content-hashed) |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (ciel 2.6.1; `docs/environment.md`) |
| Model library sha256 | `17c208a699228f5acb87bf59c09c22a4c4d3937b6766b4957737d34e8e075f64` (`sky130.lib.spice`) |
| Testbench sha256 | `4e747a4881b55aa6c36433519f7e14a43312caa3a76ac4e5f24d41d4d428b6d1` (`driver_dc.spice`) |
| DUT netlist sha256 | `5f008c909faf1fe3d3cc5dd43a9146fa5db9a7cf605634fbf37f912075959137` (`design/driver/driver.spice`, `.include`d, not copied) |
| Client | `klt 0.9.2.dev1022+g2a9c52b27ce7`, klayout 0.30.13 |
| Engine | ngspice 47 on the batch worker, binary sha256 `39ca1adb826660324c3626f72bd946ec40704f0f3fc8e243c623f76e24b3eee2` (byte-identical to this host's) |
| ngspice init | `set wnflag=1`, `set num_threads=1`, declared in the request (`options.ngspice_init`) — **load-bearing, see "The wnflag trap"** |
| Backend | `batch`, job `klt-sim-b415b94ced6d`, 75 units, `options.stage_model_inputs: true` (319 model files staged) |

The committed `driver_dc.spice` hashes to `00389d012205c88b81bb2c0d6161b4e2720974c943026002addcb60adaa86556`:
after this grid was recorded, its header comment was reworded (the pad-cell
defect it described is fixed — see "Why the pad cell is not in the deck" below;
PR #102). Comment lines only; the circuit body is byte-identical, so the run is
exactly reproducible from the committed deck. The table row above identifies the
deck **as run**.

Reproduce:

```console
PDK_ROOT=<pinned ciel root> klt sim sim/driver-dc/request.json \
    --backend batch --wait-for-capacity 600 \
    --report-out sim/driver-dc/results/report.json
```

Results: `results/summary.json` (per-condition values and per-row pass flags)
and `results/report.json.gz` (the full `klt sim` report, committed verbatim).

## What ran

One `klt sim` request (`request.json`), `analysis.kind: "op"`, over the **G75**
grid `spec/target-spec.md` §"The PVT grid" ratifies: process `tt, ff, ss, sf,
fs` × temperature −40, 27, 125 °C × the five (VCCD, VDDIO) pairs
{(1.62, 2.97), (1.80, 3.30), (1.98, 3.63), (1.62, 3.63), (1.98, 2.97)} V = 75
conditions. The supply pairs move **as a set** (one axis, not a cross product),
which is what `corners.supply_v`'s index-zipping gives.

`driver_dc.spice` holds **two** `driver` instances that share the rails and the
reference values — one per static data state — each with its own 100 Ω
differential load. Both states therefore sit in the *same* operating point, so
ΔV_OD and ΔV_OS are single expressions evaluated at one condition rather than a
join across two corner records, which is what E3 and E4's "same condition"
wording requires.

An `op` analysis has no sweep for a `.meas` card to search, so all eight
quantities are declared as `measurements[].expr` and graded by `klt` against
`limits` per condition.

## Stimulus, and why each value

Every quantity the spec does not fix:

| Stimulus | Value | Why |
|---|---|---|
| VCCD, VDDIO | the five G75 pairs, via `corners.supply_v` keyed by the source names `VVCCD`/`VVDDIO` | the spec grid |
| `IREF` | **54.3 µA**, forced into each instance's diode-connected `XMNB1`, frozen across all 75 | derived once; see below |
| `VCMREF` | **1.25 V** at every condition | E2's regulation target is 1.25 V, the centre of the TIA/EIA-644 window (`DR-002` §3). An **ideal** external reference |
| `EN` | VCCD | driver enabled: `SEL` high → `ENH` high → `XMPP`/`XMNP` pass `BIASP`/`VCMFB` to the slice's `PG`/`NG` |
| `EM0`, `EM1` | **0 V** | pre-emphasis disabled: `SEL` low → `XMPU` pulls `PG` to VDDIO and `XMND` pulls `NG` to VSSIO, so all three pre-emphasis slices are off |
| `GPA`/`GNA` (side A), `GPB`/`GNB` (side B) | 0 V and VCCD, complementary between sides; state 1 is A = 0 V, B = VCCD | the predriver's final stage per side is a rail-to-rail CMOS inverter on VCCD/VSSIO driving **both** gates of that side from one node, so these are exactly the static levels it delivers — and they track the swept rail with no extra source |
| `XPA`/`XPB`/`XNA`/`XNB` | the same static pattern as the main slice | keeps the three disabled pre-emphasis slices' switch nodes defined (E8: one switch of each pair is always on) |
| Load | 100 Ω differential, one per instance | the Electrical section preamble |

### How `IREF` was chosen, once

The bias mirror is `XMPB` (`pfet_g5v0d10v5`, W = 2, L = 1, m = 1) → `XMPS`
(W = 12.8, L = 1, `m = 11` via `SCALE=11`), an effective width ratio of
12.8 × 11 / 2 = **70.4**, so the 3.5 mA design-nominal tail wants roughly
50 µA. The value was then pinned empirically by a **single-corner local probe**
at `tt`/27 °C/1.80 V/3.30 V, as the 0.1 µA step whose V_OD lands on E1's 350 mV
design nominal:

| `IREF` | V_OD at tt/27 °C/1.80 V/3.30 V |
|---|---|
| 53.6 µA | 346.20 mV |
| 53.9 µA | 347.82 mV |
| 54.3 µA | **349.98 mV** ← chosen |
| 54.4 µA | 350.52 mV |

**54.3 µA is then frozen at all 75 conditions.** The spec fixes the nominal
V_OD, not the bias current, and freezing the bias is what keeps a failing corner
a recorded miss instead of a tuned-away one.

One source **per instance** at the same value, not one shared source: a single
shared current source would divide its current between the two instances'
`XMNB1` devices and bias each at half the intended value. (`VCMREF` is a
voltage, so it *is* shared.)

## Where the misses are, and what they look like

### E1 — V_OD below 247 mV at 15 conditions

12 of the 15 E1 misses are at **VDDIO = 2.97 V**, the low end of the I/O rail:

| VDDIO | E1 misses |
|---|---:|
| 2.97 V | 12 |
| 3.63 V | 2 |
| 3.30 V | 1 |

The tail current source `XMPS` sits on VDDIO, so this reads as a **headroom**
limit on the I/O rail rather than a core-rail or bias effect — at 2.97 V the
source and the stacked switches cannot hold the current that 100 Ω needs for
247 mV. The worst condition is `sf`/−40 °C/1.98 V/2.97 V at **117.1 mV**, less
than half the lower limit. By process: `ss` 6, `sf` 5, `tt` 2, `fs` 2, `ff` 0 —
`ff` passes E1 everywhere.

### E2 — V_OS above 1.375 V at 13 conditions

**Every** E2 miss is V_OS *too high*; not one condition sits below the window.
10 of 13 are at **VCCD = 1.62 V** and 9 of 13 at **125 °C**:

| Axis | E2 misses |
|---|---|
| VCCD | 1.62 V: 10, 1.80 V: 2, 1.98 V: 1 |
| Temperature | 125 °C: 9, 27 °C: 3, −40 °C: 1 |

The common-mode feedback pulls V_OS *down* by driving the NMOS sink gate
(`VCMFB` → `NG` → `XMNS`), and its drive is bounded by VCCD. So a low core rail
plus high temperature is where the loop runs out of authority. The worst is
`fs`/125 °C/1.62 V/3.63 V at **2.5929 V** — 1.22 V above the window and 1.34 V
above the 1.25 V target. The negative-control check below confirms the loop is
regulating where it can.

**The regulation band added no distinct information on this run.** It was given
its own measurement name so a ±75 mV band miss would stay distinguishable from a
±125 mV window miss, but there were **zero** band-only misses: every V_OS miss
is large enough to break the wider window too. The separate measurement is kept
for future runs, where a marginal condition is the likely case.

### An observation outside this bench's rows: V_OS above the thin-oxide rating

At three conditions V_OS exceeds **1.98 V**, the ceiling E8 sets for every
thin-oxide terminal pair in any powered state:

| Condition | V_OS |
|---|---:|
| `fs`/125 °C/1.62 V/3.63 V | 2.593 V |
| `ss`/125 °C/1.62 V/3.63 V | 2.342 V |
| `fs`/125 °C/1.62 V/2.97 V | 2.162 V |

This bench does **not** measure E8 and this is not an E8 verdict — E8 is a
per-device stress check, and the switches are `pfet_01v8`/`nfet_01v8`
thin-oxide devices whose terminal pairs are not evaluated here. It is recorded
because the common mode is the node those switches hang from, so a 2.59 V common
mode is a device-stress question the sizing follow-up has to answer, not just a
specification miss.

## Checks run on the bench itself

### Negative control — the bench measures what it claims

`VCMREF` moved off 1.25 V at a single local corner (`tt`/27 °C/1.80 V/3.30 V),
everything else unchanged:

| `VCMREF` | V_OS measured | Graded |
|---|---|---|
| 1.25 V | 1.2537 V | pass |
| 1.35 V | 1.3549 V | fail (regulation band) |

V_OS tracks the reference 1:1 (+101.2 mV for +100 mV), so `v_os_*` is reading
the regulated common mode and not an artefact — and the tighter band correctly
graded the 1.35 V case as a miss.

### Operating-point lint

`klt sim --op-lint` was run at three conditions — `tt`/27 °C/1.80 V/3.30 V and
the two extreme conditions the spec names for statistical rows,
`ss`/125 °C/1.62 V/2.97 V and `ff`/−40 °C/1.98 V/3.63 V. (Not all 75: linting
the whole grid locally would be a local corner grid, which this host's rules
send to the fleet instead.) Findings at the nominal condition, all accounted
for:

| Check | Count | What they are |
|---|---:|---|
| `off` | 100 | 60 in the three deliberately disabled pre-emphasis slices, 12 in their bias selects, 12 in the enable-path level shifter (a static latch has off devices by construction), 16 in the main slice — the un-selected switch of each steering pair plus the fail-safe well-biasing network, both off by design |
| `bulk_not_tied` | 54 | `XMPP` (bulk VDDIO, source `BIASP`) and the switch/well pfets whose bulk is the floating `WELL` net — the `DR-008` fail-safe floating-well intent, flagged by a generic rule |
| `triode` | 42 | mostly static logic in the select cells and the on-switches passing current at low V_ds. **`XMT`, the CMFB amplifier's own tail device, is in triode at the nominal condition** — a sizing observation for the follow-up |
| `gate_shorted_to_source` | 10 | an artefact of *this bench's* stimulus: `EM0`/`EM1` = 0 V and `EN` = VCCD tie those gates to a rail, which is exactly what "pre-emphasis disabled, driver enabled" means |
| `drain_tied_to_rail` | 10 | 2 × `XCC`, which is an intentional MOS **capacitor** (gate `VCMFB`, both other terminals VSSIO) and so a true false positive; 8 × `XMGTA`/`XMGTB`, whose drains are the bench's static gate-drive nodes |

**No floating-node finding, at any of the three conditions.** The `WELL` net in
every slice resolves cleanly — 1.7999 V at the nominal condition, and 1.9800 V
at `ff`/−40 °C/1.98 V/3.63 V — because `XMWVA`/`XMWVB` and their source–bulk
junctions tie it toward VCCD. The convergence hazard anticipated for `WELL` and
for the disabled slices' `TOP`/`BOT` nodes **did not materialise**, no
`options.nodeset` was needed, and all 75 conditions converged on the fleet.

`--op-lint` also emitted four `unsupported_hierarchy` warnings: it cannot expand
`XRS1`/`XRS2`, the `res_high_po_1p41` poly sense resistors, because their
`.subckt` lives in the model library rather than the netlist's own `.include`
closure. Those two devices are therefore **not** linted. Filed generically as
[`2AMLogic/klayout-tools#5644`](https://github.com/2AMLogic/klayout-tools/issues/5644).

### Grid shape

`klt sim --dry-run` reports `unit_count: 75` with **75 distinct** `corner_id`
values, and the committed summary carries a value — not an
`unavailable_measurement` — at all 75, including both spec-named extremes
(`ss`/125 °C/1.62 V/2.97 V: V_OD 246.6 mV, V_OS 1.7726 V, miss;
`ff`/−40 °C/1.98 V/3.63 V: V_OD 363.3 mV, V_OS 1.2471 V, pass).

## Stated limitations of this grid

- **No Monte Carlo.** E1–E4 are statistical rows; see the headline.
- **No transient.** E4's `V_OS(PP)` half, and E5/E9, are not here.
- **The poly sense resistors are typical at all 75 conditions.** All five
  process sections of the pinned `sky130.lib.spice` include
  `r+c/res_typical__cap_typical.spice`, so `XRS1`/`XRS2`
  (`res_high_po_1p41`) see no resistor corner anywhere in this grid. The sense
  divider is matched, so V_OS is first-order insensitive to *absolute* R — that
  is reasoning from the topology, not a measurement — and R **mismatch** is a
  Monte Carlo question. This is a limitation to record, not a reason to change
  the spec.
- **Measured at the driver output, not through the pad cell** — see below.
  **[Annotated 2026-11-15: resolved by the addendum below (issue #116). The
  corrected cell is now instantiated and the grid re-run; the limitation
  applied to the run recorded above, not to the addendum's run.]**
- The three disabled pre-emphasis slices are present and off; D3's enabled
  settings are not exercised.

### Why the pad cell is not in the deck

> **[Annotated 2026-11-15, issue #116: this section describes the run recorded
> above, whose deck deliberately omitted the then-defective cell. The corrected
> cell (`cd0c89a`) IS instantiated in the deck as now committed, and the G75
> grid has been re-run with it attached — see the addendum below. The rows
> here are kept verbatim as the evidence this bench's original decision rested
> on.]**

E1 and E2 are specified "at the pad". The `pad_cell` **as committed when this
bench was recorded** was nevertheless not instantiated, because it could not
carry a DC measurement: its ESD diode was declared with `area=4e14` — 400× the
model's own default — and shunted **107 mA** at 1.25 V. Measured on this host,
`tt`, 27 °C:

| Device under test | Shunt current at 1.25 V |
|---|---:|
| `pad_cell` as then committed | 107.4 mA |
| its ESD diode alone, as then committed | 107.4 mA |
| the same diode at the model default `area=1e12` | 268.6 µA |
| the ESD nfet alone (gate at VSSIO) | 6.4 pA |

That defect is **fixed**: filed as #100 and resolved by `cd0c89a` (PR #108),
which sizes the diode junction from the P1 budget (`area=64 perim=32`); #100 is
closed as completed. The rows above are kept as recorded — they are the
measurements this bench's decision rested on.

A first version of this bench did instantiate the then-committed cell on both
outputs: V_OD collapsed to 0.47 mV, V_OS to 0.23 mV, and the CMFB loop sat at a
starved zero-current operating point. The whole shunt was the diode and it
scaled with `area` exactly as the 400× ratio predicts; the ESD nfet was
correctly off. The diode's *orientation* is correct and must not be "fixed" —
the model subcircuit is `.subckt sky130_fd_pr__diode_pw2nd_11v0 N P` with body
`D0 N P`, so port 1 is the anode, and `XD1 VSSIO PAD` is therefore
reverse-biased for a positive pad, which is the ESD-to-VSSIO orientation
`DR-001` calls for.

With the pad cell absent, "at the pad" rests on an argument rather than a
simulated node: `pad_cell` is a **shunt-only** network — one reverse-biased
diode and one off ESD nfet, both from PAD to VSSIO — with **no series element
between the driver output and the pad**. At DC the driver output and the pad are
therefore the same node, and the cell's only DC effect is a shunt leakage. That
leakage is no longer an acceptance criterion — it is a **measurement**:
`sim/pad-dc/RECORD.md` ("DC shunt against the 3.5 mA tail") puts the corrected
cell's worst reverse shunt at the LVDS common mode at **2.04 nA** (`sf`,
125 °C), 5.8 × 10⁻⁷ of the 3.5 mA nominal tail, against the 107.4 mA measured
above before the fix. The equivalence argument therefore no longer rests on
topology alone. Re-running this bench with the corrected cell instantiated is
tracked in **#116** — **[done: see the 2026-11-15 addendum below.]**

## The wnflag trap

`options.ngspice_init: ["set wnflag=1", ...]` in `request.json` is **load-bearing
and must not be removed.** `wnflag` selects the multi-finger width convention:
with `nf > 1` it decides whether an instance's `W` is total width or width per
finger. The `driver` netlist uses `nf = 2, 3, 4` throughout, so the setting
changes the simulated geometry of nearly every device in it.

The first two submissions of this grid **aborted at all 75 conditions** with
`Fatal: Pclm = -0.12283 is not positive ... detected during BSIM4v5.5.0
parameter checking`, while the same request ran fine on this host. The cause was
not the models and not the engine — the staged model closure was identical (319
files, same `models_lib_sha256`) and the worker's ngspice binary is **byte-for-byte
the same build** as this host's. It was that this host's `$HOME/.spiceinit`
carries `set wnflag=1` and the fleet worker's image does not. Pointing `HOME` at
a directory whose `.spiceinit` set `wnflag=0` reproduced the identical fatal
locally, and declaring the setting in the request produced values matching the
host-`.spiceinit` run **bit for bit** on all eight measurements.

The abort was luck: a parameter happened to leave its valid range. The quiet
version of this failure is a full grid of plausible-looking numbers simulated at
the wrong device geometry, graded and committed as evidence. Declaring the init
lines in the request is what makes this record reproducible on any host.

Filed generically as
[`2AMLogic/klayout-tools#5648`](https://github.com/2AMLogic/klayout-tools/issues/5648)
(a `klt sim` report pins the netlist, models, PDK, engine version and engine
binary hash, but not the init file that also changes the numbers).

## Tool friction filed

| Issue | Gap |
|---|---|
| [klayout-tools#5644](https://github.com/2AMLogic/klayout-tools/issues/5644) | `--op-lint` never expands subcircuits whose `.subckt` is in the model library (PDK resistor primitives), so those devices go unlinted |
| [klayout-tools#5645](https://github.com/2AMLogic/klayout-tools/issues/5645) | a request field the batch runner cannot honor is refused only **after** the whole grid has run, and `--dry-run` reports `valid`; cost one full 75-unit grid |
| [klayout-tools#5648](https://github.com/2AMLogic/klayout-tools/issues/5648) | results depend on the host's ambient `.spiceinit`, which the report's `environment` block does not record |

The G75 grid itself needed **no** new `klt` capability: `corners.supply_v`
index-zips the rail pairs into one axis, giving 75 units directly.

`analysis.op_check` (a metastability check on the enable-path level shifter,
which is a cross-coupled latch) was dropped from the request: the fleet runner
image predates the field and refuses the whole run rather than grading without
it. The question it would have answered is covered instead by the three
`--op-lint` runs above, which report that path's devices and node voltages
directly.

## Per-condition results

All 75 conditions, V_OD and V_OS in both data states, ΔV_OD and ΔV_OS, and the
pass/fail mark per spec row. Grouped by process, then supply pair, then
temperature.

| # | Process | T (°C) | VCCD / VDDIO (V) | V_OD state 1 (mV) | V_OD state 0 (mV) | V_OS state 1 (mV) | V_OS state 0 (mV) | ΔV_OD (mV) | ΔV_OS (mV) | E1 | E2 win | E2 band | E3 | E4 DC |
|---:|---|---:|---|---:|---:|---:|---:|---:|---:|:--:|:--:|:--:|:--:|:--:|
| 1 | tt | -40 | 1.62 / 2.97 | 227.8 | 227.8 | 1252.7 | 1252.7 | +0.0004 | +0.0000 | **FAIL** | pass | pass | pass | pass |
| 2 | tt | 27 | 1.62 / 2.97 | 294.4 | 294.4 | 1258.5 | 1258.5 | +0.0006 | +0.0000 | pass | pass | pass | pass | pass |
| 3 | tt | 125 | 1.62 / 2.97 | 299.9 | 299.9 | 1528.5 | 1528.5 | -0.0001 | +0.0002 | pass | **FAIL** | **FAIL** | pass | pass |
| 4 | tt | -40 | 1.80 / 3.30 | 348.7 | 348.7 | 1251.4 | 1251.4 | -0.0013 | -0.0000 | pass | pass | pass | pass | pass |
| 5 | tt | 27 | 1.80 / 3.30 | 350.0 | 350.0 | 1253.7 | 1253.7 | +0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 6 | tt | 125 | 1.80 / 3.30 | 343.6 | 343.6 | 1262.7 | 1262.7 | -0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 7 | tt | -40 | 1.98 / 3.63 | 364.7 | 364.7 | 1248.4 | 1248.4 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 8 | tt | 27 | 1.98 / 3.63 | 365.9 | 365.9 | 1249.1 | 1249.1 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 9 | tt | 125 | 1.98 / 3.63 | 362.3 | 362.3 | 1252.7 | 1252.7 | -0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 10 | tt | -40 | 1.62 / 3.63 | 365.5 | 365.5 | 1249.7 | 1249.7 | -0.0002 | -0.0000 | pass | pass | pass | pass | pass |
| 11 | tt | 27 | 1.62 / 3.63 | 366.5 | 366.5 | 1253.3 | 1253.3 | +0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 12 | tt | 125 | 1.62 / 3.63 | 357.8 | 357.8 | 1422.4 | 1422.4 | +0.0001 | -0.0021 | pass | **FAIL** | **FAIL** | pass | pass |
| 13 | tt | -40 | 1.98 / 2.97 | 227.1 | 227.1 | 1252.4 | 1252.4 | +0.0040 | +0.0001 | **FAIL** | pass | pass | pass | pass |
| 14 | tt | 27 | 1.98 / 2.97 | 293.7 | 293.7 | 1255.8 | 1255.8 | -0.0057 | -0.0002 | pass | pass | pass | pass | pass |
| 15 | tt | 125 | 1.98 / 2.97 | 314.3 | 314.3 | 1263.7 | 1263.7 | -0.0001 | -0.0000 | pass | pass | pass | pass | pass |
| 16 | ff | -40 | 1.62 / 2.97 | 320.5 | 320.5 | 1253.5 | 1253.5 | -0.0023 | -0.0001 | pass | pass | pass | pass | pass |
| 17 | ff | 27 | 1.62 / 2.97 | 331.9 | 331.9 | 1257.1 | 1257.1 | +0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 18 | ff | 125 | 1.62 / 2.97 | 324.1 | 324.1 | 1269.7 | 1269.7 | +0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 19 | ff | -40 | 1.80 / 3.30 | 350.6 | 350.6 | 1250.0 | 1250.0 | +0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 20 | ff | 27 | 1.80 / 3.30 | 351.7 | 351.7 | 1251.3 | 1251.3 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 21 | ff | 125 | 1.80 / 3.30 | 348.0 | 348.0 | 1256.0 | 1256.0 | -0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 22 | ff | -40 | 1.98 / 3.63 | 363.3 | 363.3 | 1247.1 | 1247.1 | +0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 23 | ff | 27 | 1.98 / 3.63 | 366.1 | 366.1 | 1247.3 | 1247.3 | -0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 24 | ff | 125 | 1.98 / 3.63 | 364.4 | 364.4 | 1248.9 | 1248.9 | +0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 25 | ff | -40 | 1.62 / 3.63 | 363.6 | 363.6 | 1247.7 | 1247.7 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 26 | ff | 27 | 1.62 / 3.63 | 366.4 | 366.4 | 1249.2 | 1249.2 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 27 | ff | 125 | 1.62 / 3.63 | 364.0 | 364.0 | 1256.4 | 1256.4 | -0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 28 | ff | -40 | 1.98 / 2.97 | 320.0 | 320.0 | 1253.0 | 1253.0 | -0.0012 | -0.0000 | pass | pass | pass | pass | pass |
| 29 | ff | 27 | 1.98 / 2.97 | 331.4 | 331.4 | 1255.1 | 1255.1 | -0.0001 | -0.0000 | pass | pass | pass | pass | pass |
| 30 | ff | 125 | 1.98 / 2.97 | 324.3 | 324.3 | 1259.9 | 1259.9 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 31 | ss | -40 | 1.62 / 2.97 | 146.7 | 146.7 | 1252.0 | 1252.0 | -0.0060 | -0.0002 | **FAIL** | pass | pass | pass | pass |
| 32 | ss | 27 | 1.62 / 2.97 | 212.3 | 212.3 | 1256.4 | 1256.4 | +0.0075 | +0.0005 | **FAIL** | pass | pass | pass | pass |
| 33 | ss | 125 | 1.62 / 2.97 | 246.6 | 246.6 | 1772.6 | 1772.6 | +0.0008 | -0.0188 | **FAIL** | **FAIL** | **FAIL** | pass | pass |
| 34 | ss | -40 | 1.80 / 3.30 | 267.3 | 267.3 | 1251.1 | 1251.1 | +0.0001 | -0.0000 | pass | pass | pass | pass | pass |
| 35 | ss | 27 | 1.80 / 3.30 | 324.2 | 324.2 | 1255.7 | 1255.7 | -0.0052 | -0.0003 | pass | pass | pass | pass | pass |
| 36 | ss | 125 | 1.80 / 3.30 | 328.0 | 328.0 | 1538.3 | 1538.3 | +0.0001 | -0.0042 | pass | **FAIL** | **FAIL** | pass | pass |
| 37 | ss | -40 | 1.98 / 3.63 | 366.8 | 366.8 | 1249.7 | 1249.7 | -0.0002 | -0.0000 | pass | pass | pass | pass | pass |
| 38 | ss | 27 | 1.98 / 3.63 | 366.8 | 366.8 | 1251.4 | 1251.4 | +0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 39 | ss | 125 | 1.98 / 3.63 | 360.9 | 360.9 | 1258.7 | 1258.7 | +0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 40 | ss | -40 | 1.62 / 3.63 | 368.3 | 368.3 | 1253.0 | 1253.0 | -0.0001 | -0.0000 | pass | pass | pass | pass | pass |
| 41 | ss | 27 | 1.62 / 3.63 | 364.3 | 364.3 | 1432.8 | 1432.8 | -0.0003 | +0.0153 | pass | **FAIL** | **FAIL** | pass | pass |
| 42 | ss | 125 | 1.62 / 3.63 | 217.1 | 217.1 | 2342.2 | 2342.2 | -0.0001 | +0.0002 | **FAIL** | **FAIL** | **FAIL** | pass | pass |
| 43 | ss | -40 | 1.98 / 2.97 | 146.1 | 146.1 | 1251.7 | 1251.7 | -0.0035 | -0.0001 | **FAIL** | pass | pass | pass | pass |
| 44 | ss | 27 | 1.98 / 2.97 | 211.6 | 211.6 | 1254.6 | 1254.6 | +0.0027 | +0.0001 | **FAIL** | pass | pass | pass | pass |
| 45 | ss | 125 | 1.98 / 2.97 | 281.0 | 281.0 | 1265.3 | 1265.3 | -0.0001 | -0.0001 | pass | pass | pass | pass | pass |
| 46 | sf | -40 | 1.62 / 2.97 | 117.5 | 117.5 | 1251.3 | 1251.3 | -0.0027 | -0.0001 | **FAIL** | pass | pass | pass | pass |
| 47 | sf | 27 | 1.62 / 2.97 | 181.8 | 181.8 | 1253.9 | 1253.9 | +0.0071 | +0.0003 | **FAIL** | pass | pass | pass | pass |
| 48 | sf | 125 | 1.62 / 2.97 | 255.8 | 255.8 | 1262.4 | 1262.4 | -0.0042 | -0.0005 | pass | pass | pass | pass | pass |
| 49 | sf | -40 | 1.80 / 3.30 | 228.6 | 228.6 | 1250.0 | 1250.0 | -0.0089 | -0.0002 | **FAIL** | pass | pass | pass | pass |
| 50 | sf | 27 | 1.80 / 3.30 | 288.1 | 288.1 | 1252.2 | 1252.2 | -0.0018 | -0.0001 | pass | pass | pass | pass | pass |
| 51 | sf | 125 | 1.80 / 3.30 | 332.5 | 332.5 | 1258.6 | 1258.6 | +0.0002 | +0.0000 | pass | pass | pass | pass | pass |
| 52 | sf | -40 | 1.98 / 3.63 | 355.9 | 355.9 | 1249.0 | 1249.0 | +0.0021 | +0.0000 | pass | pass | pass | pass | pass |
| 53 | sf | 27 | 1.98 / 3.63 | 361.6 | 361.6 | 1249.8 | 1249.8 | -0.0001 | -0.0000 | pass | pass | pass | pass | pass |
| 54 | sf | 125 | 1.98 / 3.63 | 356.5 | 356.5 | 1252.3 | 1252.3 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 55 | sf | -40 | 1.62 / 3.63 | 357.4 | 357.4 | 1249.5 | 1249.5 | -0.0034 | -0.0001 | pass | pass | pass | pass | pass |
| 56 | sf | 27 | 1.62 / 3.63 | 362.5 | 362.5 | 1251.4 | 1251.4 | +0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 57 | sf | 125 | 1.62 / 3.63 | 357.0 | 357.0 | 1258.3 | 1258.3 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 58 | sf | -40 | 1.98 / 2.97 | 117.1 | 117.1 | 1251.2 | 1251.2 | -0.0026 | -0.0001 | **FAIL** | pass | pass | pass | pass |
| 59 | sf | 27 | 1.98 / 2.97 | 181.1 | 181.1 | 1253.6 | 1253.6 | +0.0057 | +0.0002 | **FAIL** | pass | pass | pass | pass |
| 60 | sf | 125 | 1.98 / 2.97 | 254.9 | 254.9 | 1259.8 | 1259.8 | -0.0009 | -0.0001 | pass | pass | pass | pass | pass |
| 61 | fs | -40 | 1.62 / 2.97 | 309.1 | 309.1 | 1770.2 | 1770.2 | +0.0022 | -0.0240 | pass | **FAIL** | **FAIL** | pass | pass |
| 62 | fs | 27 | 1.62 / 2.97 | 262.0 | 262.0 | 1967.2 | 1967.2 | -0.0142 | +0.0586 | pass | **FAIL** | **FAIL** | pass | pass |
| 63 | fs | 125 | 1.62 / 2.97 | 165.0 | 165.0 | 2162.1 | 2162.1 | -0.0010 | +0.0034 | **FAIL** | **FAIL** | **FAIL** | pass | pass |
| 64 | fs | -40 | 1.80 / 3.30 | 349.2 | 349.2 | 1251.6 | 1251.6 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 65 | fs | 27 | 1.80 / 3.30 | 350.2 | 350.2 | 1255.9 | 1255.9 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 66 | fs | 125 | 1.80 / 3.30 | 301.1 | 301.1 | 1882.5 | 1882.6 | +0.0011 | -0.0066 | pass | **FAIL** | **FAIL** | pass | pass |
| 67 | fs | -40 | 1.98 / 3.63 | 361.7 | 361.7 | 1248.1 | 1248.1 | +0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 68 | fs | 27 | 1.98 / 3.63 | 364.4 | 364.4 | 1249.4 | 1249.4 | -0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 69 | fs | 125 | 1.98 / 3.63 | 362.6 | 362.6 | 1256.7 | 1256.7 | -0.0000 | +0.0000 | pass | pass | pass | pass | pass |
| 70 | fs | -40 | 1.62 / 3.63 | 361.9 | 361.9 | 1251.8 | 1251.8 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 71 | fs | 27 | 1.62 / 3.63 | 339.2 | 339.2 | 1788.2 | 1788.3 | +0.0044 | -0.0352 | pass | **FAIL** | **FAIL** | pass | pass |
| 72 | fs | 125 | 1.62 / 3.63 | 127.5 | 127.5 | 2592.9 | 2592.9 | +0.0002 | -0.0010 | **FAIL** | **FAIL** | **FAIL** | pass | pass |
| 73 | fs | -40 | 1.98 / 2.97 | 331.0 | 331.0 | 1254.0 | 1254.0 | -0.0000 | -0.0000 | pass | pass | pass | pass | pass |
| 74 | fs | 27 | 1.98 / 2.97 | 330.5 | 330.5 | 1257.3 | 1257.3 | -0.0000 | -0.0001 | pass | pass | pass | pass | pass |
| 75 | fs | 125 | 1.98 / 2.97 | 315.4 | 315.4 | 1427.1 | 1427.1 | +0.0006 | -0.0105 | pass | **FAIL** | **FAIL** | pass | pass |

## Addendum — 2026-11-15: the G75 grid re-run with the corrected pad cell attached (#116)

**Nothing above this section has been rewritten** — it records the run made
without the pad cell and stays as the baseline this addendum reconciles
against. This addendum records the second run: same bench, same request
semantics, the corrected `pad_cell` (`cd0c89a`, PR #108) instantiated on all
four output nodes behind ideal 0 V ammeters.

**The headline is unchanged: 51 of 75 conditions pass every row, 24 miss at
least one, 0 errored, 0 inconclusive.** No condition's pass flag changed and no
condition's V_OD or V_OS moved by more than 1 mV (largest movement anywhere in
the grid: 0.104 mV — see Reconciliation). E1/E2 are now graded at a simulated
pad node instead of by the DC-equivalence argument, and the argument's
prediction — unchanged pass counts — is confirmed by simulation, not by
reasoning.

### What changed in the deck and the request

- `driver_dc.spice` gains `.include ../../design/pad_cell/pad_cell.spice` and
  four `pad_cell` instances, one per output node (`outp1`, `outn1`, `outp0`,
  `outn0`), identically, each behind an ideal 0 V ammeter (`VPCP1`/`VPCN1`/
  `VPCP0`/`VPCN0`, DR-007-labelled) in the **shunt** branch — between the pad
  node and the cell's `PAD` pin, so it carries only the cell's shunt current;
  the 100 Ω loads stay directly across the pad nodes. No change to `IREF`
  (still 54.3 µA, frozen), `VCMREF`, the gate-drive pattern, the loads, or any
  device size. Instantiating one instance and not the other, or one side and
  not its mirror, would have manufactured a spurious ΔV_OD/ΔV_OS out of this
  bench's own asymmetry — hence all four.
- `request.json` gains exactly two entries, both **ungraded diagnostic
  observers** (`ishunt_p1` / `ishunt_n1`, `expr: abs(i(vpcp1))` /
  `abs(i(vpcn1))`, unit A, **no `limits`**): one per side of instance 1;
  instance 0 mirrors the cells. **The eight graded `measurements` entries are
  byte-identical** to the recorded run, as are `options.ngspice_init`,
  `options.stage_model_inputs`, `node_voltage_bounds` and
  `batch.capacity_wait_s`. Because `pad_cell` adds no series element, the
  graded nodes are the pad nodes the moment the cells are on them, so the new
  grid is comparable to the recorded one condition-for-condition with no
  expression change.
- Nothing under `spec/` was touched; no graded limit was changed; a condition
  that missed before and misses again is still a recorded miss.

### Provenance

| Field | Value |
|---|---|
| Repo base commit | `7b02f9dca35c493641c62183ecc2d5dfe920b263` (inputs below are content-hashed) |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (unchanged) |
| Model library sha256 | `17c208a699228f5acb87bf59c09c22a4c4d3937b6766b4957737d34e8e075f64` (`sky130.lib.spice`, unchanged) |
| Testbench sha256 | `c522327d7f0994e51bb0774f95911b54a669639ac9633743d99f476860e06ed8` (`driver_dc.spice` **as run** — identical to the committed deck) |
| DUT netlist sha256 | `5f008c909faf1fe3d3cc5dd43a9146fa5db9a7cf605634fbf37f912075959137` (`design/driver/driver.spice`, unchanged) |
| Pad cell sha256 | `11be4ca2e27e2f1fa4968792dd61a3af6a8bad9f7f755e344a306ff54f18e116` (`design/pad_cell/pad_cell.spice`, new in the closure) |
| Client | `klt 0.9.3.dev3+gd5d57daf9a14`, klayout 0.30.13 (recorded run: `0.9.2.dev1022` — a third klt generation, see Reconciliation) |
| Runner | batch runner `klt 0.9.0`, `runner_compatibility: match` (same runner version as the recorded run) |
| Engine | ngspice 47 on the batch worker, binary sha256 `39ca1adb826660324c3626f72bd946ec40704f0f3fc8e243c623f76e24b3eee2` (byte-identical to the recorded run's and to this host's) |
| ngspice init | `set wnflag=1`, `set num_threads=1`, unchanged in the request — **still load-bearing, see "The wnflag trap"** (the pad cell's own devices are `nf=1`, which is why `sim/pad-dc/` needs no init; this request's driver devices with `nf = 2, 3, 4` decide it) |
| Backend | `batch`, job `klt-sim-0dc289f63be9`, 75 units, `options.stage_model_inputs: true` (319 model files staged), spot `m7i.4xlarge` (recorded run: `c7i.4xlarge`), job wall time 115 s |

Reproduce:

```console
PDK_ROOT=<pinned ciel root> klt sim sim/driver-dc/request.json \
    --backend batch --wait-for-capacity 600 \
    --report-out sim/driver-dc/results/report.json
```

Two solver notes for the new deck, both deliberately *not* acted on:

- **No `gmin` override.** `sim/pad-dc/` sets `gmin: [1e-15]` to resolve pA
  leakage; this request does not, because changing solver settings would
  perturb the grid whose comparability is the deliverable. At ngspice's default
  `gmin = 1e-12` each node carries a ~pA solver conductance to ground, so at
  the cold corners the shunt observers read the **floor**, not the device —
  reported below as a floor, never as a device figure.
- **The fleet's job-ceiling warning fired** (conservative serial bound 9120 s >
  ceiling 3600 s; the client suggests `remote.hosts: 3`). The job finished in
  115 s, two orders inside the ceiling, so sharding was not needed this run; a
  future grid of this shape with slower per-unit runtimes should shard per
  that warning rather than assume the same headroom.

### Single-corner probe before the fleet submit

Run locally (`--backend local`, one operating point — the only leg this host
runs locally) at `tt`/27 °C/1.80 V/3.30 V, on the committed deck and request,
**before** the 75-unit submit: host klt `0.9.3.dev3+gd5d57daf9a14`, host ngspice
47 (binary sha256 `39ca1adb…`, byte-identical to the fleet worker's), PDK
`~/.ciel` (open_pdks `f6eeac7…`):

| Quantity | Probe | Recorded baseline | Δ |
|---|---|---|---|
| V_OD state 1 | 349.9785 mV | 349.9785 mV | 0 |
| V_OD state 0 | 349.9785 mV | 349.9785 mV | 0 |
| V_OS state 1 | 1.2537480 V | 1.253748 V | 0 |
| V_OS state 0 | 1.2537480 V | 1.253748 V | 0 |
| `ishunt_p1` | 8.64 pA | — (not observed then) | new |
| `ishunt_n1` | 6.74 pA | — (not observed then) | new |

Attaching the corrected cell **moved the nominal V_OD/V_OS by nothing at the
report's 7-significant-digit precision** — the strongest single-condition
confirmation that the ammeter + shunt adds no series impedance to the graded
nodes. Only then was the grid submitted to the fleet.

### Reconciliation against the recorded grid

Per-row pass counts, condition-for-condition:

| Row | Recorded (no pad cell) | This run (pad cell attached) |
|---|---:|---:|
| E1 | 60 / 75 | **60 / 75** |
| E2 window | 62 / 75 | **62 / 75** |
| E2 regulation band | 62 / 75 | **62 / 75** |
| E3 | 75 / 75 | **75 / 75** |
| E4 (DC half) | 75 / 75 | **75 / 75** |
| any-miss | 24 / 75 | **24 / 75** |

0 errored, 0 inconclusive, and the committed `results/summary.json` carries a
value — not an `unavailable_measurement` — at all 75 conditions.

- **No condition's pass flag changed.** The 24 any-miss conditions are the same
  conditions missing the same rows as the recorded run.
- **No condition's V_OD or V_OS moved by more than 1 mV** — the naming
  threshold set for this reconciliation — so there are no individually-named
  conditions. The largest movement anywhere in the grid is **0.104 mV** (V_OS
  state 0, `fs`/1.62 V/2.97 V/27 °C), an order of magnitude inside the
  threshold; every delta is at solver-noise level.
- Observed ranges: V_OD **117.1148 – 368.2871 mV** (recorded: 117.1159 –
  368.2868 mV), V_OS **1.247141 – 2.592883 V** (recorded: 1.247141 – 2.592885
  V) — endpoints move only at the µV scale.
- |ΔV_OD| ≤ **19.4 µV**, |ΔV_OS| ≤ **110.8 µV** (recorded: 14.2 µV / 58.6 µV)
  — both far inside the 50 mV E3/E4 budget. The roughly-2× growth of these
  solver-noise residuals is not a design change: the four cells were
  instantiated symmetrically, and E3/E4 still pass at every condition. (As
  before, **do not read 75/75 as E3/E4 being met** — "Read E3 and E4 with
  care" above applies to this run unchanged.)
- Single-ended pad-node extremes from this run's committed summary: **2.6566 V**
  (`fs`/1.62 V/3.63 V/125 °C) and **1.0642 V** (`ff`/1.98 V/3.63 V/27 °C),
  matching the figures #116's curation derived from the recorded run — now
  with the cell attached and its shunt measured there.
- Three klt client generations (`0.9.2.dev1022` → `0.9.3.dev3`, same `0.9.0`
  batch runner) have now produced the same graded verdicts on this bench.

### The measured shunt

`ishunt_p1`/`ishunt_n1` are the first in-repo measurements of the corrected
cell **with the driver attached**, and they extend the characterised bias range
past `sim/pad-dc/`'s 2.4 V ceiling:

| Where | Pad node bias (V_OS ∓ V_OD/2) | `ishunt_p1` | `ishunt_n1` |
|---|---|---|---|
| nominal, `tt`/27 °C/1.80 V/3.30 V | 1.4287 / 1.0788 V | 8.64 pA | 6.74 pA |
| all 25 −40 °C corners | ≈1.07–1.92 V (upper end `fs`/1.62 V/2.97 V/−40 °C) | 6.6–9.7 pA | 5.4–8.2 pA |
| grid max, `sf`/1.62 V/3.63 V/125 °C | 1.4368 / 1.0798 V | **2.117 nA** | 1.982 nA |
| **`fs`/1.62 V/3.63 V/125 °C** | **2.6566** / 2.5291 V | **1.118 nA** | 1.109 nA |
| **`ss`/1.62 V/3.63 V/125 °C** | **2.4508** / 2.2337 V | **1.205 nA** | 1.185 nA |

- **The two >2.4 V conditions are now measured, not argued.** At a pad node of
  2.4508 V (`ss`) and 2.6566 V (`fs`) the cell shunts **1.1–1.2 nA** — six
  orders of magnitude below the 3.5 mA nominal tail, and *smaller* than the
  grid's own maximum. This was the bias range no existing measurement covered
  (the strongest reason this run spent 75 fleet units), and the answer is that
  the reverse-biased ESD diode's leakage follows the **process flavour and
  temperature** far more than the reverse bias: the grid maximum, 2.117 nA,
  sits at `sf`/125 °C with the pad node at only 1.44 V — consistent with
  `sim/pad-dc/RECORD.md`'s worst-case 2.04 nA at `sf`/125 °C at 1.25 V,
  measured there without the driver. A >2.4 V pad bias does **not** buy a
  proportionally larger shunt, and in particular buys nothing close to the
  107 mA the pre-fix cell shunted.
- **The −40 °C rows are the gmin floor, not a device figure.** At −40 °C the
  observers read 5–10 pA; ngspice's default `gmin = 1e-12` puts a ~pA solver
  conductance on each node (the pad node at ~1.25 V alone explains ~1.25 pA,
  and the ammeter's floating `pcp*` node adds its own). `sim/pad-dc/` needed
  `gmin = 1e-15` to resolve true pA-scale device leakage; this run keeps the
  default to preserve grid comparability, so those rows are a floor — quoted
  as such and carried nowhere as device leakage.
- The p1/n1 pairs differ because the two outputs of a state sit at *different*
  absolute voltages (V_OS ± V_OD/2 → different reverse biases → different
  diode leakage), not because of asymmetric instantiation; the symmetric
  instantiation is evidenced by E3/E4 staying at solver noise across all 75.

### What this still does not close

Unchanged from this record's headline: **this bench closes no spec row.** E1–E4
remain statistical rows owing the local-mismatch Monte Carlo, and E4's
`V_OS(PP)` half remains transient and out of scope. The E8 / thin-oxide stress
question at the three conditions where V_OS exceeds 1.98 V is re-observed here
under the same numbers and remains unresolved. Sizing closure starts from this
record plus that Monte Carlo.
