# Work Log

Chronological record of merged PRs and closed issues. Maintained by the Guide role.

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
