# sky130-lvds-tx target specification

- **Status**: **PROPOSED — not ratified.** Agents do not ratify their own
  spec. This document and its decision records `DR-001`…`DR-007` land marked
  *proposed*; the status flips to *ratified* only on human merge approval of
  the pull request that carries them, recorded in the table below.
- **Date**: 2026-10-17 (drafted from issue #2)
- **Written by**: builder agent (issue #2)
- **Block class**: mixed-signal LVDS-class transmitter: synthesized serializer
  plus a custom current-steering driver and pad cell.

| Ratification record | |
|---|---|
| Ratified by (human) | *not yet* |
| Date | *not yet* |
| Pull request | *not yet* |

## How to read this file

Every row has a **target**, a **fallback** (400 Mb/s), a **stretch** (1.5 Gb/s
or the low-swing mode), a **verification method**, the **PVT corners** it
holds at, and whether it is **deterministic** or **statistical**. `—` means no
value is set for that column, not that one is implied.

- **No claim without a testbench.** A row is a requirement, not a result.
  Verification methods marked *analysis* are arithmetic from stated inputs;
  *simulated* means a testbench exists later and eye diagrams are always labelled
  *simulated*; *measured* means silicon.
- **Numbers that are not published say so.** Where the PDK or a sibling does not
  publish a figure, the row says "not published" and names how it will be
  obtained. No figure here is invented to fill a cell.
- **Standards.** The V_OD, V_OS, ΔV_OD, ΔV_OS and short-circuit numbers follow
  the TIA/EIA-644 windows as quoted in public vendor application literature and
  in this repo's README draft; the standard's text was **not** read for this
  spec (it is licensed), and the numbers are to be checked against a licensed
  copy at ratification. The literature read: TI SLLA038B *Interface Circuits
  for TIA/EIA-644 (LVDS)* (247–454 mV into 100 Ω, 1.2 V typical offset,
  1.923 Gb/s theoretical maximum); TI SNLA165 / AN-971 *An Overview of LVDS
  Technology* (655 Mb/s recommended maximum, 1.923 Gb/s theoretical maximum
  "based on a loss-less media"); and the SN65LVDS31 datasheet SLLS261N §7.5, a
  part sold as meeting TIA/EIA-644, for ΔV_OD, ΔV_OC(SS), V_OC(PP) and the two
  short-circuit limits (E3, E4, E7). **The 1 Gb/s target and the 1.5 Gb/s
  stretch are above the standard's 655 Mb/s recommended maximum and below its
  1.923 Gb/s theoretical maximum**: the windows are followed at a rate the
  standard does not recommend, which is one more reason no compliance claim is
  made. The low-swing mode is described only as "D-PHY-class":
  the MIPI specifications are licensed, nothing from them was read or copied,
  and its numbers are this repo's own. **This block makes no compliance or
  conformance claim against either standard**; rows state numbers and name the
  window they follow.
- **Spec changes go through a decision record.** Results that miss a row are
  recorded as misses; the row is not edited to match.

### The PVT grid (all rows unless stated)

The grid is **G75**: process `tt, ff, ss, sf, fs` (the five standard corners,
as `sky130-pll` DR-003 ratified) × temperature −40, 27, 125 °C × supply pairs
(VCCD, VDDIO) ∈ {(1.62, 2.97), (1.80, 3.30), (1.98, 3.63), (1.62, 3.63),
(1.98, 2.97)} V = 75 conditions (`DR-002` §4). VCCD is the 1.8 V core rail
(±10 %, as `sky130-pll` row 1); VDDIO is the 3.3 V I/O rail (±10 %).
Statistical rows additionally run a **local-mismatch Monte Carlo** (population
proposed N ≥ 200) at `tt`/27 °C/1.80 V/3.30 V and at the two extreme
conditions `ss`/125 °C/1.62 V/2.97 V and `ff`/−40 °C/1.98 V/3.63 V.
Standard-cell Liberty corners stop at 100 °C; 125 °C standard-cell data is
**not published** and comes from SPICE or a stated derate.

### Rows marked statistical

Statistical (Monte Carlo local mismatch): **E1, E2, E3, E4, D2, D3**.
Statistical (transient noise, not mismatch): the random part of **C4**.
Every other row is **deterministic** over G75 and needs no Monte Carlo.

### The mixed-signal partition boundary (one sentence, for the manifest's `partition_boundary`)

> Everything from the 8-bit parallel-word capture register through the 8:1→2:1
> shift/load reduction stage and the ÷4 word counter is synthesized
> `sky130_fd_sc_hd` standard-cell logic on the 1.8 V core rail, and the 2:1 DDR
> retiming multiplexer, the predriver, the current-steering driver with its
> common-mode feedback and pre-emphasis, and the pad cell with its ESD network
> are custom analog.

## Decisions this spec rests on

| Record | Decision |
|---|---|
| `DR-001` | custom pad cell on the PDK `analog_noesd_pad` frame, ESD to VSSIO only; stock `analog_esd_pad` is the named fallback |
| `DR-002` | switches and predriver on 1.8 V core devices, current source/sink on 3.3 V I/O devices, no level shifter in the data path; CMFB on V_OS |
| `DR-003` | 8:1 serialization, 500 MHz DDR forwarded clock; 7:1 is a stretch |
| `DR-004` | `gf180-tmds-tx` serializer not imported (ratio and boundary logic differ); its micro-architecture adopted |
| `DR-005` | low-swing mode is a separate driver slice, not designed now; 0.3 pF allocated |
| `DR-006` | 1 Gb/s kept as target with a first-order edge and timing budget; 1.5 Gb/s needs a split |
| `DR-007` | 500 MHz clock specified as an interface; gap to `sky130-pll` recorded and filed on it |

---

## Rate and lanes

| ID | Parameter | Target | Fallback | Stretch | Verification | PVT | Type |
|---|---|---|---|---|---|---|---|
| R1 | Rate per lane | 1 Gb/s (UI 1000 ps) | 400 Mb/s (UI 2500 ps) | 1.5 Gb/s (UI 667 ps) | simulated eye at the pad (E9) and serializer STA (S3) | G75 | det. |
| R2 | Lanes | 4 data + 1 forwarded clock | 1 data + 1 clock | 8 data + 1 clock | structural: netlist and LVS pin/instance count | n/a | det. |
| R3 | Forwarded-clock format | DDR: clock at half the bit rate (500 MHz), 50 % duty, both edges sample; the clock lane is driven through the same serializer and driver with a fixed `10101010` word | same at 200 MHz | 7:1 option with word-rate clock (`DR-003`) | simulated: clock-lane eye vs data-lane eye, edge alignment | G75 | det. |

The word boundary is not carried by a DDR clock; a receiver needs a training
pattern or frame marker at a protocol layer this block does not provide.

## Electrical

All outputs measured into a 100 Ω differential load across the pair.

| ID | Parameter | Target | Fallback | Stretch | Verification | PVT | Type |
|---|---|---|---|---|---|---|---|
| E1 | Differential output voltage V_OD | 247–454 mV; design nominal 350 mV (3.5 mA × 100 Ω); follows TIA/EIA-644 | same | same | simulated DC/transient at the pad | G75 + MC | stat. |
| E2 | Output common mode V_OS | 1.125–1.375 V; design nominal 1.2 V ± 75 mV (`DR-002` §3); follows TIA/EIA-644 | same | same | simulated DC/transient at the pad | G75 + MC | stat. |
| E3 | Change in V_OD between complementary states ΔV_OD | ≤ 50 mV (public vendor literature value) | same | same | simulated, both states, same condition | G75 + MC | stat. |
| E4 | Change in V_OS: steady-state between complementary states ΔV_OS, and dynamic peak-to-peak V_OS(PP) | ΔV_OS ≤ 50 mV; V_OS(PP) ≤ 150 mV (public vendor literature values: SN65LVDS31 §7.5 ΔV_OC(SS) ±50 mV, V_OC(PP) 150 mV max) | same | same | simulated: DC in both states for ΔV_OS; transient with PRBS-7 for V_OS(PP) | G75 + MC | stat. |
| E5 | Rise/fall time, 20–80 %, at the pad into 100 Ω ‖ 1.0 pF per side | 100–400 ps (upper bound = 0.4 UI; lower bound proposed to limit coupling, not from a standard) | 100 ps–1.0 ns (0.4 UI) | 100–267 ps (0.4 UI) | analysis (`DR-006`) then simulated transient | G75 | det. |
| E6 | Small-signal differential output impedance, at the V_OS window | ≥ 2 kΩ (load error ≤ 5 %) | ≥ 1 kΩ | — | simulated AC | G75 | det. |
| E7 | Output short-circuit current | either output shorted to ground: \|I\| ≤ 24 mA; the two outputs shorted together (V_OD = 0): \|I\| ≤ 12 mA (public vendor literature values: SN65LVDS31 §7.5 I_OS, −24 mA max at V_O = 0 and ±12 mA max at V_OD = 0); no device over its rating | same | same | simulated DC, both shorts | G75 | det. |
| E8 | Output shorted to VDDIO, or over-voltage above 1.98 V on a thin-oxide switch node | **not targeted: documented limitation** (thin-oxide switches, `DR-002`) | — | — | analysis; stated limitation | n/a | det. |
| E9 | Simulated differential eye at the pad (PRBS-7), into 100 Ω ‖ 1.0 pF per side | width at 0 V differential ≥ 0.75 UI; height at the sampling point ≥ 150 mV | width ≥ 0.6 UI; height ≥ 120 mV | width ≥ 0.6 UI; height ≥ 120 mV | **simulated** eye diagram, labelled so; no silicon claim | G75 | det. |

E1 and E2 jointly: the window must hold with the pre-emphasis settings of D3
and with the CMFB of D2 at every G75 condition and Monte Carlo draw.

## Driver

| ID | Parameter | Target | Fallback | Stretch | Verification | PVT | Type |
|---|---|---|---|---|---|---|---|
| D1 | Topology | current-steering H-bridge: top source, two switch pairs, bottom sink (`DR-002`) | same, no pre-emphasis | plus a separate low-swing slice (`DR-005`) | design review; schematic vs LVS | n/a | det. |
| D2 | Common-mode feedback | holds V_OS at 1.2 V ± 75 mV; loop phase margin ≥ 45° | V_OS ±125 mV (full window), phase margin ≥ 45° | — | simulated loop gain (AC) and transient; offset under MC | G75 + MC | stat. |
| D3 | Pre-emphasis range | 0 to 2 dB, ≥ 4 settings; the E1 window holds at every setting | 0 dB (disabled) | 0 to 4 dB | simulated transient per setting; accuracy under MC | G75 + MC | stat. |
| D4 | Device flavours and supply per rail | switches/predriver: `nfet_01v8`/`pfet_01v8` on VCCD 1.8 V ± 10 %; current source/sink: `nfet_g5v0d10v5`/`pfet_g5v0d10v5` on VDDIO 3.3 V ± 10 %; no level shifter in the data path | same | same | netlist review; per-device voltage-stress check in every simulation | G75 | det. |

D3's upper bound is limited by the E1 window itself: 454/247 mV is 5.3 dB
before any tolerance, so 2 dB leaves room for the ±75 mV V_OS and mismatch.

## Low-swing stretch mode (D-PHY-class)

Stretch only; **does not drive the baseline architecture** (`DR-005`).

| ID | Parameter | Target | Fallback | Stretch | Verification | PVT | Type |
|---|---|---|---|---|---|---|---|
| L1 | Differential swing and common mode | — | — | ≈ 200 mV differential swing around a low common mode of ≈ 0.2 V (this repo's own numbers) | simulated | G75 | det. |
| L2 | Driver sharing | — | — | separate slice on the same pad, ≤ 0.3 pF of the P1 budget | design review; extracted capacitance | G75 | det. |

## Serializer

| ID | Parameter | Target | Fallback | Stretch | Verification | PVT | Type |
|---|---|---|---|---|---|---|---|
| S1 | Ratio and parallel-word width | 8:1; 8-bit word at 125 MHz (the ÷4 of the 500 MHz clock is an output of this block) | 8:1 at 400 Mb/s (word clock 50 MHz) | 7:1 option; or a split reduction for 1.5 Gb/s (`DR-006`) | cocotb: bit order, word boundary, no dropped or repeated bit | n/a | det. |
| S2 | Partition | the boundary sentence above: standard cells to the 8:1→2:1 reduction, custom from the DDR mux onward | same | same | design review; netlist hierarchy | n/a | det. |
| S3 | Reduction-stage timing at the 500 MHz clock | first-order floor 1.451 ns vs 2.000 ns period (0.549 ns, 27 % slack) from `sky130_fd_sc_hd__ss_100C_1v60`; **STA setup slack ≥ 0 with 10 % clock uncertainty at every Liberty corner** | 200 MHz: 71 % slack | 750 MHz does **not** close (−0.118 ns) | analysis now (`DR-006`), then STA after synthesis | Liberty corners; 125 °C not published | det. |
| S4 | Reuse | `gf180-tmds-tx` serializer not imported; micro-architecture adopted (`DR-004`) | — | — | decision record; `in_tree` ledger entry owed by the RTL issue | n/a | det. |

## Pads and ESD

Pad cell basis, options and the evidence read are in `DR-001`.

| ID | Parameter | Target | Fallback | Stretch | Verification | PVT | Type |
|---|---|---|---|---|---|---|---|
| P1 | Pad capacitance per pad (pad + ESD + driver drains; excludes receiver and package) | ≤ 2.0 pF, allocated pad + ESD ≤ 1.2 pF, LVDS driver drains ≤ 0.5 pF, low-swing slice ≤ 0.3 pF (`DR-005`). **Published figures (references only)**: `sky130_fd_io__top_analog_pad` `pad`/`pad_core` 1.061 pF (Liberty, 20 of 34 corner files; whether it describes the ESD-bearing `ef_io__analog_*` wrappers is unverified, `DR-001`) and the GPIO `PAD` pin 1.05–1.16 pF; the `ef_io__analog_*` wrappers publish none. The pad + ESD ≤ 1.2 pF allocation leaves ~0.14 pF over the 1.06 pF reference | ≤ 3.0 pF | ≤ 1.5 pF | post-layout parasitic extraction of the drawn cell, at the pad's 1.0–1.6 V bias; tool owed | process corners, extraction corners | det. |
| P2 | ESD target | HBM ≥ 2 kV, CDM ≥ 500 V as **targets, not results** (carried from `gf180-tmds-tx` DR-0011 at `9a55961`); the PDK publishes no rating | HBM ≥ 1 kV, CDM ≥ 250 V | — | **not provable by simulation**: structural review (a protected path on every pin), DRC with the ESD layers, extraction and LVS; qualification is silicon only | n/a | det. |
| P3 | Pad pitch | 75 µm slot (PDK `analog_*` pads are 75 × 200 µm in `lef/sky130_ef_io.lef`), tiling with stock ring cells | 80 µm (the GPIO slot) | — | LEF/GDS bounding box; DRC | n/a | det. |
| P4 | Behaviour when unpowered | pad current ≤ ±20 µA for 0 ≤ V_pad ≤ 2.4 V with VCCD = VDDIO = 0 V at 125 °C (a proposed figure sized to public LVDS power-off leakage; no back-power path through the ESD network, which the stock VDDIO diodes would create) | back-power through the ESD diodes allowed as a documented limitation (if the stock `analog_esd_pad` fallback of `DR-001` is used) | — | simulated DC at 0 V rails; extraction | G75 temps, process corners | det. |

## Power

| ID | Parameter | Target | Fallback | Stretch | Verification | PVT | Type |
|---|---|---|---|---|---|---|---|
| W1 | Power per lane at the stated rate, driver + CMFB + predriver + serializer share | ≤ 20 mW typical (`tt`, 27 °C, 1.80 V/3.30 V); ≤ 30 mW at any G75 condition | ≤ 18 mW typical at 400 Mb/s | ≤ 25 mW typical at 1.5 Gb/s | simulated supply current, then post-layout | G75 | det. |

Budget arithmetic, not a result: driver tail 3.5 mA × 3.3 V = 11.6 mW (exact
for the nominal design point); CMFB and bias allocation 0.5 mA × 3.3 V =
1.7 mW; core-domain allocation (serializer, DDR mux, predriver) 3 mW; sum
16.3 mW against the 20 mW target. At the window top (4.54 mA at 3.63 V = 16.5 mW,
plus 1.8 mW and 3.5 mW) the sum is 21.8 mW against the 30 mW cap. The static
tail dominates, so the 400 Mb/s fallback saves little.

## Clock interface (bit clock, no `consumes:` edge)

This block **specifies** the clock; it does not design it (`DR-007`). Compared
against `2AMLogic/sky130-pll` at `76a4b68556f83ea0710e9fa16abf44e28f89d3bc`
(rows cited from its `spec/target-spec.md`) and, as the alternative,
`2AMLogic/sky130-adpll` at `6067a8a740f8ba448324fbcc70a5b3e1ecaad599`
(`README.md`; its `spec/` is a bare README at that commit). The sibling PLL's
`main` has since moved (`4c20e8e…`); that head was not read.

| ID | Requirement | This block: target / fallback / stretch | `sky130-pll` @ `76a4b68` | `sky130-adpll` @ `6067a8a` | Fit |
|---|---|---|---|---|---|
| C1 | Bit-clock frequency (half the bit rate) | **500 MHz** / 200 MHz / 750 MHz | row 2: 10–200 MHz, **draft, not ratified, "not assumed to hold"** | draft target 200 MHz, stretch 400 MHz | **GAP.** Target needs 2.5× the top of the band; stretch 3.75×. The fallback (200 MHz) sits on the band's top edge, itself unratified. Neither sibling reaches 500 MHz. |
| C2 | Phases and format | one clock, both edges used; 0°/180° from one net, no multiphase; single-ended CMOS | one `CLK` output (rows 9, 14, 15) | not specified | Fit in format, subject to C1 |
| C3 | Duty cycle | 50 ± 2.5 % at 500 MHz (DCD ≈ 50 ps = 0.05 UI) | row 14: 45–55 %, draft | not specified | **GAP**, draft band is twice as loose: 5 % of 2 ns = 100 ps = 0.10 UI, double the allocation |
| C4 | Jitter (PLL-attributable) | ≤ 0.10 UI peak-to-peak on the 500 MHz clock, per edge = 100 ps at 1 Gb/s ≈ 7.1 ps RMS (dual-Dirac factor 14.07 at BER 10⁻¹²; informative) | row 9, **ratified**: period jitter ≤ 1.0 % RMS = 20 ps at 500 MHz ≈ 0.28 UI peak-to-peak by the same factor; first recorded measurement is a miss (1.58 %, 1.85 %, 3.07 % over 3 locked draws) | ≤ 1 % of period RMS (draft) | **GAP**, about 2.8× over even if the ratified figure were met; and the metric differs (it is *period* jitter, this budget is *absolute* TIE jitter), to be settled with the sibling |
| C5 | Supply and levels | 1.8 V domain, 1.62–1.98 V; rail-to-rail CMOS, V_OH ≥ 0.9·VDD, V_OL ≤ 0.1·VDD | row 1, **ratified**: 1.8 V ± 10 %, single domain; row 15 draft same levels | 1.8 V core cells | Fit |
| C6 | Lock indication | digital `lock`; the serializer is held in reset until it asserts | row 16: `lock` output, **draft** (contract proposed in its DR-007) | not specified | Fit in kind, draft |
| C7 | Reference / multiplication | 500 MHz = N × f_ref with integer N | rows 3–4: f_ref 1–25 MHz, N = 4…64 (draft), so 25 MHz × 20 works arithmetically | integer-N | Fit by arithmetic *if* the VCO reaches 500 MHz (C1) |
| C8 | Output load | **not yet specified**: five lane serializers plus five DDR multiplexers; set at clock-tree design | row 15 draft; its buffer scope in its own DR-008 (not read) | not specified | Open |

**Fit verdict: no sibling meets the 1 Gb/s clock requirement today.** C1, C3
and C4 are gaps. The requirement was filed as
[`2AMLogic/sky130-pll#333`](https://github.com/2AMLogic/sky130-pll/issues/333);
no PLL is designed here. Until a sibling meets C1–C8,
this block is verified with an ideal clock source and every evidence record
says so.

### Total jitter allocation (informative, at the pad, 1 Gb/s)

| Contributor | Allocation (UI, peak-to-peak) | At 1 Gb/s |
|---|---|---|
| Clock source (random, C4) | 0.10 | 100 ps |
| Clock duty-cycle distortion (C3) | 0.05 | 50 ps |
| Serializer, DDR mux and predriver deterministic jitter | 0.05 | 50 ps |
| Driver ISI and P/N skew | 0.05 | 50 ps |
| **Total** | **0.25** | **250 ps** |

The 0.25 UI total and the 0.10 UI clock share follow the split `gf180-tmds-tx`
uses for its own PLL requirement (its `spec/tmds-tx.md` DR-0004 at `9a55961`);
they are informative targets here, not taken from either interface standard.
The eye row E9 (width ≥ 0.75 UI) is the same 0.25 UI total seen from the other
side.

## Open items

- Capacitance and ESD adequacy of the custom pad cell are owed to extraction
  and silicon (P1, P2); the stock-cell fallback is named in `DR-001`.
- Receiver and package capacitance (1.0 pF per side) is an assumption in
  E5, E9 and `DR-006`.
- `sky130-pll` requirement filed as `2AMLogic/sky130-pll#333`; its answer
  (in scope or not) is awaited.
- Replace the vendor-literature numbers (E3, E4, E7) with the licensed
  standard's text at ratification. Check in the same reading whether the
  standard sets a **minimum transition time**: its 1.923 Gb/s theoretical
  maximum equals 1/(2 × 260 ps), which suggests a 260 ps floor (not verified
  from the standard's text). If it does, E5's 100 ps lower bound sits below
  it, and the 1.5 Gb/s stretch's 0.4 UI = 267 ps upper bound all but meets
  it, so the stretch would have no transition-time window inside the standard.
- 125 °C standard-cell timing is not published by the Liberty set.
