# Pad-cell DC shunt and junction capacitance — record

**Simulated, not measured.** The pad cell's DC shunt current and its
small-signal capacitance at the pad, over the process and temperature axes of
the G75 grid. It is evidence for spec rows **P1** (pad capacitance budget) and
the pad half of **P4** (unpowered pad current); it says nothing about the
driver, and it is **not** an ESD qualification (see "What this does not
establish").

This bench exists because `design/pad_cell/pad_cell.sch` carried
`area=4e14 perim=8e7` on `D1`, which DC-shorted the pad (issue #100).

| Field | Value |
|---|---|
| Repo base commit | `d7da34a8c017a4fedbe845816668cdb4bbf5653a` (inputs below are content-hashed) |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (ciel 2.6.1, `$PDK_ROOT=~/.ciel`; `docs/environment.md`) |
| Model library sha256 | `17c208a699228f5acb87bf59c09c22a4c4d3937b6766b4957737d34e8e075f64` (`sky130.lib.spice`) |
| Deck sha256 | `ce27b60c0905e18fd337fa55aab6868946ca3a2cef8abedbc982712fe5399bb4` (`pad_shunt.spice`) |
| DUT netlist sha256 | `11be4ca2e27e2f1fa4968792dd61a3af6a8bad9f7f755e344a306ff54f18e116` (`design/pad_cell/pad_cell.spice`, included by reference) |
| Request sha256 | `919fdc7ef9656b23a178e5a047da068c2c13c4817e5de8d34146be8fcf57a378` |
| Client | `klt 0.9.2.dev1025+ga90545db9ea6` (the host tool), klayout 0.30.13. The **netlists** under `design/` are generated with the repo's pinned `klayout-tools==0.8.0` instead (`docs/environment.md`), run via `uvx` — see "Which klt generated what" |
| Engine | ngspice 47 on the batch worker; `options.stage_model_inputs: true` staged 319 pinned model files, so the executed models are the pinned ones |
| Backend | `batch` (host default), job `klt-sim-8cfc383887b1`, `m7i.4xlarge` spot, us-east-1a, 15 units, submitted with `--wait-for-capacity 600` |
| Result | `status: pass`, 15/15 corners. `results/report.json.gz` (full report), `results/summary.json` (per-corner distillate), `results/batch-receipt.json` |

## What ran

`pad_shunt.spice` is a circuit body only (`klt sim` supplies `.lib`/`.temp`/the
control block, as in `sim/pdk-smoke/inverters.spice`). It `.include`s
**`design/pad_cell/pad_cell.spice` itself**, so the bench cannot drift from the
committed cell. `VSSIO` is tied to node 0 and `pad_cell` has no `VCCD`/`VDDIO`
pin, so the deck is also the **unpowered** condition by construction — the rails
are at 0 V because the cell has none.

One `klt sim` request (`request.json`) with seven `analysis_steps`: `op` solves
at pad = 1.25 V, 0 V, 2.4 V and −1.0 V, and `ac` solves at 1.0 / 1.25 / 1.60 V.
`VPAD` carries a 1 V AC magnitude, so the capacitance is read off the quadrature
branch current at 1 MHz, `C = |Im(I)| / 2πf`.

### Which klt generated what

Two `klt` builds are involved, deliberately:

- **The netlists** (`design/pad_cell/pad_cell.spice`,
  `design/lvds_tx_analog.spice`) are regenerated with the repo's **pinned**
  `klayout-tools==0.8.0` (`docs/environment.md`, `scripts/setup-env.sh`,
  `.github/workflows/signoff.yml`), invoked as
  `uvx --from "klayout-tools==0.8.0" klt netlist …`. The host's own `klt` is
  0.9.2, newer than the pin, and its `klt signoff --attest` writes a
  structurally different attestation envelope (`provenance.input.paths` instead
  of `provenance.input.path`) that CI's pinned 0.8.0 `--check` rejects with
  exit 3. The pinned build is therefore the correct generator for anything
  committed under `design/` or `verification/signoff/evidence/`.
- **This simulation** was run by the host's `klt 0.9.2`, as `sim/pdk-smoke`'s
  record was run by whatever `klt` was installed then (0.7.1.dev). The request
  and report are version-stamped in `results/report.json.gz`
  (`provenance.klt_version`), so the client is recorded rather than pinned.

The grid was run twice, before and after switching the netlist generator from
0.9.2 to the pinned 0.8.0 — jobs `klt-sim-833e7f4dd323` and
`klt-sim-8cfc383887b1`. **Every one of the 105 figures was identical**, which
is independent evidence that the textual difference between the two generators'
output (continuation-line wrapping, inherited from `xschem` rather than from
`klt` — filed as `2AMLogic/klayout-tools#5715`) is electrically inert. Only the
second job is committed, because its netlist is the committed one.

### The grid: G75 with the supply axis collapsed, and why

G75 is process (5) × temperature (3) × supply pair (5) = 75 conditions. This
cell **has no supply pin**, so the supply axis cannot be expressed and cannot
change the result; `klt sim` labels every corner `novdd` of its own accord. The
run is therefore the **15** conditions G75 has left — all five process corners
× −40 / 27 / 125 °C. Spec row `P4` sets this precedent explicitly for the
unpowered case ("all five process corners (rails at 0 V, so no supply axis)").
Any figure here that is later re-measured **with the driver attached** owes the
full 75, because the driver does have rails.

`corners.options.gmin = 1e-15` lowers the solver's conductance floor. At
ngspice's default `gmin = 1e-12` the reported shunt at 1.25 V is 7.56 pA, of
which ~83 % is the floor rather than the device; at 1e-15 it is 1.31 pA, and
1e-18 gives the identical 1.31 pA, so the reported leakage is **converged on the
device**, not on the simulator.

## Results (15/15 pass)

| corner | T °C | I(1.25 V) | C(1.00 V) | C(1.25 V) | C(1.60 V) | I(0 V) | I(2.4 V) | I(−1.0 V) |
|---|---|---|---|---|---|---|---|---|
| `tt` | −40 | 0 | 93.7 fF | 91.2 fF | 88.2 fF | <1 fA | 0 | 32.3 mA |
| `tt` | 27 | 1 pA | 95.4 fF | 92.6 fF | 89.5 fF | <1 fA | 2 pA | 45.2 mA |
| `tt` | 125 | 1.32 nA | 97.2 fF | 94.2 fF | 90.8 fF | <1 fA | 1.49 nA | 65.4 mA |
| `ff` | −40 | 0 | 82.1 fF | 79.8 fF | 77.3 fF | <1 fA | 0 | 32.8 mA |
| `ff` | 27 | 3 pA | 83.5 fF | 81.1 fF | 78.4 fF | <1 fA | 3 pA | 45.7 mA |
| `ff` | 125 | 1.73 nA | 85.1 fF | 82.5 fF | 79.5 fF | <1 fA | 2.06 nA | 65.8 mA |
| `ss` | −40 | 0 | 105.5 fF | 102.6 fF | 99.3 fF | <1 fA | 0 | 31.8 mA |
| `ss` | 27 | <1 fA | 107.3 fF | 104.3 fF | 100.8 fF | <1 fA | 1 pA | 44.8 mA |
| `ss` | 125 | 1.09 nA | 109.3 fF | 106.0 fF | 102.2 fF | <1 fA | 1.19 nA | 65.0 mA |
| `sf` | −40 | 0 | 77.1 fF | 75.0 fF | 72.6 fF | <1 fA | 0 | 32.9 mA |
| `sf` | 27 | 4 pA | 78.4 fF | 76.2 fF | 73.7 fF | <1 fA | 5 pA | 45.8 mA |
| `sf` | 125 | **2.04 nA** | 79.9 fF | 77.5 fF | 74.7 fF | <1 fA | **2.48 nA** | 65.9 mA |
| `fs` | −40 | 0 | 110.5 fF | 107.5 fF | 104.0 fF | <1 fA | 0 | **31.7 mA** |
| `fs` | 27 | <1 fA | 112.5 fF | 109.3 fF | 105.6 fF | <1 fA | <1 fA | 44.7 mA |
| `fs` | 125 | 1.01 nA | **114.6 fF** | 111.1 fF | 107.1 fF | <1 fA | 1.09 nA | 64.9 mA |

Bold is the worst case of its column. `I(1.25 V)` and `I(2.4 V)` are reverse
(blocking) currents; `I(−1.0 V)` is the clamp conducting forward.

### DC shunt against the 3.5 mA tail

Worst reverse shunt at the LVDS common mode is **2.04 nA** (`sf`, 125 °C), i.e.
**5.8 × 10⁻⁷ of the 3.5 mA nominal tail** (`E1`'s 350 mV into 100 Ω). Split by
device at `tt`/27 °C/1.25 V: `D1` alone 18.5 fA, `XMESD` alone 1.307 pA — so
what little remains is the ESD nfet's, not the diode's, and the diode's own
share is 5 × 10⁻¹² of the tail.

This is the figure that was **107.4 mA** before this change: a 5.3 × 10⁷
reduction, and the reason any "at the pad" measurement condition (`E1`–`E9`) is
now meaningful at all.

### Capacitance against the P1 allocation

`P1` allows ≤ 2.0 pF per pad, of which **pad + ESD ≤ 1.2 pF**, and notes that
allocation "leaves ~0.14 pF over the 1.06 pF reference". Taking `DR-001`'s
1.061 pF `top_analog_pad` figure as that reference leaves **139 fF** for the
custom ESD network. Worst condition over the grid *and* over `P1`'s stated
1.0–1.6 V bias range is `fs` / 125 °C / pad at 1.0 V (lowest bias gives the
largest C\_j):

| Contribution | C at `fs`/125 °C/1.0 V |
|---|---|
| `XMESD` junctions (the snapback clamp `DR-001` requires; out of scope here) | 60.5 fF |
| `D1` at 64 µm² | 54.1 fF |
| **`pad_cell` total** (measured on the grid) | **114.6 fF** |
| Reserve left of the 139 fF allocation | **24.4 fF** (17.6 %) |

The 60.5 + 54.1 = 114.6 fF split was measured per device at that corner and
reconciles exactly with the grid's whole-cell figure.

**That 24.4 fF is a reserve, not margin already banked.** It has to cover the
drawn network's interconnect, contacts and guard ring, none of which is drawn
yet, and `P1`'s own stated evidence is "post-layout parasitic extraction of the
drawn cell, at the pad's 1.0–1.6 V bias; tool owed". **P1 is not claimed met by
this record** — this is the pre-layout budget showing the choice fits with room
to extract into.

### The sizing derivation (`D1` = 8.0 × 8.0 µm)

The unit convention first, since the original report had it wrong. `area` is in
**µm²** and `perim` in **µm**: the subcircuit pre-scales its model `cj` by 1e-12
(`cj = 0.0008512*1e-12` F per unit of `area`), so one unit of `area` is 1 µm²
and the implied areal capacitance is 0.851 fF/µm² — exactly the CJ `DR-001`
line 63 records for `diode_pw2nd_11v0`. Confirmed by measurement:
`area=1000 perim=130` gives **858 fF** against 851 fF predicted. So the
committed `area=4e14` was **4 × 10¹⁴ µm² = 400 m²** of junction with an 80 m
perimeter: a raw magnitude error, with no unit convention left to work out.

There is **no drawn ESD diode to derive the geometry from** — `DR-001` line 29
records that `analog_noesd_pad` instantiates `simple_pad_and_busses` only and
has no ESD structure, and `layout/README.md` lists `D1` as not drawn. The
numbers are therefore **chosen** against the spec and will have to be matched by
layout later.

**Capacitance binds; leakage cannot.** At any sane size the reverse current is
O(1 nA) — 10⁻⁷ of the tail — so it does not discriminate between candidates.
`P1` caps the area; `P2` (HBM ≥ 2 kV, **a target, not a result**; the PDK
publishes no rating) pushes the other way, because a larger junction is the one
lever on HBM available here. So the rule applied is: **take the largest round
rectangle that still leaves a usable extraction reserve under P1.** Measured at
`fs`/125 °C/1.0 V:

| Candidate | `D1` C | cell total | reserve of 139 fF | verdict |
|---|---|---|---|---|
| 9.0 × 9.0 µm (81 µm²) | 68.1 fF | 128.5 fF | 10.5 fF (7.6 %) | rejected: too little left for interconnect that is not yet drawn |
| **8.0 × 8.0 µm (64 µm²)** | **54.1 fF** | **114.6 fF** | **24.4 fF (17.6 %)** | **chosen** |
| 7.0 × 7.0 µm (49 µm²) | 41.8 fF | 102.3 fF | 36.7 fF (26.4 %) | rejected: gives up HBM area for margin `P1` does not ask for |

Hence `area = 8.0 × 8.0 = 64` µm², `perim = 2(8.0 + 8.0) = 32` µm. A square is
the minimum perimeter for a given area, so it is also the minimum sidewall
capacitance; the drawn cell may re-shape the junction into fingers provided it
keeps `area` and `perim`. The arithmetic and this reasoning are also written
into `design/pad_cell/pad_cell.sch` as text annotations, beside the instance
they explain.

*Rejected: reverting to the model default `area=1e12`.* It is a 1 m²
normalising default, not a geometry, and gives 269 µA.

### Orientation: re-confirmed, not changed

`libs.tech/ngspice/sky130_fd_pr__model__r+c.model.spice:180–182` is
`.subckt sky130_fd_pr__diode_pw2nd_11v0 N P` with body
`D0 N P sky130_fd_pr__diode_pw2nd_11v0`. A SPICE `D` card is
`Dxxx anode cathode model`, so port 1 (`N`, despite the name) is the **anode**.
`XD1 VSSIO PAD` therefore puts the anode on `VSSIO` and the cathode on `PAD`:
reverse-biased for a positive pad, which is `DR-001`'s ESD-to-VSSIO
orientation. **Correct as committed and deliberately left alone.**

The grid corroborates it electrically: ≤ 2.04 nA at +1.25 V against 31.7–65.9 mA
at −1.0 V, a ≥ 10⁷ forward/reverse asymmetry in the direction the orientation
predicts. A flipped diode would have conducted at +1.25 V.

### `P4` spot checks (`#97`'s bench, checked cheaply here)

`P4` allows ≤ ±20 µA per pad for 0 ≤ V\_pad ≤ 2.4 V with the rails at 0 V. At
the endpoints of that range this cell draws **< 1 fA at 0 V** and at most
**2.48 nA at 2.4 V** (`sf`, 125 °C) — four orders inside the limit.

This is **not** a `P4` result. `P4` is a joint pad-and-driver requirement
(`DR-008`) and needs the driver attached, both pads of a pair swept, and the
full temperature/process grid of its own row; two endpoints of the pad cell
alone are a spot check that the corrected diode does not conduct where `P4`
forbids it. `P4`/`P4a`/`P4b` remain owed to #97.

### The clamp still clamps

Forward (pad below `VSSIO`, the negative-strike direction `D1` exists for):
31.7 mA at −1.0 V worst case (`fs`, −40 °C), rising to 65.9 mA at 125 °C. The
resize did not disable the clamp. The `fwd_clamp_1v0` measurement carries a
`min` limit of 1 mA precisely so a future mis-sizing that silently switches the
diode off fails the request instead of passing it quietly.

## What this does not establish

- **Not an ESD qualification.** `P2` (HBM ≥ 2 kV, CDM ≥ 500 V) is "not provable
  by simulation" by its own evidence column, and the PDK publishes no rating for
  this device. Choosing the largest area `P1` allows is the best this record can
  do for `P2`; it is not a margin, and no HBM claim is made or implied.
- **Not `P1` met.** `P1` is owed post-layout extraction of the drawn cell. The
  24.4 fF reserve is what extraction has to fit into.
- **No LVS re-run is implied by this change.** `D1` is in neither the layout nor
  the LVS compare — `layout/README.md` line 100: "The ESD clamp, the `D1` diode
  and the pad frame are **not in this compare** (the top is the driver cell)" —
  and `layout/README.md` § "Not drawn yet (deferred)" lists `D1` as not drawn.
  Changing its SPICE parameters therefore cannot change any LVS result. This
  replaces the original issue's "re-check LVS if device parameters change": the
  device is not in the compare, so there is nothing to re-check. The committed
  GDS is untouched by this change (`gen_driver_pad.py` reads
  `design/driver/driver.spice`, `ddr_mux.spice` and `predriver.spice`, none of
  which this change touches).
- **The driver is not in this deck.** V\_OD / V\_OS with the corrected pad on
  both outputs is #96's bench; see "Handoff to #96" below.
- **The 1.061 pF pad reference is a reference, not a verified figure** for the
  wrapper cell this repo would place. `DR-001` establishes that explicitly. If
  extraction puts the drawn pad above it, the 139 fF ESD allocation shrinks and
  `D1` has to shrink with it — the trade is recorded above so that is a
  re-derivation, not a rediscovery.

## Handoff to #96

`sim/driver-dc/` is **absent from `origin/main` at `d7da34a`** — #96 is still
open with its PR #102 unmerged — so this record cannot re-run that bench. Per
issue #100's handoff criterion, the corrected figures are recorded here and
posted to #96 for its record to cite:

| Figure, corrected cell | Value |
|---|---|
| DC shunt at the pad, 1.25 V, worst over the grid | 2.04 nA (`sf`, 125 °C) |
| …as a fraction of the 3.5 mA nominal tail | 5.8 × 10⁻⁷ |
| `pad_cell` capacitance at the pad, worst over the grid and 1.0–1.6 V | 114.6 fF (`fs`, 125 °C, 1.0 V) |
| Same figures before this change | 107.4 mA and 0.25 F at 1.25 V |

#96's bench measured at the driver output and argued DC equivalence because
instantiating the committed `pad_cell` collapsed V\_OD to 0.47 mV. With the
shunt at 2.04 nA against a 3.5 mA tail, that argument now has a measured figure
to rest on, and #96 (or a follow-up) can put the real pad on the node instead.

## Reproduce

```console
export PDK_ROOT=$HOME/.ciel PDK=sky130A
klt sim sim/pad-dc/request.json --wait-for-capacity 600 \
    -o sim/pad-dc/results --report-out sim/pad-dc/results/report.json.gz
```

A single-corner local probe (allowed by the host's rules for one operating
point) is `--backend local` on the same request narrowed to one process corner
and temperature.
