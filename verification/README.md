# verification

Cold-start digital verification harness: cocotb + Icarus Verilog, PDK-free.

## Layout

    verification/
      lint_rtl.sh                 Verilator lint of rtl/*.v
      smoke/                      shared harness: runner.py hosts run_bench(), requirements.txt
        runner.py requirements.txt  pins cocotb (the placeholder DUT was retired, spec/decisions/0003)
      serializer/                 serializer bench (`pnpm test`), with negative control

Later benches follow `verification/<bench>/{runner.py,requirements.txt,test_<bench>.py,negative_control/}`
and call `run_bench()` from `smoke/runner.py` rather than copying it.

## Cold start

    pip install -r verification/smoke/requirements.txt
    python3 verification/serializer/runner.py   # serializer bench (what `pnpm test` runs); works from any directory
    verification/lint_rtl.sh

Prerequisites: `iverilog`, `verilator` (apt). Exit status is 0 only if the good
DUT passes every test **and** the negative control fails.

## Pinned toolchain

| Tool | Version |
|---|---|
| cocotb | 2.0.1 (`requirements.txt`) |
| Icarus Verilog | 13.0 (CI prints `iverilog -V`; Ubuntu apt may differ) |
| Verilator | 5.x (CI prints `verilator --version`) |

## Negative-control rule

A bench that has never failed is not known to be able to. Each bench ships a
broken DUT with the same module name and ports; the exact, unmodified test
module must fail against it. The runner exits non-zero if it passes.

## Result file

`results/serializer.json` (gitignored; `--out` to change): per-test pass/fail for
both legs of the bench, cocotb seed (`COCOTB_RANDOM_SEED` overrides), python/cocotb/iverilog
versions, `git rev-parse HEAD`, and `overall`.

Reuse decision for the sibling's runner: `spec/decisions/0001-verification-runner-kept-separate.md`.

## Item 3 DRC

T1 checklist item 3, one `klt drc` report per partition, committed under
`verification/signoff/evidence/` and cited from `manifests/sky130-lvds-tx.json`.
Deck `sky130` (content hash `sha256:072b456a6c867ff7244bfc287908a960c265628b3c26a64db5506c4bb124d267`,
`released: false`), PDK `sky130A` at open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7`, klt `0.8.0` for the analog `r3` report (the CI pin, `KLT_VERSION` in `signoff.yml`) and `0.8.1.dev181+g70d73835514c` for the digital one.

    export PDK_ROOT=~/.ciel PDK=sky130A
    klt drc --deck sky130 --pdk-root "$PDK_ROOT" --top sky130_lvds_tx_driver_pad --format json \
        layout/sky130_lvds_tx_driver_pad.gds > verification/signoff/evidence/item-3-drc-analog-r3.json
    klt drc --deck sky130 --pdk-root "$PDK_ROOT" --format json \
        flow/serializer/serializer_routed.gds > verification/signoff/evidence/item-3-drc-digital.json
    klt drc --check verification/signoff/evidence/item-3-drc-analog-r3.json --pdk-root "$PDK_ROOT"
    klt drc --check verification/signoff/evidence/item-3-drc-digital.json --pdk-root "$PDK_ROOT"

(`klt drc` exits 3 on violations; the report is still written.) `--check` is `local_only`:
it needs the PDK and is not run in CI.

| Partition | Status | Violations |
|---|---|---|
| digital (`serializer_routed.gds`) | `clean` | 0 |
| analog (`sky130_lvds_tx_driver_pad.gds`) | `violations` | 486 |

**Analog is not clean, and nothing was waived or relaxed.** All 486 violations are
`met4`/`met5` rules (`met4.space.1` 216, `met4.enclosing.via3.1` 160, `met4.holes_area.1` 40,
`met4.width.1` 40, `met4.area.1` 2, `met5.width.1` 26, `met5.area.1` 2), and every one has
`source_cell` `sky130_ef_io__simple_pad_and_busses` or `sky130_ef_io__analog_noesd_pad`, i.e.
the stock pad frame instantiated by `layout/gen_driver_pad.py`, not geometry drawn here. The
analog layout is the routed driver beside the stock pad pair (`layout/README.md`); the routing
(met1-met3, #48) adds no violation. Issue #44 traced them: they reproduce
on the unmodified PDK cells, the foundry's own deck flags the same met4/met5 width, spacing,
enclosure and area rules, and the met5 ones are cell-edge stripes that close when cells abut.
The classification, and what stays unestablished (`met4.holes_area.1`, `met5.area.1`, and whether
the foundry waives the I/O library), is in
[`layout/README.md`](../layout/README.md#drc-of-the-stock-pad-frame-issue-44). The earlier report
`item-3-drc-analog.json` and `item-3-drc-analog-r2.json` are kept (append-only); the manifest now cites
`item-3-drc-analog-r3.json`, the same deck re-run with the CI-pinned klt (`0.8.0`) on the routed GDS
(`sha256:17a471bc…3c71`, the committed file; `r2` was bound to the earlier placement-only stream,
`sha256:4cbd2819…e488`, so it was stale). Same 486, same per-rule counts, and by `source_cell` 458 in
`sky130_ef_io__simple_pad_and_busses` and 28 in `sky130_ef_io__analog_noesd_pad`; none in a cell drawn here.

**Coverage, quoted verbatim from each report's `coverage` block** (quote the committed report,
not this copy, if they differ):

- `deck_scope` (both): `["cap2m", "capm", "ct", "difftap", "li", "licon", "m1", "m2", "m3", "m4", "m5", "npc", "nsdm", "nwell", "poly", "psdm", "rpm", "urpm", "via", "via2", "via3", "via4", "x"]`
- `layers_in_stream_without_rules`, analog: `["66/13", "70/5", "70/16", "71/5", "71/16", "72/5", "72/16"]`
- `layers_in_stream_without_rules`, digital: `["64/5", "64/16", "64/59", "67/5", "67/16", "68/5", "68/16", "69/5", "69/16", "72/5", "72/16", "81/4", "83/44", "122/16", "235/4", "236/0"]`
- `rules_skipped`, analog (48): `areaid_re.ongrid.1`, `capm.*`/`capm2.*` (9), `hvntm`, `hvtp`, `hvtr`, `lvtn`, `mf`, `ncm`, `nsm`, `pad`, `pwbm`, `pwde`, `pwell_rs`, `tunm`, `uhvi`, `vhvi`, `vpp` `.angle.1`/`.ongrid.1`, `urpm.width.1`, `met3.enclosing.capm.1`, `met4.enclosing.capm2.1`, `met4.enclosing.via4.1`, `met5.enclosing.via4.1`, `via4.angle.1`, `via4.ongrid.1`, `via4.space.1`, `via4.width.1`. Full list in the report.
- `rules_skipped`, digital (48): the analog list without `hvtp.*`, `met4.enclosing.via4.1`, `met5.enclosing.via4.1` and the four `via4.*` rules, plus `dnwell.angle.1`, `dnwell.ongrid.1`, `hvi.angle.1`, `hvi.ongrid.1`, `nwell.enclosed.hvi.1`, `rpm.angle.1`, `rpm.ongrid.1`, `rpm.width.1`. Full list in the report.
- Skipped rules are `inapplicable` / `no_applicable_geometry` in the report, and `unmodeled_rules` lists DRM rules the curated deck does not transcribe at all.
- Analog `voltage_domain_warnings`: the `hvi` (75/20) thick-oxide marker is modelled only for device recognition and `nwell.enclosed.hvi.1`; geometry drawn inside it is checked at general-case thresholds, not the medium-voltage ones (`difftap.14` etc.). Pad/ESD and 5 V device layers are therefore **not** fully covered by this deck.

## T1 item 4: LVS (`klt lvs`): digital `match`, analog `match` (scale-expanded reference)

Two probe runs, one per partition, `engine: klayout` with the curated `sky130`
deck. Requests: `verification/signoff/lvs/item-4-{analog,digital}.request.json`;
reports: `verification/signoff/evidence/item-4-lvs-{analog,digital}.json`.
The manifest cites `item-4-lvs-digital-r2.json` (`4.digital`) and
`item-4-lvs-analog-r2-scale-expanded.json` (`4.analog`); both grade `met`.
**The analog citation compares against a derived netlist, not `design/driver/driver.spice`:**
`verification/signoff/lvs/expand-scale.py` substitutes the `SCALE=11` value into `m={SCALE}`
because the converter does not evaluate it (klayout-tools#4406). The unmodified-netlist report
`item-4-lvs-analog-r2.json` stays `mismatch` (8 unmatched devices, all the `SCALE` slice) and is
kept as append-only evidence. The pad/ESD devices are outside the driver top and are not covered
by this LVS. Reports are append-only; earlier ones are kept.

| Partition | `status` | `power_connectivity.status` | Why |
|---|---|---|---|
| Analog (`sky130_lvds_tx_driver` vs `design/driver/driver.spice`) | `mismatch` unmodified netlist; `match` scale-expanded (cited) | `unchecked` (not applicable to `subckt-call`) | `item-4-lvs-analog.json` (placement-only layout): 309 devices and 500 nets extracted against 11 and 29, 0 matched. Re-run as `item-4-lvs-analog-r2.json` after routing (#48), with `flatten_*`, `combine_devices` and `compare_mos_flavour`: 89/89 devices, 50/50 nets, 81 and 37 matched; the 8 unmatched are the `SCALE=11` slice, whose `m={SCALE}` the converter does not evaluate (klayout-tools#4406). With the scale substituted into a derived netlist (`item-4-lvs-analog-r2-scale-expanded.json`) the same layout is `match` (89/89, 50/50, 18/18 pins). |
| Digital (`serializer_routed.gds` vs `serializer_routed.v`, `gate-level-verilog`) | `match` | `match` | `item-4-lvs-digital-r2.json` (klt with the #4363 fix): signal compare matches, `power_connectivity.status: "match"`, no findings, `reference.form: "gate-level-verilog"`, report `--check` clean. The `VNB`/`VPB` well-layer LEF pins (248 instances) are **excluded and disclosed** by the tool, not verified: substrate continuity is not modelled in abstract-cell extraction. The first report `item-4-lvs-digital.json` (`mismatch`, `VNB` finding) is kept as append-only evidence. |

**Digital `VNB` finding: diagnosed (#49), tool gap, not a flow defect.** Record:
`verification/signoff/evidence/item-4-lvs-digital-diagnosis.md`. A transistor-level
`klt extract` of the same GDS (no `--abstract-cells`) puts all 359 NMOS bodies on
`VGND|VSS` and all 360 PMOS bodies on `VCCD|VPB|VPWR`, and the routed DEF ties `VNB`
to `VSS` in `SPECIALNETS`. The two outliers come from how abstract extraction
probes the LEF `pwell` pin at its bounding-box centre, where parent routing
(`word_clk` met1 over `a21oi_1_0`, the `VCCD` met5 strap over `a22o_1_1`) is picked up.
Tracked upstream as 2AMLogic/klayout-tools#4363. The report therefore stays
`power_connectivity: mismatch`; the finding is not waived and `options.power_connectivity`
stays `true`. #4363 has since landed (klayout-tools PR #4366, `6f28dd6`; no PyPI release includes it yet, 0.8.0 predates it), and the re-run is `item-4-lvs-digital-r2.json`, `match`. `VNB`/`VPB` are now reported under `excluded_pins` rather than checked, so the PDN tie of `VNB` rests on the DEF `SPECIALNETS` and transistor-level extraction evidence in the diagnosis record.

Warnings only, digital: `topology` x3 (empty `nfet`/`pfet`/`pnp` classes, not real),
`topology.power_only_pruned`, `topology.reference_port_alias_joined` x3
(`word_clk`, `dout[0]`, `dout[1]`), `topology.top_level_pins_anchored`.
Analog: `device.body_unverified` (122 NMOS, 185 PMOS: no named tap nets),
`device.geometry_not_compared` and `device.placeholder_value` (`res_high_po`).

The deck does distinguish `g5v0d10v5` from `01v8` (`compare_mos_flavour`: a
swapped reference card gives `device.class`). Pad/ESD devices (the clamp, `D1`,
the pad frame) are outside the driver top and remain not established; the
`met` grade for item 4 covers the driver and serializer partitions only. The
unmodified-netlist analog `r2` report is `mismatch` only because of the
converter gap above (klayout-tools#4406); the manifest cites the scale-expanded
`match` report instead, and grades `4.analog` and `4.digital` `met`.

Digital needs `layout.abstract_cells` (`sky130_fd_sc_hd__*`) plus the library LEF;
without it the routed GDS extracts 719 flat transistors against a 0-device
reference. Re-run with:

    export PDK_ROOT=~/.ciel PDK=sky130A
    klt lvs --format json verification/signoff/lvs/item-4-digital.request.json > verification/signoff/evidence/item-4-lvs-digital-r2.json
    klt lvs --check verification/signoff/evidence/item-4-lvs-digital-r2.json   # drift check

The digital `r2` report was produced with
`uvx --from git+https://github.com/2AMLogic/klayout-tools@6f28dd6d74de81845995045c87689961092df924 klt`
(0.8.1.dev350), since the fix is not yet in a release.

The digital request names the LEF by absolute path; edit it for your `PDK_ROOT`.

## T1 item 11: power delivery (`klt erc` supply spec)

Specs: `verification/signoff/erc/{analog,digital}.supply-spec.json`. Reports (`klayout-tools==0.8.0`,
`klt erc --check` passes on both): `verification/signoff/evidence/item-11-erc-{analog,digital}.json`.

- **Digital: met.** Serializer `VCCD` and `VSS` each resolve to one island, zero findings, `erc_coverage.skipped` empty.
  Ties: `nwell_tap` (drawn n-well, dedicated tap layer) and `p_substrate_tap` (native substrate, four asserted
  `well_boxes` strips, so it is named in `checked_by_well_assertion`; 7.3 % of drawn tap area falls outside the boxes).
  Negative control: moving that tie's `tap_boxes` away gives `erc.missing_tie` per strip. LVS `power_connectivity` is `match`; P&R `pdn: true`.
- **Analog: graded `met` by `klt signoff` (0.8.0), with two declared gaps below.** After #74 strapped the supplies, the top
  `sky130_lvds_tx_driver_pad` has one island each for `VCCD`, `VDDIO` and `VSSIO` (no `erc.unconnected_net`, no
  `erc.supply_short`), `erc_coverage.skipped` is empty. Ties: `nwell_vccd` (1.8 V PMOS bodies: predriver, `ddr_mux`,
  `drv_sel_XMP_sb`) and `nwell_vddio` (thick-oxide PMOS bodies on VDDIO), each separated from the other by `well_requires_boxes`
  built from the drawn well shapes of the leaf cells that own them (74 and 38 boxes; `hvi` cannot separate them, because the DR-008
  floating wells are thick and thin both). Because they are boxes, both are named in `checked_by_well_assertion`. `p_substrate_blocks`
  asserts the native substrate right of the pad pair (x >= 150 um). Negative control: re-pointing `nwell_vddio` at `VCCD` gives 19
  `erc.missing_tie`. The class selection is boxes, not `well_requires_cells`, because the pinned 0.8.0 does not accept the latter.
  - **Gap 1, DR-008 floating well not declared.** The pad-facing PMOS well net `WELL` carries no label in the GDS (only
    port nets are labelled), so a tie to it cannot be matched and is omitted rather than declared against a name that is not in the
    layout. Those wells (`XMSPA/B`, `XMWVA/B`, `XMWPA/B`, `XMGTA/B`) are in no tie, so their taps are not graded. The grader says
    `met` anyway.
  - **Gap 2, pad-pair substrate not tied.** Declaring the substrate over the whole die (`well_complement_of: 64/20`) gives two
    `erc.missing_tie` (the two pad cells' upper body, y 50-180 um): only one p-tap lies outside the n-wells in that area and a local connectivity probe found no net on it. That
    substrate is not claimed by `p_substrate_blocks`.
- The 78 `erc.floating_gate` findings in the analog report belong to the unrouted blocks and are not this item's subject.

### Item 11 spec coverage: layers in the stream without a declaration

`erc_coverage.layers_in_stream_without_declaration` is non-empty in both reports, so it is stated here (the item 11 text in
`manifests/design-evidence-tiers.md` requires it). Both reports have `provenance.deck: null`: no curated routing-stack deck was
used. The stackup is the hand-written one in each spec (`poly`, `li1`, `met1`-`met5`, `licon1`..`via4`), not a narrowed deck.
Layer names are from `sky130A.lyp` in the pinned PDK.

- **Digital (17):** `64/5` nwell.label, `64/16` nwell.pin, `64/59` pwell.label, `67/16` li1.pin, `68/16` met1.pin, `69/16` met2.pin,
  `72/16` met5.pin, `122/16` pwell.pin, `83/44` text.drawing, `235/4` prBoundary.boundary, `236/0` boundary, `81/4` areaid.standardc,
  `78/44` hvtp.drawing, `93/44` nsdm.drawing, `94/20` psdm.drawing, `95/20` npc.drawing, `65/20` diff.drawing.
- **Analog (13):** `64/18` dnwell.drawing, `64/20` nwell.drawing, `65/20` diff.drawing, `65/44` tap.drawing, `66/13` poly.res,
  `70/16` met3.pin, `71/16` met4.pin, `72/16` met5.pin, `75/20` hvi.drawing, `86/20` rpm.drawing, `93/44` nsdm.drawing,
  `94/20` psdm.drawing, `95/20` npc.drawing.

Why these are not supply-carrying, in the digital partition (the one graded met):

- `*.pin`, `*.label`, `text.drawing`: annotation shapes drawn over metal that is already in the stackup. They add no conductor.
  The rail names are read from the declared `label_layer`s (`67/5`, `68/5`, `69/5`, `72/5`).
- `prBoundary`, `boundary`, `areaid.standardc`: outline and marker layers.
- `hvtp`, `nsdm`, `psdm`, `npc`: implant and nitride-poly-contact masks. They set device type, not connectivity.
- `diff.drawing` (`65/20`) is the one real conductor on the list. It is not walked as a connectivity layer. Supply reaches
  it through `licon` contacts to `li1`, and the check evaluates islands at `li1` and above, where the rails are routed. A
  rail connection that exists only through diffusion would not be seen. I did not look for one, and the standard-cell rows
  take VCCD and VSS on `li1`/`met1`. The `tap.drawing` shapes (`65/44`) are declared as `tap_layer` in both digital ties.

No digital layer in the list carries routing, so the digital stackup needs no addition. This is a reading of layer purposes,
not a measurement: I did not check per layer whether it overlaps rail geometry.

For the analog partition (graded unmet), `64/20`, `65/44` and `64/18` are undeclared because the spec declares no `ties[]`,
so the well and tap layers are not modelled. That is part of why it is unmet. The remaining analog layers are
pin, resistor-marker, implant and `hvi` layers with the same purposes as above. `diff.drawing` is treated the same way as in
the digital partition.
