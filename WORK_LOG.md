# Work Log

Chronological record of merged PRs and closed issues. Maintained by the Guide role.

### 2026-10-31

- **PR #67**: chore(verification): drop dead main() from shared run_bench() host
- **Issue #66** (closed): Trim dead main() and stale docstring from verification/smoke/runner.py
- **PR #64**: chore(verification): retire smoke placeholder bench, cold start runs serializer bench
- **Issue #30** (closed): Retire placeholder smoke bench and point pnpm test at the serializer bench
- **PR #61**: build: run serializer bench from pnpm test and drop duplicate check:all

### 2026-10-29

- **PR #32**: feat(signoff): attest T1 item 9 with a cold-start wrapper and pinned inventory
- **Issue #27** (closed): T1 item 9 (testbenches shipped): item 9 inventories and attestations for both partitions

### 2026-10-28

- **PR #59**: chore: re-run analog DRC on the routed GDS and cite it as 3.analog (r3)
- **Issue #58** (closed): T1 item 3 (DRC clean, analog): re-run klt drc on the routed driver/pad GDS — the cited report is bound to the pre-#48 stream
- **PR #57**: chore: retire superseded flow/pdk-smoke stand-in counter flow
- **Issue #39** (closed): Remove flow/pdk-smoke: superseded stand-in counter flow
- **Issue #24** (closed): T1 item 3 (DRC clean): klt drc on the driver/pad and serializer layouts with coverage disclosed

### 2026-10-27

- **PR #55**: build: pin klayout-tools to the 0.8.0 PyPI release
- **Issue #54** (closed): Bump klayout-tools pin dac2b5daceb6 → 0.8.0
- **PR #51**: feat: route the analog driver from its netlist so LVS compares topology
- **PR #50**: docs: diagnose VNB power finding as abstract-extraction tool gap
- **Issue #48** (closed): T1 item 4 prerequisite (analog): route the driver/pad layout so LVS compares topology
- **PR #43**: docs: record probe klt lvs reports for analog and digital partitions
- **PR #46**: docs: classify stock pad frame met4/met5 DRC findings and re-cite item 3 analog
- **PR #45**: feat: record klt drc reports per partition and cite them for T1 item 3
- **Issue #44** (closed): Analog pad frame reports 486 met4/met5 DRC violations under klt drc sky130 deck
- **PR #41**: feat: place ddr_mux and predriver in the layout generator and attest item 2 analog
- **PR #38**: feat: place driver, drv_sel and drv_slice devices in the layout generator
- **PR #36**: docs: sync manifests README verdict count and CI freshness list with signoff record
- **PR #35**: feat: generate pad-cell GDS with a grounded-gate ESD clamp (stage 1 of T1 item 2 analog)
- **PR #33**: feat: route serializer netlist with a VCCD power grid for T1 item 2
- **PR #28**: feat(design): analog schematics and derived netlists for T1 item 1
- **PR #29**: feat: add 8:1 serializer RTL, cocotb bench, netlist and item 1 digital attestation
- **Issue #22** (closed): T1 item 2 (layout, analog): driver and pad-cell layout in the 75 µm analog pad slot
- **Issue #34** (closed): manifests/README.md 'Current verdict' still says 4 of 22 items met after item 2 (digital) landed
- **Issue #23** (closed): T1 item 2 (layout, digital): place-and-route the serializer to a committed routed GDS with a PDN
- **Issue #20** (closed): T1 item 1 (design sources, analog): schematics and derived netlists for the DDR mux, predriver, current-steering driver and pad cell
- **Issue #21** (closed): T1 item 1 (design sources, digital): serializer RTL (8:1→2:1 reduction, ÷4 word counter) and its synthesized netlist

### 2026-10-24

- **PR #8**: ci: add T1 signoff manifest, item 10 attestation and freshness workflow
- **Issue #5** (closed): Signoff scaffolding: block manifest, committed klt signoff record, and CI (T1 item 10)

### 2026-10-21

- **PR #15**: Bump Repo Skills 0.24.3 -> 0.24.7
- **PR #14**: build: wire pnpm lint/test/check scripts to RTL lint and smoke bench
- **Issue #13** (closed): Wire package.json check:ci/check:all/test/lint to the real verification checks (currently vacuous exit-0 stubs)

### 2026-10-20

- **PR #9**: docs(spec): propose LVDS transmitter target spec and decision records
- **Issue #2** (closed): Draft and ratify the target spec

### 2026-10-17

- **PR #10**: feat: pin sky130 environment and commit analog and digital PDK smoke runs
- **PR #7**: feat(verification): cocotb/Icarus smoke harness with negative control, lint and CI
- **PR #1**: chore(loom): Install Loom 0.19.1180
- **Issue #4** (closed): Test harness skeleton: adopt-or-record gf180-tmds-tx's cocotb runner and negative-control pattern, plus RTL lint and CI (T1 item 9)
- **Issue #3** (closed): Pin the sky130 environment (adopt sky130-modexp's setup, include sky130_fd_io) and commit analog and digital smoke runs
