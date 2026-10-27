# verification

Cold-start digital verification harness: cocotb + Icarus Verilog, PDK-free.

## Layout

    verification/
      lint_rtl.sh                 Verilator lint of rtl/*.v (vacuous while rtl/ is empty)
      smoke/                      placeholder bench proving the harness itself
        smoke.v  test_smoke.py  runner.py  requirements.txt
        negative_control/smoke_broken.v

Later benches follow `verification/<bench>/{runner.py,requirements.txt,test_<bench>.py,negative_control/}`
and call `run_bench()` from `smoke/runner.py` rather than copying it.

## Cold start

    pip install -r verification/smoke/requirements.txt
    python3 verification/smoke/runner.py     # works from any directory
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

`results/smoke.json` (gitignored; `--out` to change): per-test pass/fail for
both legs, cocotb seed (`COCOTB_RANDOM_SEED` overrides), python/cocotb/iverilog
versions, `git rev-parse HEAD`, and `overall`.

Reuse decision for the sibling's runner: `spec/decisions/0001-verification-runner-kept-separate.md`.

## Item 3 DRC

T1 checklist item 3, one `klt drc` report per partition, committed under
`verification/signoff/evidence/` and cited from `manifests/sky130-lvds-tx.json`.
Deck `sky130` (content hash `sha256:072b456a6c867ff7244bfc287908a960c265628b3c26a64db5506c4bb124d267`,
`released: false`), PDK `sky130A` at open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7`, klt `0.8.1.dev181+g70d73835514c`.

    export PDK_ROOT=~/.ciel PDK=sky130A
    klt drc --deck sky130 --pdk-root "$PDK_ROOT" --top sky130_lvds_tx_driver_pad --format json \
        layout/sky130_lvds_tx_driver_pad.gds > verification/signoff/evidence/item-3-drc-analog-r2.json
    klt drc --deck sky130 --pdk-root "$PDK_ROOT" --format json \
        flow/serializer/serializer_routed.gds > verification/signoff/evidence/item-3-drc-digital.json
    klt drc --check verification/signoff/evidence/item-3-drc-analog-r2.json --pdk-root "$PDK_ROOT"
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
analog layout is placement-only and unrouted (`layout/README.md`). Issue #44 traced them: they reproduce
on the unmodified PDK cells, the foundry's own deck flags the same met4/met5 width, spacing,
enclosure and area rules, and the met5 ones are cell-edge stripes that close when cells abut.
The classification, and what stays unestablished (`met4.holes_area.1`, `met5.area.1`, and whether
the foundry waives the I/O library), is in
[`layout/README.md`](../layout/README.md#drc-of-the-stock-pad-frame-issue-44). The earlier report
`item-3-drc-analog.json` is kept (append-only); the manifest now cites `item-3-drc-analog-r2.json`,
the same GDS and deck re-run with the CI-pinned klt (`0.8.1.dev55+g879d39bad82b`), same 486.

**Coverage, quoted verbatim from each report's `coverage` block** (quote the committed report,
not this copy, if they differ):

- `deck_scope` (both): `["cap2m", "capm", "ct", "difftap", "li", "licon", "m1", "m2", "m3", "m4", "m5", "npc", "nsdm", "nwell", "poly", "psdm", "rpm", "urpm", "via", "via2", "via3", "via4", "x"]`
- `layers_in_stream_without_rules`, analog: `["66/13", "70/5", "70/16", "71/5", "71/16", "72/5", "72/16"]`
- `layers_in_stream_without_rules`, digital: `["64/5", "64/16", "64/59", "67/5", "67/16", "68/5", "68/16", "69/5", "69/16", "72/5", "72/16", "81/4", "83/44", "122/16", "235/4", "236/0"]`
- `rules_skipped`, analog (48): `areaid_re.ongrid.1`, `capm.*`/`capm2.*` (9), `hvntm`, `hvtp`, `hvtr`, `lvtn`, `mf`, `ncm`, `nsm`, `pad`, `pwbm`, `pwde`, `pwell_rs`, `tunm`, `uhvi`, `vhvi`, `vpp` `.angle.1`/`.ongrid.1`, `urpm.width.1`, `met3.enclosing.capm.1`, `met4.enclosing.capm2.1`, `met4.enclosing.via4.1`, `met5.enclosing.via4.1`, `via4.angle.1`, `via4.ongrid.1`, `via4.space.1`, `via4.width.1`. Full list in the report.
- `rules_skipped`, digital (48): the analog list without `hvtp.*`, `met4.enclosing.via4.1`, `met5.enclosing.via4.1` and the four `via4.*` rules, plus `dnwell.angle.1`, `dnwell.ongrid.1`, `hvi.angle.1`, `hvi.ongrid.1`, `nwell.enclosed.hvi.1`, `rpm.angle.1`, `rpm.ongrid.1`, `rpm.width.1`. Full list in the report.
- Skipped rules are `inapplicable` / `no_applicable_geometry` in the report, and `unmodeled_rules` lists DRM rules the curated deck does not transcribe at all.
- Analog `voltage_domain_warnings`: the `hvi` (75/20) thick-oxide marker is modelled only for device recognition and `nwell.enclosed.hvi.1`; geometry drawn inside it is checked at general-case thresholds, not the medium-voltage ones (`difftap.14` etc.). Pad/ESD and 5 V device layers are therefore **not** fully covered by this deck.

## T1 item 4: LVS (`klt lvs`), recorded `mismatch`

Two probe runs, one per partition, `engine: klayout` with the curated `sky130`
deck. Requests: `verification/signoff/lvs/item-4-{analog,digital}.request.json`;
reports: `verification/signoff/evidence/item-4-lvs-{analog,digital}.json`.
**Neither partition meets item 4**, so the manifest still grades it `unmet`.
The `r2` analog reports are append-only additions; the first report is kept.

| Partition | `status` | `power_connectivity.status` | Why |
|---|---|---|---|
| Analog (`sky130_lvds_tx_driver` vs `design/driver/driver.spice`) | `mismatch` | `unchecked` (not applicable to `subckt-call`) | `item-4-lvs-analog.json` (placement-only layout): 309 devices and 500 nets extracted against 11 and 29, 0 matched. Re-run as `item-4-lvs-analog-r2.json` after routing (#48), with `flatten_*`, `combine_devices` and `compare_mos_flavour`: 89/89 devices, 50/50 nets, 81 and 37 matched; the 8 unmatched are the `SCALE=11` slice, whose `m={SCALE}` the converter does not evaluate (klayout-tools#4406). With the scale substituted into a derived netlist (`item-4-lvs-analog-r2-scale-expanded.json`) the same layout is `match` (89/89, 50/50, 18/18 pins). |
| Digital (`serializer_routed.gds` vs `serializer_routed.v`, `gate-level-verilog`) | `match` | `mismatch` | Signal compare matches (174 nets, 118 pins). One finding, `power.inconsistent_pin_net`: `VNB` reaches `VSS` (246 instances), `VCCD` (1) and `word_clk` (1). Not diagnosed here. |

Warnings only, digital: `topology` x3 (empty `nfet`/`pfet`/`pnp` classes, not real),
`topology.power_only_pruned`, `topology.reference_port_alias_joined` x3
(`word_clk`, `dout[0]`, `dout[1]`), `topology.top_level_pins_anchored`.
Analog: `device.body_unverified` (122 NMOS, 185 PMOS: no named tap nets),
`device.geometry_not_compared` and `device.placeholder_value` (`res_high_po`).

The deck does distinguish `g5v0d10v5` from `01v8` (`compare_mos_flavour`: a
swapped reference card gives `device.class`). Pad/ESD devices (the clamp, `D1`,
the pad frame) are outside the driver top and remain not established. The
analog request is a probe: its `r2` report is `mismatch` only because of the
converter gap above, and the manifest still grades item 4 `unmet`.

Digital needs `layout.abstract_cells` (`sky130_fd_sc_hd__*`) plus the library LEF;
without it the routed GDS extracts 719 flat transistors against a 0-device
reference. Re-run with:

    export PDK_ROOT=~/.ciel PDK=sky130A
    klt lvs --format json verification/signoff/lvs/item-4-digital.request.json
    klt lvs --check verification/signoff/evidence/item-4-lvs-digital.json   # drift check

The digital request names the LEF by absolute path; edit it for your `PDK_ROOT`.
