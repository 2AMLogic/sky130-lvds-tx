# DR-004: Serializer reuse from `gf180-tmds-tx`

- **Status**: proposed
- **Date**: 2026-10-17
- **Author**: builder agent (issue #2)
- **Ratifies against / input to**: issue #2 (open question 3); `spec/target-spec.md` rows S1–S4
- **Supersedes**: none

## Context

`CLAUDE.md` and `2am/REUSE.md` (read at `2AMLogic/2am` commit
`155fa0c156b14ffac6a8d39a4496a910de41aa67`) say PDK-independent RTL has one
master, and that a serializer which already fits is taken by pinned
reference. The candidate is `2AMLogic/gf180-tmds-tx` at
`9a55961ab5e4608d42ffefb70308adcb4b42213e`: `rtl/tmds_serializer.v` (197
lines) with its rate record `spec/decisions/0014-serializer-rate-ceiling-and-microarchitecture.md`.

**What was read.** The module header and the DR in full; the module body past
the header was not studied line by line. From that reading:

| Property | `tmds_serializer.v` @ `9a55961` | This block needs |
|---|---|---|
| Reduction | 10 bits → 2 bits per `clk_half` cycle (10:1→2:1) | 8 bits → 2 bits per 500 MHz cycle (8:1→2:1) |
| Word boundary | derived from `clk_pix` by a two-flop edge detector (TMDS pixel framing) | from a ÷4 counter on the same clock; no pixel clock exists here |
| Clocks | consumes a bit-rate clock, divides by two internally to make `clk_half` | consumes a 500 MHz DDR clock directly (DR-003) |
| Input | the encoder's registered 10-bit TMDS character | 8 free-running payload bits |
| Rate assessment | feasibility derived from a gf180mcu 3.3 V library at `ss_125C_3v00` | sky130 `sky130_fd_sc_hd` 1.8 V |
| Micro-architecture | loadable shift register, one `mux2` level per bit (its DR-0014 §1) | same idea applies |

## Decision

**Do not import `tmds_serializer.v`.** Its ratio (10), its boundary logic
(pixel-clock edge detector) and its clocking (internal ÷2) differ from this
block's at the interface, so it is not a drop-in. **Adopt its micro-architecture
by name** (loadable shift register, one 2:1 mux level, as its DR-0014 §1 argues)
in new RTL here, with the ratio as a parameter so the 7:1 stretch and the
400 Mb/s fallback need no second file.

This is the recorded decision REUSE.md requires for a serializer that is not
taken: a second implementation exists because the boundary logic differs, not
by accident. **Revisit** when either repo factors out the generic
parameterised shift/load core: this repo is a second consumer of that idea,
which is REUSE.md's trigger for extraction. No `reuse.lock.json` is written
by this issue because nothing is imported; the RTL issue should add an
`in_tree` ledger entry with this record as its decision.

Proposed; ratifies with the PR.

## Alternatives considered

- **Vendor `tmds_serializer.v` with a parameter patch**: would need the ratio
  generalised and the pixel-boundary logic removed: a divergence on most of the
  file, which REUSE.md allows only with a decision record and makes the "pin"
  meaningless. Rejected.
- **Fetch it unmodified as a library and wrap it**: the 10-bit width cannot
  carry an 8-bit word without padding wasted cycles. Rejected.
- **Propose a generic core in `gf180-tmds-tx`**: reasonable and the stated
  revisit path, but it is another repo's decision and a change to a design
  whose evidence binds to its current netlist. Not filed by this issue.

## Consequences

- New serializer RTL and cocotb tests are owed in this repo (issue #4 harness,
  later RTL issue); the verification plan is in spec row S4.
- The micro-architecture claim "one mux level" is checked against sky130
  Liberty in spec row S3, not inherited from the gf180 numbers (different
  library, voltage, corner).

## Status notes

Proposed. The unread remainder of the sibling RTL is the limit of this
comparison; the decision rests on the interface differences above, which the
header and DR establish.
