# Work Plan

Roadmap generated from GitHub label state by the Guide role. Only the region between the markers is machine-generated. **Those rows are a point-in-time snapshot from when the region was last regenerated, not live state — some may since have closed or changed label. To recover the generation time, run `git log -1 --format=%cI -- WORK_PLAN.md`; the live labels are authoritative.**

<!-- guide:plan-body:start -->
## Operator Attention: Merge-Risk-Hold Pileup

Judge-approved PRs under a hold (`loom:blocked` or `loom:operator`) — only a human merge decision is missing.

- **#79**: feat: label DR-008 well nets and declare analog well and substrate ties
- **#95**: docs: roadmap as of 2026-11-13

## Very Important

`loom:very-important` (one counts per workspace); every stage takes these first.

_None._

## Important

`loom:important`; taken before unlabelled work.

_None._

## Ready

Human-approved issues ready for implementation (`loom:issue`).

_None._

## In Progress

Issues currently being built (`loom:building`).

- **#77**: layout: label the DR-008 floating WELL net and tie the pad-pair substrate to VSSIO so item 11 analog ERC can declare both
- **#103**: spec/ has two decision-record directories under a rule its README states wrongly
- **#125**: Re-run sim/unpowered-pad bench against the ESD-fixed pad cell (cd0c89a)
- **#128**: WORK_PLAN.md's generated region carries no generated-at timestamp, so a stale snapshot reads as current truth

## PRs Awaiting Review

PRs waiting on Judge (`loom:review-requested`).

- **#117**: docs(spec): state the decision-record placement rule semantically
- **#131**: docs: state WORK_PLAN snapshot semantics in header, name generation-time recovery
- **#132**: sim(unpowered-pad): re-run the grid against the ESD-fixed pad cell (cd0c89a)

## Approved (Awaiting Merge)

PRs that passed review and are queued for Champion auto-merge (`loom:pr`).

- **#79**: feat: label DR-008 well nets and declare analog well and substrate ties
- **#95**: docs: roadmap as of 2026-11-13

## Proposed

Issues carrying `loom:curated`.

- **#6**: Track the gap to T1 (klayout-tools design-evidence-tiers.md) *(curated)*
- **#77**: layout: label the DR-008 floating WELL net and tie the pad-pair substrate to VSSIO so item 11 analog ERC can declare both *(curated)*
- **#114**: Document (and file upstream) the two klt/host toolchain frictions worked around in PR #111 *(curated)*
- **#125**: Re-run sim/unpowered-pad bench against the ESD-fixed pad cell (cd0c89a) *(curated)*
- **#128**: WORK_PLAN.md's generated region carries no generated-at timestamp, so a stale snapshot reads as current truth *(curated)*

## Proposed (Architect / Hermit)

- **#101**: Remove manifests/design-evidence-tiers.md: a byte-identical copy of the pinned klt wheel's own package data *(hermit)*

## Epics

_None._

## Backlog Balance

| Bucket | Count |
|------|-------|
| Operator merge-risk holds | 2 |
| Very important | 0 |
| Important | 0 |
| Ready (`loom:issue`) | 0 |
| In Progress (`loom:building`) | 4 |
| PRs awaiting review | 3 |
| Approved PRs awaiting merge | 2 |
| Curated | 5 |
| Architect / Hermit proposals | 1 |
| Active epics | 0 |
<!-- guide:plan-body:end -->
