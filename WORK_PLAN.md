# Work Plan

Roadmap generated from GitHub label state by the Guide role. Only the region between the markers is machine-generated.

<!-- guide:plan-body:start -->
## Operator Attention: Merge-Risk-Hold Pileup

Judge-approved PRs under a hold (`loom:blocked` or `loom:operator`) — only a human merge decision is missing.

- **#79**: feat: label DR-008 well nets and declare analog well and substrate ties

## Very Important

`loom:very-important` (one counts per workspace); every stage takes these first.

- **#100**: design: pad_cell ESD diode area is 400x the model default and shunts 107 mA at 1.25 V DC

## Important

`loom:important`; taken before unlabelled work.

- **#96**: sim: driver DC bench for V_OD and V_OS (spec rows E1, E2) across the G75 grid
- **#98**: Serializer S3: close setup timing at the 1.60 V and 1.76 V ss corners with 10 % clock uncertainty
- **#104**: layout: sky130_lvds_tx_driver_pad.gds does not regenerate byte-identically under any pinned klt

## Ready

Human-approved issues ready for implementation (`loom:issue`).

- **#103**: spec/ has two decision-record directories under a rule its README states wrongly

## In Progress

Issues currently being built (`loom:building`).

- **#77**: layout: label the DR-008 floating WELL net and tie the pad-pair substrate to VSSIO so item 11 analog ERC can declare both
- **#96**: sim: driver DC bench for V_OD and V_OS (spec rows E1, E2) across the G75 grid
- **#97**: sim: unpowered-pad DC bench for the fail-safe well biasing (spec rows P4, P4a, P4b; DR-008)
- **#99**: Remove gen_esd(): klt_gen() is the same klt gen wrapper, generalised

## PRs Awaiting Review

PRs waiting on Judge (`loom:review-requested`).

- **#105**: refactor: generate the ESD clamp through the shared klt_gen wrapper

## Approved (Awaiting Merge)

PRs that passed review and are queued for Champion auto-merge (`loom:pr`).

- **#79**: feat: label DR-008 well nets and declare analog well and substrate ties
- **#95**: docs: roadmap as of 2026-11-13

## Proposed

Issues carrying `loom:curated`.

- **#6**: Track the gap to T1 (klayout-tools design-evidence-tiers.md) *(curated)*
- **#77**: layout: label the DR-008 floating WELL net and tie the pad-pair substrate to VSSIO so item 11 analog ERC can declare both *(curated)*
- **#96**: sim: driver DC bench for V_OD and V_OS (spec rows E1, E2) across the G75 grid *(curated)*
- **#97**: sim: unpowered-pad DC bench for the fail-safe well biasing (spec rows P4, P4a, P4b; DR-008) *(curated)*
- **#98**: Serializer S3: close setup timing at the 1.60 V and 1.76 V ss corners with 10 % clock uncertainty *(curated)*
- **#100**: design: pad_cell ESD diode area is 400x the model default and shunts 107 mA at 1.25 V DC *(curated)*

## Proposed (Architect / Hermit)

- **#101**: Remove manifests/design-evidence-tiers.md: a byte-identical copy of the pinned klt wheel's own package data *(hermit)*

## Epics

_None._

## Backlog Balance

| Bucket | Count |
|------|-------|
| Operator merge-risk holds | 1 |
| Very important | 1 |
| Important | 3 |
| Ready (`loom:issue`) | 1 |
| In Progress (`loom:building`) | 4 |
| PRs awaiting review | 1 |
| Approved PRs awaiting merge | 2 |
| Curated | 6 |
| Architect / Hermit proposals | 1 |
| Active epics | 0 |
<!-- guide:plan-body:end -->
