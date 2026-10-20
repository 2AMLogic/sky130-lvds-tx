# DR-007: Bit-clock sourcing: specify the interface, record the gap, file the requirement

- **Status**: proposed
- **Date**: 2026-10-17
- **Author**: builder agent (issue #2)
- **Ratifies against / input to**: issue #2; `spec/target-spec.md` rows C1–C8
- **Supersedes**: none

## Context

This repo has no `consumes:` edge and does not design a PLL (`CLAUDE.md`).
It must specify the bit-clock interface and compare it against `sky130-pll`
by name at a commit; if the band does not reach the requirement, the gap goes
in the spec and the requirement is filed on the sibling (`2am/REUSE.md`, read
at `2AMLogic/2am` `155fa0c156b14ffac6a8d39a4496a910de41aa67`; its audit already
records the same pattern: `gf180-tmds-tx` needed 270 MHz, `gf180-pll` was
ratified for 10–200 MHz, and neither repo mentioned the other).

Siblings read:

- `2AMLogic/sky130-pll` at `76a4b68556f83ea0710e9fa16abf44e28f89d3bc`
  (`spec/target-spec.md`, rows 1–4, 9, 14–16, 19–20). Its `main` has since
  moved to `4c20e8e2e787d2f5d7dc36f3c5928bb4dcb6d4ce`; **this record compares
  against the commit the issue names, not the newer head, which was not read.**
- `2AMLogic/sky130-adpll` at `6067a8a740f8ba448324fbcc70a5b3e1ecaad599`
  (`README.md` only; its `spec/` holds only a README at that commit).

The comparison table is `target-spec.md` rows C1–C8. In summary: the PLL's
draft output band (row 2, **not ratified**) is 10–200 MHz; the 1 Gb/s target
needs 500 MHz (2.5× above the band's top), and the 1.5 Gb/s stretch 750 MHz
(3.75×). Its **ratified** period jitter (row 9) is ≤ 1.0 % RMS = 20 ps at
500 MHz; this block's budget allots the clock ≤ 0.10 UI peak-to-peak (≈ 7 ps
RMS under the dual-Dirac factor 14.07 for BER 10⁻¹²), so the ratified figure
is ≈ 2.8× over; and that spec's own first measurement records a miss against
1.0 % (1.58 %, 1.85 %, 3.07 % over 3 locked draws). The sky130-adpll draft
output is 200 MHz target / 400 MHz stretch, also short of 500 MHz.

## Decision

1. **The 500 MHz DDR clock is specified here as an interface requirement**
   (spec C1–C8), not designed here.
2. **The gap is recorded in the spec**, at the cited commits: no sibling PLL
   fits the 1 Gb/s target today; the 400 Mb/s fallback (200 MHz) sits on the
   top edge of the PLL's *draft* band.
3. **The requirement is filed on `2AMLogic/sky130-pll`** (the analog PLL named
   in `CLAUDE.md`) with the table, and the issue notes `sky130-adpll` as the
   alternative whose stretch (400 MHz) also falls short. Filing the
   requirement is the action this issue's acceptance criteria call for; the
   issue is `2AMLogic/sky130-pll#333`.
4. **No edge is added to `repos.yml` and no `reuse.lock.json` import is
   written**: adding a `consumes` edge is operator-governed (REUSE.md).

Proposed; ratifies with the PR.

## Alternatives considered

- **Design a clock multiplier or doubler here** to turn the PLL's ≤ 200 MHz
  into 500 MHz: that is PLL design by another name and is out of scope.
- **Quietly lower the target to fit the PLL**: the spec is not relaxed to
  match an unavailable clock; the fallback column already states what fits.
- **Use `sky130-adpll`**: its draft target is 200 MHz (stretch 400 MHz) and its
  spec directory was empty at the read commit; it does not fit either.
  Recorded as a candidate to watch, not chosen.
- **Re-read the newer `sky130-pll` head**: would change the comparison commit;
  the issue names `76a4b68…` and the comparison is repeated when this spec is
  ratified or the sibling's band is ratified.

## Consequences

- The system is blocked at the clock source until a sibling meets C1–C8:
  everything up to the serializer and the driver can still be built and
  verified with an ideal clock source, and the evidence records must say so.
- Jitter metric mismatch to resolve with the sibling: it spec'd *period*
  jitter; this block's budget is *absolute (TIE)* jitter at the output.

## Status notes

Proposed. Re-compare on any change to `sky130-pll` rows 2, 9 or 14.
