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
    The manifest's `content_hash` is the sha256 of the inventory.
  - **Item 1, digital (`1.digital`)** cites
    [`verification/signoff/evidence/item-1-design-sources-digital.json`](../verification/signoff/evidence/item-1-design-sources-digital.json),
    produced by `klt signoff --attest 1` from
    [`verification/signoff/item-1-digital-inventory.json`](../verification/signoff/item-1-digital-inventory.json)
    (serializer RTL, synthesis request, committed gate-level netlist).
  - **Item 2, digital (`2.digital`)** cites
    [`verification/signoff/evidence/item-2-layout-digital.json`](../verification/signoff/evidence/item-2-layout-digital.json),
    a hand-written `generic` envelope bound to the routed GDS
    `flow/serializer/serializer_routed.gds` (`klt signoff --attest` has no item 2
    producer, 2AMLogic/klayout-tools#4188). Its `regeneration` claim is backed by
    `verification/signoff/check-serializer-pnr.sh` (`local_only`); see
    [`flow/serializer/PNR.md`](../flow/serializer/PNR.md).
  - **Item 2, analog (`2.analog`)** cites
    [`verification/signoff/evidence/item-2-layout-analog-r2.json`](../verification/signoff/evidence/item-2-layout-analog-r2.json)
    (append-only; the earlier `item-2-layout-analog.json` is kept as history, bound to the unrouted GDS),
    a hand-written `generic` envelope bound to
    `layout/sky130_lvds_tx_driver_pad.gds` (the CI-pinned klt has no item 2
    producer; same route as `2.digital`). Its `regeneration` claim is backed by
    `verification/signoff/check-driver-pad-gds.sh` (`local_only`); see
    [`layout/README.md`](../layout/README.md). The manifest's `content_hash` is the
    sha256 of the GDS, not of the envelope. The driver is routed (#48); `ddr_mux` and `predriver` are placement-only.
  - **Item 3, digital (`3.digital`)** cites
    [`verification/signoff/evidence/item-3-drc-digital.json`](../verification/signoff/evidence/item-3-drc-digital.json),
    the `klt drc --deck sky130` report on `flow/serializer/serializer_routed.gds`
    (`status: clean`, 0 violations). The manifest's `content_hash` is the sha256 of the GDS.
    Coverage disclosure (verbatim from the report's `coverage` block) is in
    [`verification/README.md`](../verification/README.md#item-3-drc).
  - **Item 3, analog (`3.analog`)** cites
    [`verification/signoff/evidence/item-3-drc-analog-r3.json`](../verification/signoff/evidence/item-3-drc-analog-r3.json)
    (re-run with the CI-pinned klt on the routed GDS; the earlier `item-3-drc-analog.json` and `-r2.json` are kept as history),
    the `klt drc --deck sky130 --top sky130_lvds_tx_driver_pad` report on
    `layout/sky130_lvds_tx_driver_pad.gds`: **`status: violations`, 486 violations**, so the
    row grades `unmet` / `check_failed`. It is cited, not waived: the report is the evidence. All 486 are in the
    unmodified stock pad frame; classification in [`layout/README.md`](../layout/README.md#drc-of-the-stock-pad-frame-issue-44).
  - **Item 10 (repo hygiene)** is cited for both partitions. It cites
    [`verification/signoff/evidence/item-10-repo-hygiene-r3.json`](../verification/signoff/evidence/item-10-repo-hygiene-r2.json),
    produced by `klt signoff --attest 10` from
    [`verification/signoff/item-10-inventory.json`](../verification/signoff/item-10-inventory.json).
    The manifest's `content_hash` for item 10 is the sha256 of the inventory
    file (`item-10-inventory.json`), not of the envelope.
  - **Item 9 (testbenches shipped)** is the second cited item. It cites
    [`verification/signoff/evidence/item-9-testbenches-r3.json`](../verification/signoff/evidence/item-9-testbenches-r2.json),
    produced by `klt signoff --attest 9` from
    [`verification/signoff/item-9-inventory.json`](../verification/signoff/item-9-inventory.json).
    Item 9 is kind-independent: the bare key `"9"` serves both partitions, so
    one inventory lists the analog and digital benches together. The
    `content_hash` is the sha256 of the inventory file. Its `cold_start` is
    [`verification/signoff/cold-start.sh`](../verification/signoff/cold-start.sh)
    (digital serializer bench with negative control, then the analog smoke through
    `klt sim`, which goes to the batch fleet on a dispatch worker).
    The cold start is `local_only`, so CI re-hashes the inventory but does not re-run it.
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

`klt signoff --attest` (klayout-tools#2844) and the `local_only` check flag are
in the PyPI release `klayout-tools==0.8.0`, which is the pin. The pin lives in
`.github/workflows/signoff.yml` (`KLT_VERSION`). A git build reports a dev
version and does not satisfy `==0.8.0` (klayout-tools#2823).

## Regenerate

```console
KLT="uvx --from klayout-tools==0.8.0 klt"
$KLT signoff --attest 9 --inventory verification/signoff/item-9-inventory.json \
             -o verification/signoff/evidence/item-9-testbenches-r3.json   # runs the cold start (sim leg: batch fleet)
$KLT signoff --attest 10 --inventory verification/signoff/item-10-inventory.json \
             -o verification/signoff/evidence/item-10-repo-hygiene-r3.json
# if the inventory changed, copy its sha256 (provenance.input.content_hash) into the manifest
$KLT signoff --attest 1 --inventory verification/signoff/item-1-analog-inventory.json \
             -o verification/signoff/evidence/item-1-analog-design-sources.json
$KLT signoff --attest 1 --inventory verification/signoff/item-1-digital-inventory.json \
             -o verification/signoff/evidence/item-1-design-sources-digital.json
$KLT signoff --manifest manifests/sky130-lvds-tx.json \
             --tiers-doc manifests/design-evidence-tiers.md \
             --format json > manifests/sky130-lvds-tx.signoff.json
```

`--manifest` exits `3` when some T1 item is `unmet` (a clean run; the honest
state today) and `0` when all are met. The item 10 envelope records the hash
of every inventoried file (including the workflow), so editing any of them
requires re-attesting, then re-rendering the record, in the same PR.

## Freshness is CI-enforced

`.github/workflows/signoff.yml` re-attests item 1 (digital), item 10, item 1
(analog) and item 9 with `--check` and re-renders the report, failing on any byte difference
from the committed record. Item 2 (digital and analog) is not re-attested, since `klt signoff
--attest` has no item 2 producer (klayout-tools#4188); they are hash-bound only by that
full-record comparison.

## Current verdict

Not T1: 9 of 22 items met (item 10 once per partition; item 9, both partitions; item 1,
both partitions; item 2, both partitions; item 3, digital only: the analog DRC report is not clean). All others are
`unmet` / `no_evidence`.
