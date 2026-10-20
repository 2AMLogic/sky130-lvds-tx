# DR-006: Rate and lane-count targets, with the slow-corner edge budget

- **Status**: proposed
- **Date**: 2026-10-17
- **Author**: builder agent (issue #2)
- **Ratifies against / input to**: issue #2 (open question 1); `spec/target-spec.md` rows R1–R3, E5, S3
- **Supersedes**: none

## Context

Open question: does a 1 Gb/s target leave enough rise/fall margin on sky130 at
the slow corner, or should the target drop toward the 400 Mb/s fallback? The
issue asks for a stated first-order budget; no simulation is required or
claimed here. Every number is arithmetic from stated inputs; the recorded
evidence is later work (issue #6).

## The budget

**Edge-time allowance.** At 1 Gb/s, UI = 1000 ps. The spec bounds the pad
rise/fall time (20–80 %) at ≤ 0.4 UI = 400 ps at every PVT corner (spec E5).

**Load RC (output pole).** Each pad sees ≈ 50 Ω to the differential midpoint.
Assume pad + ESD + driver drains at the P1 budget plus 1.0 pF for receiver and
package (an assumption; neither is in the repo):

| Case | C_pad | C_total | τ = 50 Ω·C | t₂₀₋₈₀ = 1.386·τ | Driver edge allowed (root-sum-square with 0.4 UI) |
|---|---|---|---|---|---|
| Target, 1 Gb/s | 2.0 pF | 3.0 pF | 150 ps | 208 ps | √(400² − 208²) ≈ 342 ps |
| Fallback pad budget, 1 Gb/s | 3.0 pF | 4.0 pF | 200 ps | 277 ps | ≈ 289 ps |
| Stretch, 1.5 Gb/s (UI 667 ps, 0.4 UI = 267 ps) | 1.5 pF | 2.5 pF | 125 ps | 173 ps | ≈ 203 ps |

The single-pole residual after one UI at the target is exp(−1000/150) ≈ 0.13 %,
so output-pole ISI is negligible at 1 Gb/s. The load RC alone uses about half
the edge budget, which is why the capacitance gate in P1 exists.

**Serializer register-to-register budget** (the reduction stage runs on the
500 MHz clock, 2.000 ns period). Read directly from
`libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__ss_100C_1v60.lib`, first table
point (input slew 0.01 ns, load ≈ 1.5 fF):

| Item | Cell / arc | Value |
|---|---|---|
| Clock-to-Q | `dfxtp_1`, `CLK→Q`, cell_rise (worse of rise/fall) | 0.580 ns |
| Setup | `dfxtp_1`, `D` vs `CLK`, fall_constraint | 0.260 ns |
| One mux level | `mux2_1`, `A0→X`, cell_fall (worse of rise/fall) | 0.611 ns |
| **Sum** | floor 0.840 ns + mux 0.611 ns | **1.451 ns** |

| Clock | Period | Slack vs 1.451 ns |
|---|---|---|
| 200 MHz (400 Mb/s fallback) | 5.000 ns | 3.549 ns (71 %) |
| **500 MHz (1 Gb/s target)** | 2.000 ns | **0.549 ns (27 %)** before clock skew, wire, uncertainty |
| 750 MHz (1.5 Gb/s stretch) | 1.333 ns | **−0.118 ns (−8.8 %)**: does not close |

Caveats: this corner is 1.60 V (spec minimum 1.62 V) and 100 °C (spec maximum
125 °C; the installed Liberty set has no 125 °C corner, so 125 °C is **not
published** by the library). Fan-out, clock-tree skew and wires are not in the
number. It is an arithmetic floor, not an STA result.

## Decision

- **Keep 1 Gb/s per lane as the target and 400 Mb/s as the fallback.** On this
  arithmetic the edge budget is not the limit at the stated capacitance
  budget, and the serializer closes with 27 % slack at the slow Liberty corner.
- **The binding risks are elsewhere**: the pad capacitance (P1), and the clock
  source, which the sibling PLL does not reach (spec C1–C6, DR-007).
- **1.5 Gb/s stays a stretch** and the same architecture does **not** reach it:
  at 750 MHz the one-mux reduction stage misses by 0.118 ns, so the stretch
  needs a split (for example 8:1→4:1 at a quarter-rate clock, then a custom
  4:1 final stage). That is not designed now.
- **Lane count**: 4 data + 1 forwarded clock lane (the README draft); fallback
  1 data + 1 clock; stretch 8 data + 1 clock. Ten signal pads for the target,
  at the 75 µm slot pitch (DR-001), is 750 µm of ring, plus supply cells.

Proposed; ratifies with the PR. Agents do not move the target toward the
fallback to make a result pass: if the T1 campaign misses, that is a recorded
miss, and a change is a new decision record.

## Alternatives considered

- **Lower the target to 800 Mb/s or 400 Mb/s now**: premature; the arithmetic
  shows slack at 1 Gb/s. Rejected.
- **Make the pad capacitance budget tighter (≤ 1 pF)**: unattainable on
  unpublished data and not needed by this arithmetic. Rejected.
- **A 16:1 serializer to ease the shift stage**: unnecessary at 500 MHz;
  would raise register count. Kept as a stretch option.

## Consequences

- Rows E5 and S3 carry these budgets as their stated derivation.
- The fallback is real but also depends on the clock: 200 MHz sits at the
  top edge of `sky130-pll`'s draft band (DR-007).

## Status notes

Proposed. All inputs and caveats are stated above; the receiver/package 1.0 pF
is an assumption that the first post-layout eye run must replace.
