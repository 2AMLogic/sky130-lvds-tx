# 0002 — Local edits to the vendored `scripts/setup-env.sh`

Status: accepted (toolchain bring-up; decides nothing the spec decides).

## Context

`scripts/setup-env.sh` is vendored from `2AMLogic/sky130-modexp` at
`18f4d8fd5e104f64550817a5468f262c159f734f` (`reuse.lock.json`, `mode:
vendored`). `sha256` in the lock is the upstream file; `local_sha256` is the
file as committed here. They differ because of the edits below, which this
record exists to justify.

The version pins themselves are unchanged: `klayout-tools`
`dac2b5daceb69a2068d9d2ee190d7afe37b29af7`, ciel `2.6.1`, open_pdks
`f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7`, YoWASP Yosys
`0.68.0.0.post1208` (wasm sha256 in the script).

## Edits

1. **Libraries.** Upstream enables only `sky130_fd_pr`. This block needs the
   I/O library (`sky130_fd_io`, the pad path) and the standard cells
   (`sky130_fd_sc_hd`, the serializer), so `ciel enable` gets one `-l` per
   library (`CIEL_LIBRARIES`), and the script fails if any of the three is
   missing under `libs.ref/` after the install.
2. **Negative control.** `SETUP_ENV_EXPECTED_OPEN_PDKS_REV` overrides the
   revision the installed `SOURCES` file is checked against (default: the
   pin). A wrong value makes the script exit 1; it is a test hook, not a way
   to re-pin.
3. **venv fallback.** If `python3 -m venv` fails (no `ensurepip`, as on a
   host without `python3-venv`), create the venv with `uv venv` instead of
   asking for a system package.
4. **No Docker OpenROAD route.** The upstream fallback symlinks
   `scripts/openroad-docker.sh`, which is not vendored. A missing `openroad`
   is reported, not installed.
5. **Dropped references** to upstream-only files (`verification/check_pins.py`,
   `verification/cross_check.py`, `npm run` targets). The pin table
   is `docs/environment.md`; no checker for it exists in this repo yet.

## Consequences

Re-vendoring from upstream means re-applying these five edits. Edit 1 is
the only one this repo cannot do without.
