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
