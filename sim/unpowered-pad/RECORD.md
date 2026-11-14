# Unpowered-pad DC bench — record

**Simulated, not measured.** Graded **against a PROPOSED spec**: rows P4, P4a
and P4b of `spec/target-spec.md` are proposed figures carrying the operator
ruling of `DR-008` (2026-10-20); they are not ratified silicon limits. Nothing
here is a measurement, and nothing here is post-layout.

**Verdict: rows P4, P4a and P4b all FAIL on the committed schematics.** The
failures are recorded as findings. No schematic, device size or `spec/` text was
changed to make a row pass — see *Findings* below for the four defects this
bench surfaced and the follow-up work each one owes.

| Field | Value |
|---|---|
| Repo base commit | `d7da34a8c017a4fedbe845816668cdb4bbf5653a` (inputs below are content-hashed) |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (ciel 2.6.1; `docs/environment.md`) |
| PDK root (client) | `~/.ciel` — pinned with `$PDK_ROOT`; see *Pinning the PDK root* below |
| Model library sha256 | `17c208a699228f5acb87bf59c09c22a4c4d3937b6766b4957737d34e8e075f64` (`sky130.lib.spice`) |
| Design netlist sha256 | `e4e96a1bb634c5055f5289e70e0e630b60123820a562c6695623cecfc980b74e` (`design/lvds_tx_analog.spice`) |
| Testbench sha256 | `b1bb6c5339777d783b3bfe342059c99acce98b7f79a7403761e7c05a90d042c8` (`tb_unpowered.spice`, the shared core) |
| | `f6c6e439092aec839a6c4a7699a968563c6529cde563b66ec3144780c432c0b9` (`tb_sweep_a.spice`) |
| | `3dd141d7f6dc9850151a43c4064a90cde2065dc97c8aa8bb998011553244ead2` (`tb_sweep_b.spice`) |
| | `8f45d4aca36ab0dcfb5466039e5c18637db78fda20d60aa7e67be08d968197d9` (`tb_ramp.spice`) |
| Client | `klt 0.9.2.dev1022+g2a9c52b27ce7`, klayout 0.30.10 |
| Engine | ngspice-47 on the batch worker (`engine_version: "47"`, build of 2026-11-13 23:19:32 UTC — byte-identical banner to this host's client ngspice) |
| Backend | `batch`, `options.stage_model_inputs: true` (319 staged model inputs, pinned library) |
| Jobs | `klt-sim-816401017acb` (Sweep A), `klt-sim-13d4789e5ccc` (Sweep B), `klt-sim-ee92c54c9c19` (ramp); 10 units each, 30 total |
| Corner grid | `tt`/`sf`/`ff`/`ss`/`fs` × −40 / 125 °C, rails at 0 V, no supply axis (rows P4–P4b) |

## What ran

One `klt sim` request per condition, submitted as one set:

```bash
PDK_ROOT=~/.ciel klt sim --batch-set sim/unpowered-pad/request-sweep-a.json \
                                     sim/unpowered-pad/request-sweep-b.json \
                                     sim/unpowered-pad/request-ramp.json \
        --wait-for-capacity 600 --capacity-retries 2 -o <outdir> --report-out <path>
```

| Request | Condition | Analysis | Units | Aggregate |
|---|---|---|---|---|
| `request-sweep-a.json` | both pads of the pair swept together, 0 → 2.4 V | `dc VPSRC 0 2.4 0.01` (241 pts) | 10 | `inconclusive` (7 fail, 3 inconclusive) |
| `request-sweep-b.json` | row P4's differential partner pattern, V_padn = 2.5 − V_padp | `dc VPSRC 0.9 1.6 0.005` (141 pts) | 10 | `fail` (10 fail) |
| `request-ramp.json` | VCCD/VDDIO 0 → nominal → 0 over 1 ms each way, pads held at 1.25 V | `tran 2u 2.4m` | 10 | `fail` (5 pass, 5 fail) |

Results: `results/summary-{sweep-a,sweep-b,ramp}.json` (per-corner values) and
`results/report-{sweep-a,sweep-b,ramp}.json.gz` (the full `klt sim` reports).
Every one of the 30 units returned a value for every declared measurement
(`valueless = 0`); no corner errored or timed out.

### The device under test, and why the top level

The benches `.include` `design/lvds_tx_analog.spice` and instantiate
`lvds_tx_analog` whole — the committed subcircuits, included rather than
copied. The top level rather than `driver` plus `pad_cell` separately, because
the P-side top-switch gates are driven by DR-008's gate-tracking devices and
the N-side gates by the predriver's off devices: a bench that invented a value
for `GPA`/`GPB`/`XPA`/`XPB`/`GNA`/`GNB`/`XNA`/`XNB` would either defeat the
gate tracking rows P4a/P4b are about or fabricate a pass. As it turns out, the
predriver's own output stage is where two of the four findings live, so a bench
that had cut it off would have reported a very different — and wrong — result.

`WELL`, `TOP` and `BOT` are local nets inside `drv_slice`, not ports, and
`driver` instantiates `drv_slice` four times, so there are **four independent
floating wells**. All four are probed and reported separately, as are all eight
(gate, well) pairs — `XPA`/`XPB` are shared by three slices whose wells are
separate nets.

Each pad is fed through its own 0 V ammeter source, so each pad's current is
graded on its own against P4's per-pad limit; in Sweep B the two are not equal
and opposite.

### Convergence, and no bleeder was needed

The curated guidance anticipated that the N-side gates would be
high-impedance enough to need a bleeder resistor, with a sensitivity check on
its value. **It was not needed and none was added**: 27 of 30 units solved with
no convergence diagnostic at all. The N-side gates are not in fact floating —
each is the drain of a `pfet_01v8` whose n-well sits on VCCD = 0 V and of an
`nfet_01v8` whose bulk sits on VSSIO = 0 V, so the node is clamped to the 0 V
rails by two junctions rather than left open. Because no bleeder exists, there
is no bleeder-value sensitivity check to report; adding a resistor purely to
have something to sweep would have been a fabricated check. `.nodeset`/`.ic`
were not used either — they would preempt the well voltage row P4b measures.

Three Sweep A units (`tt`, `sf`, `ss` at −40 °C) emitted
`nonconvergence: "Warning: Dynamic gmin stepping failed"`. The request declares
`options.fail_on_diagnostic: ["nonconvergence"]`, so those three are graded
**`inconclusive`, not `fail`** — their solves are not trusted and their pad
currents are excluded from every range quoted below. That grading is not
cosmetic: `tt`/−40 °C returned a pad current of **4271.4 A**, which is
physically impossible and is a solver artifact of finding F1 below. The other
two returned 4.95 mA and 5.27 mA, consistent with their trusted neighbours, but
are still reported as inconclusive rather than cherry-picked.

The requests also declare `options.node_voltage_bounds: {min: -3.63, max: 3.63}`
as a trust guard on every measurement in volts: nothing in this bench can
legitimately leave that window (the DC sweeps drive at most 2.4 V against 0 V
rails; the ramp's powered hold reaches VDDIO = 3.30 V, and 3.63 V is the G75
window top). No unit tripped it — **every voltage result below, including at the
three inconclusive corners, is inside the plausible window and varies smoothly
with corner and temperature.** The pads are driven by ideal sources, so the
pathological current of F1 does not move the well or gate nodes; the row
P4a/P4b voltage evidence stands at all 10 Sweep A corners even where the
current magnitude does not.

## Row P4 — pad current: **FAIL**

Limit: ≤ ±20 µA per pad for 0 ≤ V_pad ≤ 2.4 V with VCCD = VDDIO = 0 V.
Graded on `ipadp_max`/`ipadp_min`/`ipadn_max`/`ipadn_min` (current into each
pad). **FAIL at all 17 graded corners** — 7 of 10 in Sweep A (3 inconclusive)
and 10 of 10 in Sweep B.

Sweep A, worst pad current per corner, with the rail it returns to:

| Corner | i_padp worst | → VSSIO | → VDDIO | → VCCD | Status |
|---|---|---|---|---|---|
| tt/−40 °C | 4271.4 A | 8542.7 A | 14.9 mA | 0.189 mA | **inconclusive** |
| sf/−40 °C | 4.95 mA | 13.62 µA | 9.76 mA | 0.122 mA | **inconclusive** |
| ss/−40 °C | 5.27 mA | 13.62 µA | 10.39 mA | 0.131 mA | **inconclusive** |
| ff/−40 °C | 9.99 mA | 13.62 µA | 19.72 mA | 0.253 mA | fail |
| fs/−40 °C | 10.43 mA | 13.62 µA | 20.58 mA | 0.265 mA | fail |
| tt/125 °C | 443.75 A | 887.48 A | 24.6 mA | 0.162 mA | fail |
| sf/125 °C | 443.75 A | 887.48 A | 18.7 mA | 0.108 mA | fail |
| ff/125 °C | 443.76 A | 887.48 A | 29.0 mA | 0.214 mA | fail |
| ss/125 °C | 443.75 A | 887.48 A | 18.6 mA | 0.114 mA | fail |
| fs/125 °C | 443.76 A | 887.48 A | 27.6 mA | 0.223 mA | fail |

The rail decomposition is what makes this diagnosable, and it separates two
independent defects:

- **The VSSIO column is finding F1** — the pad-cell ESD diode's area
  parameter. It is violently temperature-dependent (13.62 µA at −40 °C,
  887.48 A at 125 °C for the pair) because it is a junction reverse saturation
  current, and at 125 °C it is not a physically meaningful number at all.
- **The VDDIO and VCCD columns are findings F2 and F3** — the driver's own
  back-power — and they are **not** dominated by F1. At −40 °C, where the F1
  term collapses to 13.62 µA, the pad still draws **9.99–10.43 mA** at the
  trusted corners, essentially all of it into VDDIO. That is **500× the ±20 µA
  limit from the driver alone**, independent of the pad-cell defect.

Sweep B (all 10 graded, all fail). At −40 °C, where F1 is negligible, the worst
pad current is **0.235–1.75 mA**, still 12×–87× the limit; at 125 °C it is
443.74 A. `vcms` sits at exactly 1.25 V at every corner, confirming the
common-mode sense resistors are an active pad-to-pad divider (finding F4).

The mildest condition measured anywhere is the ramp's static state (both pads
at 1.25 V, −40 °C): 8.03–72.4 µA per pad. Even that exceeds ±20 µA.

## Row P4a — junction forward bias, per device: **FAIL**

Limit: every p+/n-well and n-well/p-substrate junction of the pad-facing
devices reverse-biased or ≤ 0.3 V forward, reported per device. Ranges are over
the 7 trusted Sweep A corners and all 10 Sweep B corners; `xsl_main` is quoted,
with the e-slice spread in the last column.

| Device(s) | Junction | Measurement | Sweep A | Sweep B | Limit | Verdict |
|---|---|---|---|---|---|---|
| `XMSPA` drain, `XMWPA` source | p+/n-well, pad to WELL | `ja_<s>_mspa_d` | 0.440–0.504 V | 0.255–0.489 V | 0.3 V | **FAIL** |
| `XMSPB` drain, `XMWPB` source | p+/n-well, pad to WELL | `ja_<s>_mspb_d` | 0.440–0.504 V | 0.255–0.489 V | 0.3 V | **FAIL** |
| `XMSPA`/`XMSPB` source | p+/n-well, TOP to WELL | `ja_<s>_msp_s` | 0.011–0.051 V | ≤ 0.051 V | 0.3 V | pass |
| `XMWVA`/`XMWVB` source | p+/n-well, VCCD to WELL | `ja_<s>_mwv_s` | ≈ 0 (< 1e-18 V) | ≈ 0 | 0.3 V | pass |
| `XMGTA` drain | p+/n-well, GPA to WELL | `ja_<s>_mgta_d` | ≈ 0 (< 2e-18 V) | ≈ 0 | 0.3 V | pass |
| `XMGTB` drain | p+/n-well, GPB to WELL | `ja_<s>_mgtb_d` | ≈ 0 | ≈ 0 | 0.3 V | pass |
| all WELL-bulk devices | n-well/p-substrate | `ja_<s>_nwsub` | ≈ 0 | ≈ 0 | 0.3 V | pass |
| `XMSNA`/`XMSNB` drains (×4 slices), pad-cell `XD1` anode, `XMESD` drain | n+/p-substrate | `ja_nsub_padp`, `ja_nsub_padn` | 0 V | −0.9 V | 0.3 V | pass |
| predriver `XMP_3pma`/`XMP_3pmb` drains | p+/n-well, GPA/GPB to VCCD | `ja_pre_gpa`, `ja_pre_gpb` | 0.410–0.675 V | 0.306–0.614 V | 0.3 V | **FAIL** |
| predriver `XMP_3pea`/`XMP_3peb` drains | p+/n-well, XPA/XPB to VCCD | `ja_pre_xpa`, `ja_pre_xpb` | 0.683–0.973 V | 0.550–0.737 V | 0.3 V | **FAIL** |
| predriver `XMP_3nma`/`XMP_3nmb`/`XMP_3nea`/`XMP_3neb` drains | p+/n-well, N-side gates to VCCD | `ja_pre_gna` etc. | ≈ 0 | ≈ 0 | 0.3 V | pass |

Two things are worth separating here.

**What DR-008 got right.** Every n+/p-substrate junction stays reverse-biased
at every corner — 0 V forward in Sweep A, −0.9 V in Sweep B. That is exactly
DR-008's claim that "the bottom NMOS switches' n+ drains sit in the grounded
p-substrate and are reverse-biased for any positive pad voltage, so they need
no measure beyond a gate held low", and it covers the ESD diode and snapback
NMOS too. The well-switch and gate-tracking devices' own junctions, and every
n-well/p-substrate junction, are likewise clean to within numerical noise.

**What it did not cover.** The pad-to-WELL junction misses 0.3 V by
0.14–0.20 V at every corner, because the well follows the pad one PMOS V_T
behind it rather than exactly (row P4b, below). And the predriver's output-stage
PMOS devices — whose drains *are* the eight switch-gate nets, and whose n-wells
sit on VCCD = 0 V — are forward-biased by up to 0.973 V. Those devices are not
in DR-008's pad-facing device list at all; this bench says they belong there.

## Row P4b — well and gate tracking: **FAIL**

### Floating well within 0.3 V of max(VCCD, V_pad): **FAIL**

| Quantity | Sweep A (7 trusted) | Sweep B (10) | Limit | Verdict |
|---|---|---|---|---|
| `wt_main` (xsl_main) | 0.440–0.504 V | 0.255–0.489 V | 0.3 V | **FAIL** |
| `wt_e0` / `wt_e1a` / `wt_e1b` | 0.422–0.517 V | 0.253–0.498 V | 0.3 V | **FAIL** |
| `well_main_max` at V_pad = 2.4 V | 1.896–1.960 V | — | (reported) | — |
| `well_e0_max` at V_pad = 2.4 V | 1.883–1.979 V | — | (reported) | — |

**The mechanism works; the tolerance does not.** The well does follow the pad —
it reaches 1.88–1.98 V when the pad is at 2.4 V, and in the ramp it rises to
1.42–1.80 V when VCCD reaches 1.80 V, so the `XMWVA`/`XMWVB`/`XMWPA`/`XMWPB`
pair tracks max(VCCD, V_pad) in both directions as DR-008 §1 specifies. It
tracks it through a PMOS source follower, so it lags by roughly a threshold,
and 0.44–0.52 V of lag misses a 0.3 V criterion. This is a tolerance miss on a
working mechanism, not a broken mechanism, and it is the mildest of the four
findings.

The three e-slices' wells agree to every reported digit at every corner. The
curated guidance flagged that `XPA`/`XPB` are shared by three slices with
separate wells and that a divergence between them would be the interesting
result; there is no divergence.

### Every top-switch gate within 0.3 V of its well: **FAIL**

All eight (gate, well) pairs, reported individually:

| Pair | Gate net | Sweep A (7 trusted) | Sweep B (10) | Limit | Verdict |
|---|---|---|---|---|---|
| `gw_main_a`, `gw_main_b` | GPA, GPB | 1.285–1.498 V | 0.637–0.831 V | 0.3 V | **FAIL** |
| `gw_e0_a`, `gw_e0_b` | XPA, XPB | 0.997–1.261 V | 0.489–0.646 V | 0.3 V | **FAIL** |
| `gw_e1a_a`, `gw_e1a_b` | XPA, XPB | 0.997–1.261 V | 0.489–0.646 V | 0.3 V | **FAIL** |
| `gw_e1b_a`, `gw_e1b_b` | XPA, XPB | 0.997–1.261 V | 0.489–0.646 V | 0.3 V | **FAIL** |

This is finding F3 and it is the most consequential result in this record:
**DR-008's gate tracking is defeated as netlisted.** The gate-tracking PMOS
does its job — `ja_<s>_mgta_d` shows GPA never rises above its well — but it
cannot pull the gate up to the well, because the predriver's output PMOS has
its n-well on VCCD = 0 V and its p+ drain/n-well junction clamps the gate at
0.41–0.68 V (GPA/GPB) or 0.68–0.97 V (XPA/XPB) while the well is at 1.9 V. The
gate therefore sits 1.3–1.5 V *below* its well, the top switch is not off, and
the pad has a path through it to TOP — which is where the 10 mA into VDDIO of
finding F2 comes from. DR-008 §2 specifies the gate-tracking device but its
device list gives the predriver output stage no floating well and no isolation,
so the mechanism has nothing to hold the gate against.

### Every thin-oxide terminal pair ≤ 1.98 V: **FAIL in Sweep A, pass in Sweep B**

The curated guidance flagged a genuine reading ambiguity in "every thin-oxide
terminal pair": taken literally it includes bulk-referenced pairs, which are
reverse-biased junctions rather than oxide stress. **Both readings are reported
and both agree on the verdict**, so the ambiguity does not need settling:

| Reading | Measurement | Sweep A | Sweep B | Limit | Verdict |
|---|---|---|---|---|---|
| gate-referenced (oxide stress): g-s, g-d, g-b of `XMSPA`/`XMSPB`/`XMSNA`/`XMSNB` | `tox_<s>_ox` | 2.400 V | 1.600 V | 1.98 V | **FAIL** / pass |
| channel pair: drain-source of the same four | `tox_<s>_ds` | 2.293–2.400 V | 1.534–1.600 V | 1.98 V | **FAIL** / pass |
| bulk-referenced, p-side | `tox_<s>_db` | 0.719–0.931 V | ≤ 0.489 V | 1.98 V | pass |
| bulk-referenced, N-side drain-bulk | `tox_nsub_padp`, `tox_nsub_padn` | 2.400 V | 1.600 V | 1.98 V | **FAIL** / pass |
| predriver output stage, gate-referenced | `tox_pre_ox` | 0.683–0.973 V | 0.550–0.737 V | 1.98 V | pass |
| predriver output stage, drain-to-rail | `tox_pre_ds` | 0.683–0.973 V | 0.550–0.737 V | 1.98 V | pass |

The worst gate-referenced pair is 2.400 V at every Sweep A corner, flat across
process and temperature because it is set by the stimulus: it is
|V(GNA) − V(PADP)| with `GNA` clamped at 0 V and the pad at its 2.4 V endpoint,
on `XMSNA OUTP GNA BOT VSSIO sky130_fd_pr__nfet_01v8` — a thin-oxide drain on
the pad with an untracked gate. That is exactly the exposure the curated
guidance predicted by hand (finding F5), now confirmed in simulation.
DR-008's gate tracking covers only the P-side gates; there is no N-side
equivalent in the committed netlist.

Because the criterion is driven by the pad endpoint, Sweep B — which only
reaches 1.6 V — passes it at every corner. The row's condition is the full
0–2.4 V range, so the Sweep A result is the governing one.

**Device scope of this check.** The thin-oxide devices able to see a nonzero
terminal voltage in the unpowered state are the pad-reachable ones: the four
slices' top switches and pull-downs, and the predriver output stage whose
drains are the switch gates. That is asserted as evidence rather than argument:
`core_max`, the worst voltage on the predriver's pre-output thin-oxide chain
(`g_ma`, `g_mb`, `s1_*`, `s2_*`) and the three `drv_sel` bias outputs, is
**≤ 1.04e-18 V at the 7 trusted Sweep A corners and ≤ 2.54e-13 V in Sweep B**
— zero to numerical noise. At the three inconclusive Sweep A corners it reaches
0.32–0.48 mV, which is still five orders below any stress of interest and is
consistent with those solves' own residual rather than with a real bias.
Nothing deeper in the core is stressed.

### Supply ramp, ±1 mA excursion: **covered — passes on the excursion reading**

The ramp was run, not omitted. VCCD 0 → 1.80 V and VDDIO 0 → 3.30 V over 1 ms,
a 0.2 ms hold at nominal, 1 ms back down, pads held at 1.25 V throughout
(nominal rails per `spec/target-spec.md` lines 60–62).

The row bounds the pad-current **excursion** over the ramp, so two numbers are
reported: the graded absolute current, and the excursion above the static
pre-ramp current at t = 0.

| Corner | static i_padp (t = 0) | worst i_padp | excursion, pad P | excursion, pad N | WELL at hold | Graded |
|---|---|---|---|---|---|---|
| tt/−40 °C | 14.23 µA | 14.23 µA | 0 | 8.82 µA | 1.541 V | pass |
| sf/−40 °C | 8.03 µA | 8.03 µA | 60 pA | 77.3 nA | 1.415 V | pass |
| ff/−40 °C | 37.10 µA | 37.10 µA | 0 | 43.8 µA | 1.774 V | pass |
| ss/−40 °C | 8.82 µA | 8.83 µA | 3.13 nA | 1.21 µA | 1.425 V | pass |
| fs/−40 °C | 72.39 µA | 72.39 µA | 0 | 167.6 µA | 1.798 V | pass |
| tt/125 °C | 443.73 A | 443.73 A | 0 | 0 | 1.799 V | **fail** |
| sf/125 °C | 443.73 A | 443.73 A | 0 | 0 | 1.788 V | **fail** |
| ff/125 °C | 443.73 A | 443.73 A | 0 | 0 | 1.800 V | **fail** |
| ss/125 °C | 443.73 A | 443.73 A | 0 | 0 | 1.794 V | **fail** |
| fs/125 °C | 443.73 A | 443.73 A | 0 | 0 | 1.797 V | **fail** |

**On the excursion reading the criterion passes at all 10 corners**: the worst
excursion anywhere is 167.6 µA, against a ±1 mA bound. The five 125 °C failures
are the *static* 443.73 A offset of finding F1 — the ramp contributes exactly
zero excursion there — so they are a restatement of the P4 failure, not a
separate dynamic problem. The ramp also gives the clearest positive evidence
for DR-008 §1: the floating well rises to 1.42–1.80 V at the powered hold,
tracking VCCD = 1.80 V, and returns on the way down.

## Findings

Recorded as evidence. **No fix is applied here** — the issue's Out of Scope
list forbids changing the schematics, device sizes or `spec/`, and the repo
rule is that agents do not relax a ratified spec to make a row pass. Each
finding names the follow-up it owes.

### F1 — pad-cell ESD diode area/perimeter are ~11 orders of magnitude out (blocking)

`design/pad_cell/pad_cell.spice` (and `pad_cell.sch`, where it originates):

```
XD1 VSSIO PAD sky130_fd_pr__diode_pw2nd_11v0 area=4e14 perim=8e7
```

sky130's diode model carries the unit conversions internally —
`cj = '0.0008512*1e-12*…'` F/m² and `cjsw = '8.5204e-011*1e-6*…'` F/m in
`sky130_fd_pr__diode_pw2nd_11v0.model.spice` — so the instance parameters are
in **µm² and µm**. `area=4e14` is therefore 4 × 10¹⁴ µm² = 4 × 10⁸ mm².

Measured consequences (single-corner local probes at `tt`, 27 °C, plus the
recorded grid):

| `area` / `perim` | reverse current at V = 2.4 V | junction capacitance at 1.25 V |
|---|---|---|
| `4e14` / `8e7` (committed) | **107.4 mA** | **0.252 F** |
| `4` / `8` (a ~4 µm² junction) | 2.40 pA (at ngspice's gmin floor) | — |
| `1400` / `150` (~1400 µm², sized to row P1's 1.2 pF pad+ESD allocation) | 2.78 pA (gmin floor) | 0.894 pF |

Across the recorded grid the committed value gives 13.62 µA at −40 °C and
887.48 A at 125 °C for the pad pair — a junction reverse saturation current's
exponential temperature dependence, not a leakage spec.

This defect is not confined to row P4. A 0.252 F pad capacitance is 11 orders
above row **P1**'s 1.2 pF pad + ESD allocation, so any P1 result computed from
this netlist is also void. And it is what makes three Sweep A units
numerically untrustworthy: driving a ~10²–10³ A ideal junction from an ideal
voltage source is what "Dynamic gmin stepping failed" and the 4271.4 A artifact
are about.

**Owed**: a follow-up issue against `design/pad_cell/` to establish the
intended ESD diode geometry and correct `area`/`perim` in the schematic, then
re-run this bench. Until then the *magnitudes* in the P4 table above are not
usable as leakage figures — though the **verdicts** stand, because F2 and F3
alone exceed the limit by 500× at the corners where F1 is negligible.

### F2 — the driver back-powers VDDIO through the current source's grounded n-well

At −40 °C, where F1 contributes 13.62 µA, each pad still draws 9.99–10.43 mA at
the trusted corners and `i(VDDIO)` carries 19.72–20.58 mA — the whole of it.

The path: the top switch is not off (F3), so the pad drives the switch source
node `TOP`; `XMPS TOP PG VDDIO VDDIO sky130_fd_pr__pfet_g5v0d10v5` has its
n-well on VDDIO = 0 V, so its p+ drain/n-well junction conducts from `TOP` into
the grounded rail. DR-008 §4 states that "the current source needs no measure
of its own … with both switches off that node has no DC path from the pad, and
the device's own n-well is at VDDIO = 0 V with its drain floating". The premise
"with both switches off" does not hold, so neither does the conclusion. In
`xsl_main` the device is `mult=11`, so this is the largest single path.

**Owed**: an amendment to `DR-008` (a new decision record, per the repo rule
that a change to these rows is a new decision record) addressing the current
source's well in the unpowered state — or establishing that fixing F3 alone
closes it, since with the switches genuinely off the premise is restored.

### F3 — gate tracking is defeated by the predriver's grounded output-stage n-well

All eight (gate, well) pairs miss the 0.3 V criterion by 0.7–1.5 V. The
gate-tracking PMOS pulls each P-side gate toward its well, but the predriver's
output PMOS (`XMP_3pma`/`XMP_3pmb`/`XMP_3pea`/`XMP_3peb`, all `pfet_01v8`) has
its n-well on VCCD = 0 V, and its p+ drain/n-well junction clamps that same
gate node 0.41–0.97 V above ground. The gate cannot reach the well, the top
switch stays on, and 0.11–0.27 mA flows into VCCD through the clamp.

DR-008 §2 specifies the gate-tracking device; its device list does not give the
predriver output stage a floating well or any isolation from the lifted gate
node. This is the root cause of the P4b gate criterion, and — through F2 — of
most of the P4 current at the corners where F1 is negligible.

**Owed**: the same `DR-008` amendment. This is the one to fix first: it is
upstream of F2.

### F4 — the common-mode sense resistors are a real pad-to-pad path, but not the dominant one (confirmed, minor)

The curated guidance traced `XRS1`/`XRS2` (`res_high_po_1p41`, `L=15`) by hand
to ≈ 3.71 kΩ each, ≈ 7.41 kΩ pad to pad, giving ≈ 94 µA at Sweep B's 0.7 V
differential. The mechanism is confirmed: `vcms` sits at exactly 1.25 V at every
Sweep B corner, which is the resistive divider's mid node and could not happen
otherwise.

The magnitude is not the limiting term. `idiff` — the differential half of the
pad current, (i_padp − i_padn)/2, in which anything returning to a rail cancels
and only a pad-to-pad path survives — measures **0.165–0.929 mA at −40 °C** and
18.3–19.7 mA at 125 °C, against the ≈ 94 µA the resistors alone predict. The
rest is pad-to-pad leakage through the switch devices (PADP–TOP–PADN and
PADP–BOT–PADN), i.e. F3 again. In Sweep A `idiff` is ≤ 3.7e-13 A, zero by
symmetry, which is the cross-check that the decomposition is sound.

**Owed**: nothing on its own. It is subsumed by the F3 follow-up; recorded so
the hand-traced prediction is marked confirmed-but-not-dominant rather than
left open.

### F5 — N-side thin-oxide exposure (confirmed)

Confirmed as predicted: the worst gate-referenced thin-oxide pair is 2.400 V at
every Sweep A corner, set by |V(GNA) − V(PADP)| on `XMSNA` with `GNA` at 0 V
and the pad at 2.4 V, against the 1.98 V ceiling. Covered by the F3/DR-008
amendment, which has to decide whether the N-side gates get tracking of their
own.

### F6 — an untracked `~/.spiceinit` was deciding device sizing (evidence hygiene, fixed here)

Not a design finding, but it nearly produced a wrong record and it affects
other benches in this repo.

ngspice's `wnflag` decides whether a BSIM device's `W` is the total width
(divided among `nf` fingers) or the width of each finger. This host had
`set wnflag=1` in an untracked `~/.spiceinit`, so the first local run of this
bench passed while a batch unit on a **byte-identical ngspice-47 build** aborted
with `Fatal: Vsat at current temperature = -4117.03 is not positive` during
BSIM4v5.5.0 parameter checking — the wrong value selects a different model bin
for `sky130_fd_pr__esd_nfet_g5v0d10v5`, and that bin's `vsat_diff` drives
`vsat` negative.

`wnflag=1` is this netlist's own convention, established from the committed
geometry rather than from documentation: `XMSPA` (`W=3.6`, `nf=4`) carries
`ad=0.522 as=0.783 pd=4.76 ps=7.14`, which is exactly 0.29 µm of diffusion
extension on a 3.6/4 = 0.9 µm finger — the per-finger reading of `W` overstates
all four by 4×. `XMPS` (`W=12.8`, `nf=2`) agrees at 2×, and the `nf=1` devices
pin the 0.29 µm extension itself. All three requests therefore declare
`options.ngspice_init: ["set wnflag=1"]`, which `klt sim` materializes as a
per-corner `.spiceinit`. With it declared, the bench gives identical results on
a local run with `$HOME` neutralized and on the fleet.

**Owed**: a follow-up to declare the same setting in `sim/pdk-smoke/request.json`.
That bench's recorded numbers are **not** affected — every device in it is
`nf=1`, where the two readings coincide — but the omission is latent for any
future multi-finger bench that copies it as a template.

## Tool notes

Three corrections to the curated guidance, recorded because they cost time and
because the first is the opposite of what the issue predicted.

**`klt sim` does stage the netlist's own `.include` closure.** The issue
expected it might not, and provided for a `build-deck.sh` fallback plus a
friction filing at `2AMLogic/klayout-tools`. Neither is needed and neither was
done. The batch report's `environment.netlist_closure` lists all three files,
two levels deep and resolved against each file's own directory:

```
sim/unpowered-pad/tb_sweep_a.spice      f6c6e439…
sim/unpowered-pad/tb_unpowered.spice    b1bb6c53…
design/lvds_tx_analog.spice             e4e96a1b…
```

The dry-run observation behind the concern was sound but misread:
`staged_files` reports the `options.stage_model_inputs` closure only (319
entries, all `models.lib`), while the netlist closure is a separate mechanism
reported under `environment.netlist_closure`. `docs/cli/sim.md` documents it as
"Off-host backends stage the netlist's `.include` closure".

**Pinning the PDK root: `$PDK_ROOT`, not `models.pdk_root`.** Two installs on
this host provide variant `sky130A` (`~/.ciel`, the pinned one, and
`~/.volare`) and `klt` resolves first-match-wins, so the root does need
pinning. But `models.pdk_root` — and the `--pdk-root` flag that folds into it —
is **refused on the batch backend** (`models_pdk_root_host_path`): it is a
submitting-host path and is forwarded verbatim to a runner where it does not
exist. The client-side pin that backend accepts is the `$PDK_ROOT` environment
variable, which is why the reproduce command above sets it and the request
files do not carry the field. `klt` still warns about the skipped install on
every run; the warning is expected and the pinned library's sha256 in the table
above is the check that matters.

**`environment.ngspice_init` is not echoed** in this `klt` version's report
(the field is `null` even when the setting is in force and demonstrably
effective). Provenance for finding F6's setting is therefore the committed
`request-*.json` files and their content hashes, not the report.

## Caveats

- **Simulated, pre-layout, and against a proposed spec.** Schematic netlist
  (`netlist_source: "schematic"`); no extraction, no post-layout, no silicon.
  Rows P4–P4b are proposed figures under `DR-008`, not ratified limits.
- **The P4 current magnitudes are not usable leakage figures** until finding
  F1 is corrected, and three Sweep A units are graded `inconclusive` for that
  reason. The P4/P4a/P4b **verdicts** do not depend on F1: findings F2 and F3
  exceed the P4 limit by 500× at the corners where F1 is negligible, and every
  P4a/P4b voltage result is inside the declared plausibility window at all 10
  corners.
- **Row P2 (ESD adequacy) is untouched** — not provable by simulation, per the
  spec's own verification column.
- **The worker image carries its own sky130A** at a different open_pdks
  revision than the pin. `options.stage_model_inputs: true` ships the pinned
  `sky130.lib.spice` and its 319-file closure with every job, so the executed
  models are the pinned ones. This `klt` version's report does not populate a
  `pdk_stamp_comparison` field; the evidence that staging took effect is
  `environment.staged_model_inputs` (319 entries, `source_sha256`
  `17c208a6…e075f64` matching the pinned library) in each
  `results/report-*.json.gz`.
- **No Monte Carlo.** Rows P4–P4b are deterministic over the process grid;
  DR-008 says so explicitly ("the limits are leakage bounds, not matching").
- **Reproducibility checked.** The grid was run twice on the fleet, in
  independent job sets, and the two runs agree on **all 2000 recorded values
  bit-for-bit** (890 + 890 + 220). The second run is the one recorded here;
  the first differed only in `options.timeout_s`, which was lowered from
  900/3600 s to 120 s so the fleet's conservative whole-job bound
  (timeout × units + 120 s) fits inside its 3600 s ceiling. Observed per-unit
  runtime is 11–12 s.
- Reproduce: `PDK_ROOT=~/.ciel klt sim --batch-set sim/unpowered-pad/request-sweep-a.json
  sim/unpowered-pad/request-sweep-b.json sim/unpowered-pad/request-ramp.json
  --wait-for-capacity 600 --capacity-retries 2 -o <outdir> --report-out <path>`.
  Exit 4 (Sweep A, `inconclusive`) and exit 3 (Sweep B, ramp, `fail`) are the
  expected codes, not errors.
