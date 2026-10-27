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

## T1 item 4: LVS (`klt lvs`), recorded `mismatch`

Two probe runs, one per partition, `engine: klayout` with the curated `sky130`
deck. Requests: `verification/signoff/lvs/item-4-{analog,digital}.request.json`;
reports: `verification/signoff/evidence/item-4-lvs-{analog,digital}.json`.
**Neither partition meets item 4**, so the manifest still grades it `unmet`.

| Partition | `status` | `power_connectivity.status` | Why |
|---|---|---|---|
| Analog (`sky130_lvds_tx_driver` vs `design/driver/driver.spice`) | `mismatch` | `unchecked` (not applicable to `subckt-call`) | The layout is placement-only and unrouted (`layout/README.md`): 309 devices and 500 nets extracted against 11 and 29 in the reference, 0 matched. Needs the routing deferred in #22. |
| Digital (`serializer_routed.gds` vs `serializer_routed.v`, `gate-level-verilog`) | `match` | `mismatch` | Signal compare matches (174 nets, 118 pins). One finding, `power.inconsistent_pin_net`: `VNB` reaches `VSS` (246 instances), `VCCD` (1) and `word_clk` (1). Not diagnosed here. |

Warnings only, digital: `topology` x3 (empty `nfet`/`pfet`/`pnp` classes, not real),
`topology.power_only_pruned`, `topology.reference_port_alias_joined` x3
(`word_clk`, `dout[0]`, `dout[1]`), `topology.top_level_pins_anchored`.
Analog: `device.body_unverified` (122 NMOS, 185 PMOS: no named tap nets),
`device.geometry_not_compared` and `device.placeholder_value` (`res_high_po`).

Not established: whether the deck recognises the `g5v0d10v5` and pad/ESD
devices. The analog compare fails on topology before that matters, and the
driver's thick-oxide devices are drawn as `hvi`-flavoured `mos_array` cells, not
`nfet_g5v0d10v5`. Re-check once the driver is routed.

Digital needs `layout.abstract_cells` (`sky130_fd_sc_hd__*`) plus the library LEF;
without it the routed GDS extracts 719 flat transistors against a 0-device
reference. Re-run with:

    export PDK_ROOT=~/.ciel PDK=sky130A
    klt lvs --format json verification/signoff/lvs/item-4-digital.request.json
    klt lvs --check verification/signoff/evidence/item-4-lvs-digital.json   # drift check

The digital request names the LEF by absolute path; edit it for your `PDK_ROOT`.
