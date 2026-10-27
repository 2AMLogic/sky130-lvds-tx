# Block manifest and tier-verdict record

`klt signoff` input and committed output for this block's T1 tier. The
manifest declares what is cited; the `.signoff.json` is the **verdict of
record**, produced by the regeneration command below. Never hand-edit it.

## Files

- **`sky130-lvds-tx.json`** — block manifest: `kind: mixed-signal`, plus
  per-item evidence citations. `partition_boundary` is the boundary sentence of
  the PROPOSED spec (`spec/target-spec.md`), used for both partitions; it moves
  at ratification (#2).
  - **Item 1, analog (`1.analog`)** cites
    [`verification/signoff/evidence/item-1-analog-design-sources.json`](../verification/signoff/evidence/item-1-analog-design-sources.json),
    produced by `klt signoff --attest 1` from
    [`verification/signoff/item-1-analog-inventory.json`](../verification/signoff/item-1-analog-inventory.json)
    (schematics, symbols, derived netlists; see [`design/README.md`](../design/README.md)).
    The manifest's `content_hash` is the sha256 of the inventory. The digital
    partition's item 1 is uncited.
  - **Item 10 (repo hygiene)** is the only cited item. It cites
    [`verification/signoff/evidence/item-10-repo-hygiene.json`](../verification/signoff/evidence/item-10-repo-hygiene.json),
    produced by `klt signoff --attest 10` from
    [`verification/signoff/item-10-inventory.json`](../verification/signoff/item-10-inventory.json).
    The manifest's `content_hash` for item 10 is the sha256 of the inventory
    file (`item-10-inventory.json`), not of the envelope.
  - Every other item is uncited and renders `unmet` / `no_evidence`; the
    evidence lands under #2, #3, #4 and the design issues, tracked in #6.
- **`design-evidence-tiers.md`** — the T1-T4 checklist the grader parses.
  Vendored **byte-identical** from
  [`2AMLogic/klayout-tools@267ea83a`](https://github.com/2AMLogic/klayout-tools/blob/267ea83a0510bcb61d2956058095201c0f481ff7/docs/design-evidence-tiers.md)
  `docs/design-evidence-tiers.md` (MIT-licensed upstream; this repo's
  Apache-2.0 `LICENSE` does not relicense the vendored copy). Re-vendor and
  regenerate the record in the same PR when upstream moves.
- **`sky130-lvds-tx.signoff.json`** — the verdict of record.

## klt pin

`klt signoff --attest` (klayout-tools#2844) is not in any PyPI release; the
latest, 0.7.0, rejects the flag. The pin is therefore a **commit**:
`2AMLogic/klayout-tools@dce956c3c39995643ff2a5c31b53c474b3c2aada`
(`0.7.1.dev1755+gdce956c3c399`). Move to the first release containing
`--attest`, and regenerate every record, when one exists. The pin lives in
`.github/workflows/signoff.yml` (`KLT_COMMIT`).

## Regenerate

```console
KLT="uvx --from git+https://github.com/2AMLogic/klayout-tools@dce956c3c39995643ff2a5c31b53c474b3c2aada klt"
$KLT signoff --attest 10 --inventory verification/signoff/item-10-inventory.json \
             -o verification/signoff/evidence/item-10-repo-hygiene.json
# if the inventory changed, copy its sha256 (provenance.input.content_hash) into the manifest
$KLT signoff --attest 1 --inventory verification/signoff/item-1-analog-inventory.json \
             -o verification/signoff/evidence/item-1-analog-design-sources.json
$KLT signoff --manifest manifests/sky130-lvds-tx.json \
             --tiers-doc manifests/design-evidence-tiers.md \
             --format json > manifests/sky130-lvds-tx.signoff.json
```

`--manifest` exits `3` when some T1 item is `unmet` (a clean run; the honest
state today) and `0` when all are met. The item 10 envelope records the hash
of every inventoried file (including the workflow), so editing any of them
requires re-attesting, then re-rendering the record, in the same PR.

## Freshness is CI-enforced

`.github/workflows/signoff.yml` re-attests items 10 and 1 (analog) with `--check` and
re-renders the report, failing on any byte difference from the committed
record.

## Current verdict

Not T1: 3 of 22 items met (item 10 once per partition; item 1, analog). All others are
`unmet` / `no_evidence`.
