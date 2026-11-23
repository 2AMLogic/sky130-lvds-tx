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
    [`verification/signoff/evidence/item-1-analog-design-sources-r2.json`](../verification/signoff/evidence/item-1-analog-design-sources-r2.json),
    produced by `klt signoff --attest 1` from
    [`verification/signoff/item-1-analog-inventory.json`](../verification/signoff/item-1-analog-inventory.json)
    (schematics, symbols, derived netlists; see [`design/README.md`](../design/README.md)).
    The manifest's `content_hash` is the envelope's `provenance.input.content_hash`
    (the input-set digest over the inventoried files; klt 0.9.1 expands an
    `--inventory` into `provenance.input.paths` and pins the set digest, no longer
    the inventory file's own sha256).
  - **Item 1, digital (`1.digital`)** cites
    [`verification/signoff/evidence/item-1-design-sources-digital-r2.json`](../verification/signoff/evidence/item-1-design-sources-digital-r2.json),
    produced by `klt signoff --attest 1` from
    [`verification/signoff/item-1-digital-inventory.json`](../verification/signoff/item-1-digital-inventory.json)
    (serializer RTL, synthesis request, committed gate-level netlist; regenerated
    under the pinned `yowasp-yosys` so the netlist freshness leg genuinely
    passes -- the earlier `item-1-design-sources-digital.json` is kept as history,
    bound to a host-yosys netlist build).
  - **Item 2, digital (`2.digital`)** cites
    [`verification/signoff/evidence/item-2-layout-digital-r3.json`](../verification/signoff/evidence/item-2-layout-digital-r3.json),
    produced by `klt signoff --attest 2 --input flow/serializer/serializer_routed.gds`
    (the item 2 producer, klayout-tools#4188) under the pinned attest pair
    (`klt 0.9.1` + `klayout 0.28.17.post1`), bound to the routed GDS
    `flow/serializer/serializer_routed.gds` re-closed against the current
    netlist by #119 (`regenerated_hash`
    `sha256:f5de09887d17301b9e8fe89fbdf97f84ec97d78ce362900790783e058d158f25`;
    the P&R that produced those bytes ran under `.venv-pnr`, disclosed in
    the envelope's `regeneration.generator`).
    Its `regeneration` claim is backed by
    `verification/signoff/check-serializer-pnr.sh` (`local_only`), which
    reproduces the GDS byte-identically at seed 1; see
    [`flow/serializer/PNR.md`](../flow/serializer/PNR.md). The P&R backend
    is net-name-sensitive: regenerating the netlist again would change the
    routed bytes even at identical connectivity, so the byte-compare is only
    expected to hold for the committed netlist (the check script's contract
    states this). The hand-written r2 envelope
    (`item-2-layout-digital-r2.json`, bound to the pre-#115 netlist's
    `sha256:1cecbc447…`) stays as history.
    `flow/serializer/RECORD.md` carries the netlist-regeneration context.
  - **Item 2, analog (`2.analog`)** cites
    [`verification/signoff/evidence/item-2-layout-analog-r5.json`](../verification/signoff/evidence/item-2-layout-analog-r5.json)
    (append-only; the earlier `item-2-layout-analog.json`, `-r2.json`, `-r3.json`
    and `-r4.json` are kept as history, bound to earlier GDS revisions and tool pins),
    produced by `klt signoff --attest 2 --input layout/sky130_lvds_tx_driver_pad.gds`
    (the item 2 producer, klayout-tools#4188) under the pinned pair
    (`klt 0.9.1` + `klayout 0.28.17.post1`, issue #104), bound to
    `layout/sky130_lvds_tx_driver_pad.gds` (the issue-#165 met5-completed
    GDS). Its `regeneration` claim is backed by
    `verification/signoff/check-driver-pad-gds.sh` (`local_only`); see
    [`layout/README.md`](../layout/README.md). The manifest's `content_hash` is the
    sha256 of the GDS, not of the envelope. The driver is routed (#48); `ddr_mux` and `predriver` are placement-only.
  - **Item 3, digital (`3.digital`)** cites
    [`verification/signoff/evidence/item-3-drc-digital-r3.json`](../verification/signoff/evidence/item-3-drc-digital-r3.json),
    the `klt drc --deck sky130` report on `flow/serializer/serializer_routed.gds`
    (`status: clean`, 0 violations; re-run under `.venv-pnr` on the #119
    re-closure GDS; the r2 report on the previous implementation is kept as
    history). The manifest's `content_hash` is the sha256 of the GDS.
    Coverage disclosure (verbatim from the report's `coverage` block) is in
    [`verification/README.md`](../verification/README.md#item-3-drc).
  - **Item 3, analog (`3.analog`)** cites
    [`verification/signoff/evidence/item-3-drc-analog-r4.json`](../verification/signoff/evidence/item-3-drc-analog-r4.json)
    (re-run with klt `0.9.1` under `.venv-pnr` on the issue-#165 met5-completed
    GDS; the earlier `item-3-drc-analog.json`, `-r2.json` and `-r3.json` are kept
    as history), the `klt drc --deck sky130 --top sky130_lvds_tx_driver_pad`
    report on `layout/sky130_lvds_tx_driver_pad.gds`: **`status: violations`,
    458 violations**, all `met4` inside `sky130_ef_io__simple_pad_and_busses`,
    zero `met5` (the stock cells' free-end met5 findings are removed in the
    design, issue #165). The row grades **`met` through the disclosed
    foundry-cell exception** (operator ruling on #44, applied per issue #165;
    klayout-tools#4530) carried in the entry's `foundry_cell_exceptions`: one
    record — cell `sky130_ef_io__simple_pad_and_busses`, `cell_hash`
    `sha256:a27d049e…28ca`, rules `met4.space.1` 216 / `met4.enclosing.via3.1`
    160 / `met4.holes_area.1` 40 / `met4.width.1` 40 / `met4.area.1` 2,
    `bare_cell_layout` `layout/bare_pad_frame.gds` (two unmodified stock
    instances at the 75 um pitch, generated by `layout/gen_bare_pad_frame.py`),
    `bare_cell_report`
    [`item-3-drc-analog-r4-bare.json`](../verification/signoff/evidence/item-3-drc-analog-r4-bare.json)
    (458, identical per-rule counts, input hash = the bare layout's sha256).
    Nothing is waived beyond geometry inside that unmodified cell; the report is
    cited as evidence, not declared clean. Full record and grading conditions:
    [`layout/README.md`](../layout/README.md#foundry-cell-drc-exception-applied-issue-165).
  - **Item 4 (LVS)** is cited per partition with `klt lvs` reports (`engine: klayout`, `status: match`); the manifest's `content_hash` is the sha256 of the layout GDS.
    `4.digital` cites [`item-4-lvs-digital-r4.json`](../verification/signoff/evidence/item-4-lvs-digital-r4.json)
    (`gate-level-verilog`, `power_connectivity.status: "match"`; `VNB`/`VPB` are excluded and disclosed, not verified;
    re-run under `.venv-pnr` on the #119 re-closure GDS against the same run's routed verilog; the r3 report on the
    previous implementation is kept as history).
    `4.analog` cites [`item-4-lvs-analog-r3-scale-expanded.json`](../verification/signoff/evidence/item-4-lvs-analog-r3-scale-expanded.json)
    (the issue-#165 re-run on the met5-completed GDS, klt `0.9.1` under `.venv-pnr`, `input_verified: true`; the `r2` re-run on the earlier GDS and the unmodified-netlist `item-4-lvs-analog-r2.json`, `mismatch`, are kept as history),
    which compares against a derived netlist with `SCALE` substituted (klayout-tools#4406), not `design/driver/driver.spice`. Pad/ESD devices are outside the driver top.
    Details: [`verification/README.md`](../verification/README.md#t1-item-4-lvs-klt-lvs-digital-match-analog-match-scale-expanded-reference).
  - **Item 11 (power delivery, structural)** is cited per partition as an array (`klt erc` supply report + LVS report, digital also the P&R response).
    `11.digital` is **met**: [`item-11-erc-digital-r3.json`](../verification/signoff/evidence/item-11-erc-digital-r3.json) (`VCCD`, `VSS` one island each; n-well and asserted p-substrate ties checked), `item-4-lvs-digital-r4.json` (`power_connectivity: match`) and `flow/serializer/pnr.response.json` (`pdn: true`, tapcell named).
    The P&R response citation is current: #119 re-ran P&R from the committed
    netlist, so the response's `provenance.input.content_hash` names
    `serializer_synth.v`
    (`sha256:c9760e742c2d3979b42795345cce86394152de8d4a1bb0dd17c5328a79025353`)
    and `klt place-and-route --check` reports `match`. The earlier r2
    envelopes and response (bound to the pre-#115 netlist,
    `sha256:a353a87b…`) stay as history.
    `11.analog` is **met**: [`item-11-erc-analog-r2.json`](../verification/signoff/evidence/item-11-erc-analog-r2.json)
    (the issue-#165 re-run on the met5-completed GDS with klt `0.9.1` under
    `.venv-pnr`; the earlier analog ERC report is kept as history) plus
    `item-4-lvs-analog-r3-scale-expanded.json`. Two supply-spec gaps stay
    declared (the DR-008 floating well and the pad-pair substrate are not
    claimed); see [`verification/README.md`](../verification/README.md#t1-item-11-power-delivery-klt-erc-supply-spec).
  - **Item 10 (repo hygiene)** is cited for both partitions. It cites
    [`verification/signoff/evidence/item-10-repo-hygiene-r18.json`](../verification/signoff/evidence/item-10-repo-hygiene-r18.json),
    produced by `klt signoff --attest 10` from
    [`verification/signoff/item-10-inventory.json`](../verification/signoff/item-10-inventory.json)
    (append-only; r2-r17 are kept as history, bound to earlier workflow and
    spec revisions).
    The manifest's `content_hash` for item 10 is the sha256 of the inventory
    file (`item-10-inventory.json`), not of the envelope.
  - **Item 9 (testbenches shipped)** is the second cited item. It cites
    [`verification/signoff/evidence/item-9-testbenches-r9.json`](../verification/signoff/evidence/item-9-testbenches-r9.json),
    produced by `klt signoff --attest 9` from
    [`verification/signoff/item-9-inventory.json`](../verification/signoff/item-9-inventory.json)
    for the corrected transient measurements, stimulus metadata, grading
    regression test and nominal mux and pad waveform checks.
    Revisions 2 through 8 remain available.
    Item 9 is kind-independent: the bare key `"9"` serves both partitions, so
    one inventory lists the analog and digital benches together. The
    `content_hash` is the sha256 of the inventory file. Its `cold_start` is
    [`verification/signoff/cold-start.sh`](../verification/signoff/cold-start.sh)
    (digital serializer bench with negative control, then the analog smoke through
    `klt sim`, which goes to the batch fleet on a dispatch worker).
    The cold start is `local_only`, so CI re-hashes the inventory but does not re-run it.
  - **Item 5, digital (`5.digital`)** cites
    [`verification/serializer/rtl.report.json`](../verification/serializer/rtl.report.json),
    a `klt functional-verification` report of the serializer bit-exact suite
    (4/4 pass, seed 21, `environment.sdf: null` — the RTL, unannotated run;
    request beside it). The row stays `unmet` / `partial_coverage` with
    `detail.missing_kinds: ["sta"]` by construction: the Digital column needs
    a `klt sta` report **plus** this one, and the STA half is not citable
    until spec S3's "every Liberty corner" wording is settled
    (`flow/serializer/STA.md` records setup failing at the five slowest `ss`
    libraries — a ratification question, out of scope of #169). The item-7
    SDF-annotated half of the same task is staged but not citable at the
    pinned klt (portability gaps, `flow/serializer/SDF.md`).
  - Every other item is uncited and renders `unmet` / `no_evidence`; the
    evidence lands under #2, #3, #4 and the design issues, tracked in #6.
- **T1–T4 checklist (bundled in pinned `klayout-tools`)** — `klt signoff` reads
  the T1–T4 checklist directly from the pinned `klayout-tools==0.9.1` wheel's
  own package data (`docs/design-evidence-tiers.md`; upstream reference at tag
  [`2AMLogic/klayout-tools@v0.9.1`](https://github.com/2AMLogic/klayout-tools/blob/v0.9.1/docs/design-evidence-tiers.md)).
  The checklist is not vendored in-tree and `--tiers-doc` is not passed; the
  pinned `klt` release alone selects the checklist
  ([`spec/decisions/0006-unvendor-design-evidence-tiers.md`](../spec/decisions/0006-unvendor-design-evidence-tiers.md)).
- **`sky130-lvds-tx.signoff.json`** — the verdict of record.

## klt pin

`klt signoff --attest` (klayout-tools#2844), the `local_only` check flag and
the item 2 attest producer (`--input <layout stream>`; klayout-tools#4188) are
in the PyPI release `klayout-tools==0.9.1`, which is the pin. The pins live in
`scripts/setup-env.sh` (`KLT_VERSION`, plus `KLAYOUT_VERSION` for the klayout
module, which serialises the layout bytes) and `.github/workflows/signoff.yml`
(both). A git build reports a dev version and does not satisfy `==0.9.1`
(klayout-tools#2823). The previous pin `0.8.0` was wrong for item 2 analog:
it predates the attested driver-pad GDS and its `klt gen` renames 114 of the
GDS's 237 cells, so it could not regenerate the artifact at all (issue #104).

## Regenerate

```console
KLT="uvx --from klayout-tools==0.9.1 klt"
$KLT signoff --attest 9 --inventory verification/signoff/item-9-inventory.json \
             -o verification/signoff/evidence/item-9-testbenches-r9.json   # runs the cold start using KLT_SIM_BACKEND
$KLT signoff --attest 10 --inventory verification/signoff/item-10-inventory.json \
             -o verification/signoff/evidence/item-10-repo-hygiene-r18.json
# if the inventory changed, copy its sha256 (provenance.input.content_hash) into the manifest
$KLT signoff --attest 1 --inventory verification/signoff/item-1-analog-inventory.json \
             -o verification/signoff/evidence/item-1-analog-design-sources-r2.json
$KLT signoff --attest 1 --inventory verification/signoff/item-1-digital-inventory.json \
             -o verification/signoff/evidence/item-1-design-sources-digital-r2.json
# item 2 analog (producer from klayout-tools#4188; run it with the repo's pinned
# .venv klt so the recorded versions are the pins -- the regeneration claim it
# records is backed by the local_only gate below)
$KLT signoff --attest 2 --input layout/sky130_lvds_tx_driver_pad.gds \
             --generator "sh verification/signoff/check-driver-pad-gds.sh" \
             --regenerated-hash sha256:... \
             -o verification/signoff/evidence/item-2-layout-analog-rN.json
# item 3 analog (issue #165): full deck, never a rule subset, and the pinned
# klt 0.9.1 needs its klayout>=0.30 floor satisfied for `drc`, so run these
# under .venv-pnr; then the bare-cell leg of the foundry-cell exception
source .venv-pnr/bin/activate
klt drc --deck sky130 --pdk-root "$PDK_ROOT" --top sky130_lvds_tx_driver_pad --format json \
    layout/sky130_lvds_tx_driver_pad.gds > verification/signoff/evidence/item-3-drc-analog-rN.json
klayout -b -r layout/gen_bare_pad_frame.py   # writes layout/bare_pad_frame.gds
klt drc --deck sky130 --pdk-root "$PDK_ROOT" --top bare_pad_frame --format json \
    layout/bare_pad_frame.gds > verification/signoff/evidence/item-3-drc-analog-rN-bare.json
klt lvs --format json verification/signoff/lvs/item-4-analog-scale-expanded.request.json \
    > verification/signoff/evidence/item-4-lvs-analog-rN-scale-expanded.json
klt erc --top sky130_lvds_tx_driver_pad --format json \
    layout/sky130_lvds_tx_driver_pad.gds verification/signoff/erc/analog.supply-spec.json \
    > verification/signoff/evidence/item-11-erc-analog-rN.json
deactivate
# the foundry-cell exception's cell_hash (no klt subcommand prints it yet,
# klayout-tools#6946): identical from the block GDS, the bare layout or the
# stock GDS
.venv/bin/python3 -c 'from klayout_tools._provenance import cell_geometry_digest; \
    print(cell_geometry_digest("layout/sky130_lvds_tx_driver_pad.gds", \
                               "sky130_ef_io__simple_pad_and_busses"))'
$KLT signoff --manifest manifests/sky130-lvds-tx.json \
             --format json > manifests/sky130-lvds-tx.signoff.json
```

`--manifest` exits `3` when some T1 item is `unmet` (a clean run; the honest
state today) and `0` when all are met. The item 10 envelope records the hash
of every inventoried file (including the workflow), so editing any of them
requires re-attesting, then re-rendering the record, in the same PR. Any GDS
change refreshes the item 2 / 3 / 4 / 11 analog evidence in the same PR
(append-only records; issue #165 is the worked example).

## Freshness is CI-enforced

`.github/workflows/signoff.yml` re-attests item 1 (digital), item 10, item 1
(analog) and item 9 with `--check` and re-renders the report, failing on any byte difference
from the committed record. Item 2 (digital and analog) is not re-attested: the
analog regeneration claim is backed by the `local_only` PDK gate, and the
digital one by the `local_only` PnP check; the producer itself exists since
0.9.1 (klayout-tools#4188) and produced the analog r5 record. Both item 2
envelopes are hash-bound by that full-record comparison.

That comparison is `verification/signoff/check-verdict-record.sh`, shared by the CI
step and the local `pnpm check:signoff`: it renders `klt signoff` and requires the
bytes to equal the committed record (render exit 0 or 3 only). The local check is
therefore as strict as CI; klt's semantic `--check` is no longer used, so even a
whitespace or checklist-wording change needs a regenerated record.

## Repo-local disclosure notes (items 2 and 11)

Moved here when `manifests/design-evidence-tiers.md` was unvendored
([`spec/decisions/0006-unvendor-design-evidence-tiers.md`](../spec/decisions/0006-unvendor-design-evidence-tiers.md)):

- **Item 2 — Regeneration-freshness note (repo-local)**: a `regeneration`
  claim on this item is only as fresh as the netlist its generator runs on.
  The serializer digital partition was re-closed against the current
  `serializer_synth.v` — the pinned-`yowasp-yosys` regeneration of
  2AMLogic/sky130-lvds-tx#115 — by 2AMLogic/sky130-lvds-tx#119:
  `item-2-layout-digital-r3.json` records `regenerated_hash: sha256:f5de0988…`,
  reproduced byte-identically by `verification/signoff/check-serializer-pnr.sh`
  at seed 1 (the r2 envelope, bound to the pre-regeneration netlist's
  `sha256:1cecbc44…`, stays as history). The P&R backend is
  net-name-sensitive: a future regeneration of the netlist changes the routed
  GDS bytes even at identical connectivity, because OpenROAD's resizer and CTS
  follow net and instance names. A byte-compare failure after a netlist
  regeneration therefore means the digital evidence must be re-closed — as #119
  did — not that the flow broke; the analog partition's driver-pad GDS is
  unaffected.
- **Item 11 — Citation-freshness note (repo-local)**: a `klt place-and-route`
  response cited for this item pins its input netlist by content hash. The
  serializer digital partition's response is current: it was re-run from the
  regenerated netlist by 2AMLogic/sky130-lvds-tx#119, and its
  `provenance.input.content_hash` names the committed `serializer_synth.v`
  (`sha256:c9760e74…`, the pinned-`yowasp-yosys` regeneration of
  2AMLogic/sky130-lvds-tx#115), so `klt place-and-route --check` reports
  `match` and the `power.pdn`/tapcell facts it records describe the routed GDS
  the digital envelopes bind. The backend is net-name-sensitive, so a future
  netlist regeneration is expected to drift the response again; re-run P&R and
  the digital envelopes that cite it — as #119 did — rather than suppressing
  the check.

## Current verdict

Not T1: 14 of 22 T1 items met (item 10 once per partition; item 9, both partitions;
item 1, both partitions; item 2, both partitions; item 3, both partitions —
analog through the disclosed foundry-cell exception of issue #165; item 4,
both partitions; item 11, both partitions). Item 5 digital is cited but
`unmet` / `partial_coverage` (the STA half and spec S3 ratification are
pending, above); item 7 digital is uncited pending the klt pin bump
(`flow/serializer/SDF.md`). All others are `unmet` /
`no_evidence`.
