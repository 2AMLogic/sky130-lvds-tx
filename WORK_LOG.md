# Work Log

Chronological record of merged PRs and closed issues. Maintained by the Guide role.

### 2026-10-27

- **PR #36**: docs: sync manifests README verdict count and CI freshness list with signoff record
- **PR #35**: feat: generate pad-cell GDS with a grounded-gate ESD clamp (stage 1 of T1 item 2 analog)
- **PR #33**: feat: route serializer netlist with a VCCD power grid for T1 item 2
- **PR #28**: feat(design): analog schematics and derived netlists for T1 item 1
- **PR #29**: feat: add 8:1 serializer RTL, cocotb bench, netlist and item 1 digital attestation
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
