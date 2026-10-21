# Work Plan

Roadmap generated from GitHub label state by the Guide role. Only the region between the markers is machine-generated.

<!-- guide:plan-body:start -->
## Operator Attention: Merge-Risk-Hold Pileup

Judge-approved PRs under a hold (`loom:blocked` or `loom:operator`) — only a human merge decision is missing.

- **#8**: ci: add T1 signoff manifest, item 10 attestation and freshness workflow
- **#14**: build: wire pnpm lint/test/check scripts to RTL lint and smoke bench

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

- **#5**: Signoff scaffolding: block manifest, committed klt signoff record, and CI (T1 item 10)
- **#13**: Wire package.json check:ci/check:all/test/lint to the real verification checks (currently vacuous exit-0 stubs)

## PRs Awaiting Review

PRs waiting on Judge (`loom:review-requested`).

_None._

## Approved (Awaiting Merge)

PRs that passed review and are queued for Champion auto-merge (`loom:pr`).

- **#8**: ci: add T1 signoff manifest, item 10 attestation and freshness workflow
- **#14**: build: wire pnpm lint/test/check scripts to RTL lint and smoke bench
- **#15**: Bump Repo Skills 0.24.3 -> 0.24.7

## Proposed

Issues carrying `loom:curated`.

- **#5**: Signoff scaffolding: block manifest, committed klt signoff record, and CI (T1 item 10) *(curated)*
- **#6**: Track the gap to T1 (klayout-tools design-evidence-tiers.md) *(curated)*

## Proposed (Architect / Hermit)

_None._

## Epics

_None._

## Backlog Balance

| Bucket | Count |
|------|-------|
| Operator merge-risk holds | 2 |
| Very important | 0 |
| Important | 0 |
| Ready (`loom:issue`) | 0 |
| In Progress (`loom:building`) | 2 |
| PRs awaiting review | 0 |
| Approved PRs awaiting merge | 3 |
| Curated | 2 |
| Architect / Hermit proposals | 0 |
| Active epics | 0 |
<!-- guide:plan-body:end -->
