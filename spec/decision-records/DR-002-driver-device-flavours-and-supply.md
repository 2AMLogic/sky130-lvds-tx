# DR-002: Driver device flavours, supply per rail, and common-mode regulation

- **Status**: proposed
- **Date**: 2026-10-17
- **Author**: builder agent (issue #2)
- **Ratifies against / input to**: issue #2; `spec/target-spec.md` rows E1–E8, D1–D4, PVT
- **Supersedes**: none

## Context

`CLAUDE.md` names the common mode as the second risk: an LVDS output sits near
1.2 V, which constrains which device flavours the driver can use and how
common-mode feedback (CMFB) holds across PVT. The driver is a current-steering
H-bridge: a top current source from a supply, two switch pairs steering the
current through the 100 Ω load, and a bottom current sink, with CMFB setting
the output common mode. Electrical windows are the numbers in
`target-spec.md` (V_OS 1.125–1.375 V, V_OD 247–454 mV, nominal 3.5 mA × 100 Ω
= 350 mV), following the TIA/EIA-644 windows.

sky130 flavours installed and modelled (`libs.ref/sky130_fd_pr/spice/`):
1.8 V core `nfet_01v8`/`pfet_01v8` (plus lvt/hvt variants), and the 5 V-class
`nfet_g5v0d10v5`/`pfet_g5v0d10v5` (with `esd_nfet_g5v0d10v5`), all with
`tt/ff/ss/fs/sf` corner files. The I/O library characterises VDDIO of 3.0 V
and 3.3 V up to 5.5 V against a 1.6–1.95 V core (`lib/sky130_ef_io__gpiov2_pad_*`).
The 3.3 V standard-cell library `sky130_fd_sc_hvl` is installed.

**Headroom arithmetic (first order, no simulation).** Let the pad high level
be V_OS + V_OD/2. At the regulation target 1.25 V (the window centre, §3)
+ 175 mV it is 1.425 V; at the window extreme 1.375 V + 227 mV it is 1.60 V.
The PMOS source plus switch must fit between the top rail and that level.

| Top rail | Rail min | Headroom to nominal pad-high 1.425 V | to window-extreme 1.60 V |
|---|---|---|---|
| 1.8 V core, ±10 % | 1.62 V | 0.195 V for source V_dsat **and** switch drop at 3.5 mA | 0.02 V |
| 3.3 V VDDIO, ±10 % | 2.97 V | 1.545 V | 1.37 V |

0.195 V cannot hold a saturated 3.5 mA PMOS source plus a switch at the slow
corner without a very large device, and the window-extreme case has no
headroom at all, so a 1.8 V-only H-bridge cannot cover the V_OS window. The
bottom side is not the constraint: the lowest pad level
(1.125 V − 227 mV ≈ 0.90 V) leaves ≈ 0.8 V for the sink after a switch drop.
The tightest item the 3.3 V choice leaves is the **NMOS switch Vgs ≈ 0.8 V**
(source ≈ 1.0 V, gate 1.8 V) at the slow corner, which sizes those switches
wide; it is a design consequence, not a feasibility problem.

**Why not 3.3 V switches.** Gates of 3.3 V switches would need level shifting
out of the 1.8 V domain. The stock cell is far too slow and skewed for this:
`sky130_fd_sc_hvl__lsbuflv2hv_1`, `A→X`, at `ss_100C_3v00_lowhv1v65_lv1v60`
(`lib/sky130_fd_sc_hvl__ss_100C_3v00_lowhv1v65_lv1v60.lib`, first table
entry): cell_rise 2.31 ns, cell_fall 0.68 ns. A 1.6 ns rise/fall asymmetry is
more than a whole 1 ns bit time, so it is unusable in the data path.

## Decision

1. **Rails.** Core/digital logic and the **switch devices run on VCCD =
   1.8 V ± 10 % (1.62–1.98 V)**, consistent with `sky130-pll` row 1 (ratified
   there, same range). The **current source and sink (and the CMFB amplifier's
   output stage) run on VDDIO = 3.3 V ± 10 % (2.97–3.63 V)**. The rail names
   are the PDK ring's (`VCCD`, `VDDIO`, `VSSIO`; analog `VDDA`/`VSSA` are
   present on the pad cell but this design takes the driver supply from VDDIO).
2. **Flavours.** Current source/sink: `pfet_g5v0d10v5` / `nfet_g5v0d10v5`.
   Switch pairs and predriver: 1.8 V `pfet_01v8` / `nfet_01v8`, driven directly
   from the 1.8 V domain, **no level shifter in the data path**. Every
   thin-oxide terminal pair must stay ≤ 1.98 V: switch source nodes sit at
   ≈ 1.5–1.7 V (top) and ≈ 0.8 V (bottom) by the arithmetic above, so this
   holds in normal operation; it does **not** hold if a pad is shorted to
   VDDIO (see spec row E8, where that case is explicitly not targeted).
3. **Common-mode regulation.** CMFB senses the pad common mode and trims the
   bottom sink against the fixed top source; the V_OS target is
   **1.25 V ± 75 mV across PVT** (1.175–1.325 V), the centre of the
   1.125–1.375 V window, leaving 50 mV to each edge for mismatch and ripple.
   (1.2 V, the figure vendor literature quotes as typical, is not the
   target: 1.2 V ± 75 mV would touch the window's lower edge with no margin.) Verification includes CMFB loop gain and phase margin
   (≥ 45°, the criterion `sky130-pll` row 7 uses), and V_OS must hold with the
   pad common-mode loaded by the receiver tolerance.
4. **PVT.** Process `tt, ff, ss, sf, fs` (the five standard corners the
   sibling `sky130-pll` DR-003 ratified); temperature −40, 27, 125 °C (same
   sampling); supply pairs (VCCD, VDDIO) ∈ {(1.62, 2.97), (1.80, 3.30),
   (1.98, 3.63), (1.62, 3.63), (1.98, 2.97)}: 5 × 5 × 3 = 75 conditions per
   recorded analog result. Note: the installed `sky130_fd_sc_hd` Liberty
   corners stop at 100 °C; 125 °C data for standard cells must come from
   SPICE or a derate, and is **not published** by the library.

This record is **proposed** and ratifies only with the PR that carries it.

## Alternatives considered

- **1.8 V-only driver (no VDDIO)**: fails the headroom arithmetic above.
  Rejected. Would be revisited only if the V_OS window were lowered, which
  would be a spec change.
- **3.3 V switches with level shifters**: rejected on the measured stock
  level-shifter delays above; a custom shifter would add a block and its
  jitter. Kept as the contingency if thin-oxide stress (short to VDDIO) later
  proves a requirement.
- **Voltage-mode (source-terminated) driver**: its common mode follows the
  supply (≈ 0.9 V from 1.8 V), not ≈ 1.2 V; does not meet the V_OS window.
- **`nfet_05v0_nvt` / native devices on the tail**: lower Vth helps headroom
  but is not needed given the 3.3 V rail; unnecessary variety. Rejected for now.
- **Open-loop common mode (no CMFB)**: V_OS would track process directly;
  the window is only ±125 mV. Rejected.

## Consequences

- Two supply domains plus ground-referenced ESD: the floorplan needs VCCD and
  VDDIO to the driver; this adds a supply row to the PVT grid (75 conditions)
  and to every analog evidence record.
- Thin-oxide switches see the pad: over-voltage on the pad (short to VDDIO,
  hot-plug above 1.98 V) can stress them; the spec states it as a limitation
  (E8) rather than claiming tolerance.
- Power-off and disabled states are design requirements, not afterthoughts.
  (i) With VCCD = VDDIO = 0 V the pad-facing PMOS drains (top switches, and
  through them the current source) are p+ junctions in n-wells sitting at
  0 V; they conduct from V_pad ≈ 0.6 V exactly as the stock pad's VDDIO
  diode would, so spec row P4 is met only with fail-safe well biasing of
  those devices (or an isolating element), which this record leaves to the
  driver design and `DR-001` names as a joint requirement. (ii) In any
  powered state in which both switches of a steering pair are off (reset,
  disable, a break-before-make gap), the VDDIO current source pulls the
  shared thin-oxide switch source node toward VDDIO (up to 3.63 V); the
  predriver must guarantee that one switch of each pair is always on, or the
  node must be clamped, and every simulation's per-device stress check (D4)
  covers those states (spec E8).
- Static power is dominated by the tail current from 3.3 V (see power row).
- Total pad capacitance includes the switch drains (P1 allocates 0.5 pF).

## Status notes

Proposed. Numbers above are arithmetic from the windows and from Liberty
tables; none is a simulation result. The T1 driver campaign (issue #6) owns
the evidence.
