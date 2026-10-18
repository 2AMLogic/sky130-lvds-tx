# 0001 — Verification runner is kept separate from gf180-tmds-tx's

**Status**: accepted (harness decision; no change to the ratified spec)

## Decision

The cocotb/Icarus runner in `verification/smoke/runner.py` is written here,
not vendored from `2AMLogic/gf180-tmds-tx`. Mechanics are adopted by
convention: same bench layout, same `cocotb==2.0.1` pin, same rule that the
negative control runs the unmodified test module and must fail.

## Evidence

Read at `gf180-tmds-tx` @ `9a55961ab5e4608d42ffefb70308adcb4b42213e`:
`verification/tmds_serializer/runner.py`.

## Reasons

- The sibling runner is design-specific (hardcoded `rtl/` paths, toplevel,
  test module, `SEL_MODES`, a `tmds_tx_chain.v` wrapper). The reusable part
  is about 30 lines and there is no `verification/common/` to stamp.
- This harness must write a machine-readable result (per-test pass/fail,
  seed, tool versions, commit); the sibling only prints. Vendoring would mean
  a diverged copy from day one.

## Rejected

- Vendoring the runner as-is: carries TMDS names and is modified anyway.
- Running both Verilator and Yosys lint: Verilator alone is on the host and
  in Ubuntu apt.

The serializer itself is a separate reuse decision (issue #2).
