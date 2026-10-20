# DR-001: PDK pad cell vs. custom pad cell

- **Status**: proposed
- **Date**: 2026-10-17
- **Author**: builder agent (issue #2)
- **Ratifies against / input to**: issue #2; `spec/target-spec.md` rows P1–P4 (pads, ESD, unpowered behaviour), E8
- **Supersedes**: none

## Context

The driver must reach a pad with ESD protection and a capacitance budget a
~1 Gb/s low-swing signal survives (`CLAUDE.md`). Before deciding to draw a
cell, this record establishes what the sky130 I/O library provides for a
direct analog path to a pad.

**What was read.** Only files installed in the volare tree, PDK revision
`open_pdks c6d73a35f524070e85faff4a6a9eef49553ebc2b` (`~/.volare/sky130A/SOURCES`;
environment pinning is issue #3, so this is the revision read, not a pin).
Paths below are relative to `libs.ref/sky130_fd_io/`. The upstream
`google/skywater-pdk` I/O library README could not be fetched in this session
(the forge read gateway was shedding), so no claim here rests on it.

**What the library provides.**

| Cell (`sky130_ef_io__…`) | Source (LEF / GDS / mag) | Signal path to pad | ESD structure as drawn |
|---|---|---|---|
| `gpiov2_pad` (+`_wrapped`) | `lef/sky130_ef_io.lef` 80 × 197.965 µm (wrapped: 210.965 µm deep) | through the cell's own output driver / input buffer; analog only via the `ANALOG_EN`/`ANALOG_SEL` switches onto `AMUXBUS_A/B` | on-cell GPIO ESD; Liberty `PAD` pin capacitance 1.05–1.16 pF (see below) |
| `analog_esd_pad` | LEF 75 × 200 µm; `mag/…analog_esd_pad.mag` | `P_PAD` (met1–met5 stack) tied to `P_CORE` (met3, 24.72–49.72 µm wide stub at the core edge): a direct metal path, no active device | `esd_pad_and_busses`: one `esd_ndiode_11v0_array` instance named `esd_vddio` and one `esd_pdiode_11v0_array` named `esd_vssio` (`mag/sky130_ef_io__esd_pad_and_busses.mag`): diodes **to VDDIO and to VSSIO** |
| `analog_noesd_pad`, `analog_pad` | LEF 75 × 200 µm | same direct path | **none**: both instantiate `simple_pad_and_busses` only; their `.mag` bodies are identical modulo the cell name (checked with `diff`) |
| `analog_minesd_pad`, `…_short` | `gds/sky130_ef_io__analog.gds` and `mag/` only; **absent from `lef/` and `maglef/`** | same direct path | `minesd_pad_and_busses`: one `esd_ndiode_11v0_single` and one `esd_pdiode_11v0_single` instead of the arrays |
| `bare_pad` | LEF 65.4 × 75.4 µm, `CLASS BLOCK` | pad metal only | none |
| `vddio_hvc_clamped_pad`, `vssio_hvc_clamped_pad`, `vccd_lvc_clamped*_pad`, … | LEF 75 × 197.965 µm | supply cells | rail clamps (`hvclampv2`, `lvclamp`) in the ring |

**Published capacitance and ESD data.** The PDK publishes pad capacitance in
Liberty for two things:

- The GPIO: `PAD` pin capacitance 1.117 pF (tt, 25 °C, 1.8/3.3 V), 1.163 pF
  (ss, 100 °C, 3.0 V), 1.048 pF (ff, −40 °C, 5.5 V), unit `pf`
  (`lib/sky130_ef_io__gpiov2_pad_*.lib`).
- The foundry analog-pad primitive `sky130_fd_io__top_analog_pad`
  (`lib/sky130_fd_io__top_analog_pad_<corner>.lib`, 34 files). In the 20 files
  that carry a pin capacitance, `pad` and `pad_core` are both **1.061130 pF**,
  identical at every one of those corners (tt 25 °C and 100 °C, ss and ff
  files among them). The other 14 files (the multi-supply `ff_ss_*`/`ss_ff_*`
  corners and two `ss_*_5v50_1v65` ones) declare the pins with no capacitance
  attribute, so they publish nothing. The cell is 75 × 198 µm (`area 14850`),
  the same footprint as the `ef_io__analog_*` slot. Its `.mag` instantiates
  `top_analog_pad_pddrvr_strong`/`pudrvr_strong` drivers, which differ from the
  `esd_*diode_11v0_*` structure the `ef_io__analog_*` wrappers draw.

**What is and is not established about the relation.** Same footprint and pad
pin names suggest `top_analog_pad` is the core pad primitive, but this record
did **not** establish that its Liberty figure describes the ESD-bearing
`ef_io__analog_*` wrapper cells, and the drawn internals differ. So 1.061 pF is
a **reference**, comparable in order to the GPIO figure, not a verified
capacitance of any cell this repo would place. The `sky130_ef_io__analog_*`
wrappers have **no `.lib`, CDL or SPICE subcircuit** (`cdl/sky130_ef_io.cdl` has
none), so for those cells capacitance is **not published**. It cannot be
estimated reliably from the layout either: the diode marker layers in
`esd_*diode_11v0_array.mag` are 0.07 µm slivers, not junction area. **No HBM or
CDM rating is published in any installed file.** The diode models exist
(`sky130_fd_pr__diode_pd2nw_11v0`, CJ 0.775 fF/µm²;
`sky130_fd_pr__diode_pw2nd_11v0`, CJ 0.851 fF/µm²), but their junction areas
are not given anywhere installed. The capacitance of every candidate is
therefore owed to extraction of the drawn cell (T1 evidence, issue #6), not
asserted here.

**The fleet precedent.** `2AMLogic/gf180-tmds-tx` at
`9a55961ab5e4608d42ffefb70308adcb4b42213e`:
`spec/pad-ring-esd-survey.md` found that the gf180mcu I/O library had no
differential/CML pad and drew a custom pad; `spec/decisions/0011-pad-esd-strategy.md`
kept a diode-based clamp, a ≤ 2 pF per-pad capacitance budget, HBM ≥ 2 kV and
CDM ≥ 500 V as targets (not results), required a drawn substrate tap, and
required ring continuity. Its own measured custom-pad capacitance (7.95 pF at a
25 × 25 µm pad) exceeded that 2 pF budget about 4×, which is the cautionary
number for any custom cell here. sky130 differs: it ships analog pads, which
gf180mcu does not, so the question is open here in a way it was not there.

**The deciding observation.** The stock ESD cell clamps with diodes to
**VDDIO** as well as VSSIO. With the transmitter's rails at 0 V and another
chip driving the pad to ~1.2 V, the VDDIO diode conducts from about
V_pad > 0.6 V: a back-power path. Whether that matters is a spec row
(`target-spec.md` P4); it is the one electrical requirement the stock ESD
structure cannot meet by construction. Removing that diode is **necessary
for P4 but not sufficient**: the driver's pad-facing PMOS drains (`DR-002`:
the top switches and, through them, the current source) are p+ junctions in
n-wells tied to a rail that is also at 0 V, and they conduct from the same
≈ 0.6 V. P4 therefore binds `DR-002` as well (fail-safe well biasing of the
pad-facing PMOS devices, or an isolating element), and the spec records it as
a joint requirement on pad and driver, not on the pad cell alone.

## Decision

**Draw a custom pad cell**, built on the PDK's own frame rather than from a
blank: take `sky130_ef_io__analog_noesd_pad` (75 × 200 µm slot, supply/AMUX
bus continuity, met1–met5 pad stack, `P_CORE` on met3) and add a custom ESD
network on the core side of `P_CORE`, **to VSSIO only**: a pad-to-VSSIO diode
(`sky130_fd_pr__diode_pw2nd_11v0` class) for negative strikes, and a
grounded-gate snapback NMOS from `sky130_fd_pr__esd_nfet_g5v0d10v5` for
positive strikes. The snapback device is not optional: with no pad-to-VDDIO
element there is no path from the pad to the ring's VDDIO/VSSIO rail clamp,
so the local clamp to VSSIO is the only positive-polarity path. Its trigger
voltage must sit below the breakdown of the thin-oxide switch drains that
`DR-002` places at the pad; that is a device-class and sizing question for
the drawn cell (an `esd_nfet_01v8` clamp is the alternative if the 5 V-class
device triggers too high). Pad pitch stays at the PDK's 75 µm slot so the
cell tiles with stock ring cells.

**Fallback (named, not hidden):** if the custom ESD network cannot be signed
off through `klt` (DRC, extraction, LVS) or its extracted capacitance exceeds
the P1 budget, use the stock `sky130_ef_io__analog_esd_pad` unmodified and
move spec row P4 (unpowered behaviour) to its fallback column. That
substitution is a spec change and needs its own decision record; agents do not
make it silently.

This record is **proposed**. It becomes ratified only on human merge approval
of the PR that carries it (see `spec/README.md`).

## Alternatives considered

- **Stock `analog_esd_pad` as the baseline.** Foundry-supplied ring-compatible
  diodes and no new ESD to sign off. Rejected as baseline because (a) its
  VDDIO diodes defeat unpowered behaviour, (b) its capacitance is not published for the wrapper itself (only the
  `top_analog_pad` primitive's ~1.06 pF is, and its match is unverified), so it
  would be adopted on faith, and (c) it leaves nothing for this repo to
  learn about the core-to-pad seam, which `CLAUDE.md` names as the risk. Kept
  as the fallback and as the A/B reference for the first extraction.
- **`analog_minesd_pad`.** Smaller diodes, lower capacitance, same VDDIO diode.
  Not usable as shipped: no LEF or maglef view, so the ring flow cannot place
  it; same back-power path.
- **`gpiov2_pad` in analog mode.** Its 1.05–1.16 pF is published, but the
  signal passes through the `AMUX` switches or the cell's own driver, neither
  characterised for 1 Gb/s; rejected.
- **A fully blank custom pad (from `bare_pad`).** Maximum freedom, but
  re-draws the supply-bus continuity the stock frame already provides;
  gf180-tmds-tx needed that ring-continuity rework later (its DR-0011
  "ring continuity: required"). Not chosen.
- **Defer until capacitance is extracted.** Rejected: layout, driver and
  seam planning all depend on the pitch and ESD topology now.

## Consequences

- The decision does **not** depend on capacitance being unpublished. The
  deciding argument is the VDDIO back-power diode (P4). The published
  ~1.06 pF `top_analog_pad` figure leaves the P1 allocation (pad + ESD
  ≤ 1.2 pF) workable but with only ~0.14 pF of margin, which is a reason to
  extract early, not a reason to change the decision.
- Spec rows P1 (capacitance budget), P2 (ESD target), P3 (pitch) and P4
  (unpowered) are written against this decision.
- P4 is not met by this cell alone (see the deciding observation). If
  `DR-002`'s driver does not adopt fail-safe well biasing, P4 moves to its
  fallback column whatever pad is drawn, and this decision then rests on the
  seam-learning and capacitance-margin arguments only; that would be the
  moment to re-weigh the stock `analog_esd_pad` as the baseline.
- A new custom cell to draw, DRC/LVS in `klt`, and extract; the ESD clamp
  sizing and its HBM/CDM adequacy are **not provable by simulation** and stay
  an unverified target until silicon (`measurements/`).
- The ring around the lanes must supply clamped VDDIO/VSSIO cells; the
  floorplan has to reserve them.
- Risk accepted: gf180-tmds-tx's custom pad exceeded its capacitance budget
  4×; the budget gate in P1 exists so the same outcome here triggers the
  stated fallback, not a relaxed budget.
- Friction to file against klayout-tools when the cell is drawn (not
  encountered yet; none filed by this issue, which ran no `klt` command).

## Status notes

Proposed. Ratifies with the PR carrying `spec/` (human merge approval).
Capacitance and ESD claims for the drawn cell stay "owed" until extracted;
the `top_analog_pad` ~1.06 pF is a reference only.
