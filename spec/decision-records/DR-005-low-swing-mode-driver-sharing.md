# DR-005: Low-swing (D-PHY-class) stretch mode: shared driver or separate slice

- **Status**: proposed
- **Date**: 2026-10-17
- **Author**: builder agent (issue #2)
- **Ratifies against / input to**: issue #2; `spec/target-spec.md` rows L1–L2
- **Supersedes**: none

## Context

The low-swing mode is a stretch described only as "D-PHY-class": a ~200 mV
differential high-speed swing around a low common mode. The MIPI
specifications are licensed to members; nothing from them was read or copied,
and the numbers below are this repo's own targets. `CLAUDE.md`: do not let the
stretch mode drive architecture before LVDS closes.

The LVDS driver (DR-002) cannot produce a low common mode: its bottom sink
needs the lowest pad level to leave sink headroom, and a ~0.2 V common mode
puts the low pad level near 0.1 V, below the ≈ 0.8 V that stack needs.

## Decision

**A separate low-swing driver slice on the same pad**, not a reconfiguration of
the LVDS H-bridge. It is a stretch item and is **not designed or sized now**.
The only architectural consequence accepted today is a **capacitance
allocation**: the pad capacitance budget (spec P1, 2.0 pF) is partitioned as
pad + ESD ≤ 1.2 pF, LVDS driver drains ≤ 0.5 pF, low-swing slice ≤ 0.3 pF, so
that adding the slice later cannot break the LVDS budget unnoticed. The
allocation is a budget, not a result.

Proposed; ratifies with the PR.

## Alternatives considered

- **Share the H-bridge** by lowering its supply or common mode: loses the
  headroom that makes the LVDS common mode work (DR-002). Rejected.
- **Defer the entire question**: the allocation costs nothing now and removes
  a surprise later. Rejected as the sole answer, kept as the implementation
  stance (no design).
- **Separate pad pair**: doubles pad area and breaks the "one pad, two modes"
  premise. Not preferred; revisit if the 0.3 pF allocation proves
  unachievable.

## Consequences

- Spec rows L1–L2 carry numbers marked stretch; they are not verified by the
  baseline campaign.
- The isolation of the unused slice (leakage and off-capacitance) must be
  shown when the stretch is attempted.

## Status notes

Proposed. Everything about the low-swing mode stays a stretch until LVDS
closes at the target rate.
