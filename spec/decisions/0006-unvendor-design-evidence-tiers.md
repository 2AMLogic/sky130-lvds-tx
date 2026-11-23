# 0006 — Remove vendored `design-evidence-tiers.md`; anchor the T1–T4 checklist on the pinned `klayout-tools` release

**Status**: accepted (repo/signoff tooling decision; no change to the block electrical spec)

## Decision

Remove the in-tree vendored copy `manifests/design-evidence-tiers.md` and drop
the `--tiers-doc` override from every caller (`package.json`,
`.github/workflows/signoff.yml`, and the regeneration recipe in
`manifests/README.md`). The pinned `klayout-tools` PyPI release alone
(`KLT_VERSION="0.9.1"`) selects the T1–T4 checklist via its own bundled package
data (`docs/design-evidence-tiers.md`, corresponding to
[`2AMLogic/klayout-tools@v0.9.1`](https://github.com/2AMLogic/klayout-tools/blob/v0.9.1/docs/design-evidence-tiers.md)).

This records and implements the **2026-11-23 operator ruling** (attended
`/fleet:decide` session, round `20261121-r19`, `q103`, recorded on issue
#101), which reverses the earlier decision to vendor
`manifests/design-evidence-tiers.md` in-tree and grade against it with
`--tiers-doc`.

## Context

Previously, this repository anchored the T1–T4 signoff skeleton twice:

1. As `KLT_VERSION` (`klayout-tools==0.9.1` in `.github/workflows/signoff.yml`
   and `scripts/setup-env.sh`), whose wheel already ships
   `klayout_tools/data/design-evidence-tiers.md` and reads it by default.
2. As a hand-vendored copy at `manifests/design-evidence-tiers.md` (originally
   snapshotted from `2AMLogic/klayout-tools@267ea83a`, 1053 lines) passed via
   `--tiers-doc`, with a standing manual re-vendor obligation and two
   repo-local disclosure notes appended for items 2 and 11.

Because the two anchors moved independently, the vendored copy drifted behind
the pinned `klayout-tools==0.9.1` wheel (whose bundled checklist is 1108 lines
and includes grading rules this block already relies on, such as the item 3
foundry-cell DRC exception). Maintaining a second copy in-tree created drift
without providing stronger provenance than the pinned wheel plus the committed
`manifests/sky130-lvds-tx.signoff.json` record (which hashes `source_doc` via
`source_doc_content_hash`).

## Alternatives declined

- **Re-vendor `docs/design-evidence-tiers.md` from `v0.9.1` and keep
  `--tiers-doc`** — ruled out by the 2026-11-23 operator ruling (`q103`): it
  preserves the dual-anchor maintenance obligation and will drift again at the
  next `klt` pin bump.

## Consequences

- `manifests/design-evidence-tiers.md` is deleted; `--tiers-doc` is removed
  from `package.json`, `.github/workflows/signoff.yml`, and
  `manifests/README.md`.
- The two repo-local disclosure notes previously appended to items 2 and 11 of
  the vendored file (covering the #115/#119 digital netlist-binding state and
  the P&R backend's net-name sensitivity) are preserved in
  `manifests/README.md` under "Repo-local disclosure notes (items 2 and 11)".
- `.github/workflows/signoff.yml` retains its fresh-run-versus-committed-record
  byte comparison (`cmp -s`), which catches any checklist or grading change
  when `KLT_VERSION` is bumped in the future.
- Regenerating `manifests/sky130-lvds-tx.signoff.json` at `klayout-tools==0.9.1`
  without `--tiers-doc` changes only `source_doc` (`docs/design-evidence-tiers.md`),
  `source_doc_content_hash`, the drifted item texts/notes, and the re-attested
  item 10 citation (`r17`); all 22 T1 item verdicts (`t1_met_count: 14`) and
  the overall tier result (`null`) remain unchanged.

## Reversal condition

Only a subsequent operator ruling explicitly requiring an in-tree checklist
override would reintroduce a vendored copy and `--tiers-doc`.
