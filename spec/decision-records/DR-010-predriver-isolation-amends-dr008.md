# DR-010: Predriver output-stage isolation and floating wells (proposed amendment of DR-008)

- **Status**: proposed. Agents do not ratify; `DR-008` and the `spec/target-spec.md` rows are **unchanged**.
- **Date**: 2026-11-20
- **Author**: builder agent (issue #167)
- **Ratifies against / input to**: `spec/target-spec.md` rows P4, P4a, P4b, D4; amends `DR-008` §2 and §4; uses the device flavours of `DR-002`
- **Supersedes**: none
- **Number**: `main` ends at `DR-008`; PR #79 proposes `DR-009`, so this takes `DR-010`. Renumber at merge if #79 lands differently.

## Context

`sim/unpowered-pad/RECORD.md` (findings F2, F3, F5) found that `DR-008`'s
gate tracking is defeated as netlisted: the predriver's P-side output PMOS
(`XMP_3pma`, `XMP_3pmb`, `XMP_3pea`, `XMP_3peb`, `pfet_01v8`) has its n-well on
VCCD = 0 V, so its drain/n-well junction clamps each top-switch gate 0.41-0.97 V
above ground while the floating well is near 1.9 V. The top switch stays on, the
pad drives node `TOP`, and the current source `XMPS` conducts into the grounded
VDDIO rail (about 10 mA per pad at -40 C). `DR-008` §4 ("the current source needs
no measure of its own") rests on both switches being off, which F3 broke.

## Decision

1. **Isolate each P-side output stage from its switch-gate net with a thick-oxide
   transmission gate** (`pfet_g5v0d10v5` + `nfet_g5v0d10v5`, L = 0.5 um). The
   thin-oxide PMOS/NMOS pair still drives an inner node (`IN_3pma`, `IN_3pmb`,
   `IN_3pea`, `IN_3peb`); the transmission gate connects it to `GPA`/`GPB`/`XPA`/`XPB`.
   Both gates are controlled by VCCD: powered, the gate is on (n-gate at VCCD,
   p-gate pulled to VSSIO); unpowered, the gate is off, so the lifted
   switch-gate net is no longer applied to the thin-oxide stage.
2. **Floating n-well for the transmission-gate PMOS**, one well per group
   (`PWM` for `GPA`/`GPB`, `PWE` for `XPA`/`XPB`), tied to max(VCCD, V_gate-net) by
   the same pair of well-switch `pfet_g5v0d10v5` devices `DR-008` §1 uses
   (VCCD to well gated by the net; net to well gated by VCCD).
3. **Transmission-gate p-gate control** (`GIM`, `GIE`): a `pfet_g5v0d10v5` from
   VCCD-gated well to the control node (pulls it to the well when VCCD is absent,
   keeping the PMOS off) and a minimum `nfet_g5v0d10v5` to VSSIO (pulls it low when
   VCCD is present).
4. **Sizing**: transmission-gate PMOS W = 20 um, NMOS W = 10 um. A powered
   predriver transient (tt, 27 C, 120 fF per P-side net) shows rise/fall to 0.9 V
   of about 0.38 ns / 0.40 ns against 0.29 / 0.26 ns without the gate, and a
   full-swing high of 1.79 V. This is a powered-mode speed cost that is **not
   closed against the 1 Gb/s eye**; it is owed to the driver-sizing work (#166).
5. **Current source (F2)**: with the P-side switches off, the worst Sweep A pad
   current is 0.1-41 uA across all 10 units (one, `fs`/125 C, at 41 uA misses
   20 uA), against about 10 mA before. Six of those ten units did not converge and
   are graded inconclusive, so only the four 125 C units are trusted values. F3 alone
   restored `DR-008` §4's premise to within that residue, so **no separate well
   measure for the current source is added**; the 125 C residue is recorded as a
   miss, not a ruling.
6. **N-side gates (F5)**: **no tracking is added in this record.** The
   gate-referenced thin-oxide pair on `XMSNA`/`XMSNB` stays at 2.400 V (pad 2.4 V,
   gate at 0 V) against the 1.98 V ceiling. A tracked N-side gate must also keep
   the bottom switch off and the `BOT` node from floating up, which interacts with
   the pull-down `XMNS`; that design is not settled here and is filed as a
   follow-up. P4b's thin-oxide criterion therefore still **fails**.

## Alternatives considered

- **Floating well for the predriver output PMOS itself** (the first option in
  issue #167), well-switches only. Probed at tt / -40 C, Sweep A endpoint: the pad
  current fell from 7.5 mA to 4.8 mA but the drain/well clamp moved with the well
  (`ja_pre_gpa` 0.91 V), so the gate still sat 1.1 V from its well. Rejected.
- **A single thick PMOS in series with the output PMOS source** (floating well, gate
  on VCCD). Probed at tt / -40 C, pad 2.4 V: pad current 0.35 nA, so it also
  isolates. It was not carried forward or run over the corner grid; it keeps the
  thin-oxide stage inside the powered pull-up path. The transmission gate was
  chosen because it isolates both output-stage devices. This is a design choice
  between two probed options, not a measured ranking.
- **Wider gate-tracking device** (`XMGTA`/`XMGTB` at W = 0.5, 2, 8 um, tt, -40 C):
  worst gate-to-well error 0.383 / 0.406 / 0.392 V. Width does not move it; the
  residual is the PMOS threshold deadband around V_pad of 0.4-0.6 V. Rejected as
  a fix, recorded as the traced mechanism.

## Consequences

- `DR-002`'s device list gains the transmission gates and control devices above;
  D4's wording about the well-switch and gate-tracking devices is not edited here.
- Row status after this change is in `sim/unpowered-pad/RECORD.md`
  (addendum 2026-11-20): P4 passes at 3 of the 4 converged Sweep A units and fails Sweep B at all
  10 units (common-mode sense resistors, F4 -- no
  longer subsumed); P4a/P4b gate-to-well and thin-oxide still fail. Nothing is
  relaxed.
- Layout: the predriver gains seven new device groups and two floating wells; the
  layout generator and the item 2 / 3 / 4 / 11 analog evidence are **not** updated
  here and must not be cited as covering this netlist (follow-up filed).
