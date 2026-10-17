# spec

The target specification and its decision records. **Status: proposed, not
ratified.** Agents do not ratify their own spec; the status flips to ratified
only on human merge approval, recorded in the header of `target-spec.md`
(date, pull request).

| File | What it is |
|---|---|
| [`target-spec.md`](target-spec.md) | every parameter as target / fallback / stretch, with verification method, PVT corners, and deterministic/statistical marking; the clock-interface table against `sky130-pll`; the mixed-signal partition boundary |
| [`decision-records/DR-001-pdk-pad-vs-custom-pad-cell.md`](decision-records/DR-001-pdk-pad-vs-custom-pad-cell.md) | PDK pad vs custom pad cell, with the PDK I/O evidence |
| [`decision-records/DR-002-driver-device-flavours-and-supply.md`](decision-records/DR-002-driver-device-flavours-and-supply.md) | device flavours and supply per rail; common-mode regulation |
| [`decision-records/DR-003-serializer-ratio-and-clock-framing.md`](decision-records/DR-003-serializer-ratio-and-clock-framing.md) | 8:1 vs 7:1; DDR forwarded clock |
| [`decision-records/DR-004-serializer-reuse-from-gf180-tmds-tx.md`](decision-records/DR-004-serializer-reuse-from-gf180-tmds-tx.md) | serializer reuse from `gf180-tmds-tx` |
| [`decision-records/DR-005-low-swing-mode-driver-sharing.md`](decision-records/DR-005-low-swing-mode-driver-sharing.md) | low-swing stretch mode: separate slice |
| [`decision-records/DR-006-rate-lane-count-and-slow-corner-budget.md`](decision-records/DR-006-rate-lane-count-and-slow-corner-budget.md) | rate and lane targets; first-order slow-corner edge and timing budget |
| [`decision-records/DR-007-bit-clock-sourcing-and-pll-gap.md`](decision-records/DR-007-bit-clock-sourcing-and-pll-gap.md) | bit-clock requirement, the gap to `sky130-pll`, and the filed requirement |

Sibling references are by commit: `2AMLogic/gf180-tmds-tx`
`9a55961ab5e4608d42ffefb70308adcb4b42213e`; `2AMLogic/sky130-pll`
`76a4b68556f83ea0710e9fa16abf44e28f89d3bc`; `2AMLogic/sky130-adpll`
`6067a8a740f8ba448324fbcc70a5b3e1ecaad599`; `2AMLogic/2am` (REUSE.md)
`155fa0c156b14ffac6a8d39a4496a910de41aa67`. PDK revision read:
`open_pdks c6d73a35f524070e85faff4a6a9eef49553ebc2b`.

Records use the layout of the sibling `sky130-pll` repo
(`spec/decision-records/DR-NNN-<slug>.md`: Context, Decision, Alternatives
considered, Consequences, Status notes).
