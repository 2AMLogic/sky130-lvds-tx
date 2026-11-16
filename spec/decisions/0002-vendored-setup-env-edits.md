# 0002 — Local edits to the vendored `scripts/setup-env.sh`

Status: accepted (toolchain bring-up; decides nothing the spec decides).

## Context

`scripts/setup-env.sh` is vendored from `2AMLogic/sky130-modexp` at
`18f4d8fd5e104f64550817a5468f262c159f734f` (`reuse.lock.json`, `mode:
vendored`). `sha256` in the lock is the upstream file; `local_sha256` is the
file as committed here. They differ because of the edits below, which this
record exists to justify. `scripts/check_reuse_lock.py` re-hashes every
`local_sha256` and checks every `diverged:` pointer in CI, so the lock and
this record can no longer drift from the committed file silently.

The version pins are NOT unchanged from upstream except klayout-tools.
Upstream pins klt as a git revision (`KLT_REPO`/`KLT_REV`); this copy
replaces that with PyPI pins of its own and carries module pins upstream
does not have (edits 6–7, 9):

- `klayout-tools==0.9.1` (`KLT_VERSION`, both venvs; upstream: git revision)
- `klayout==0.28.17.post1` in the main venv (`KLAYOUT_VERSION`; no upstream
  counterpart)
- `klayout==0.30.13` in the P&R venv (`PNR_KLAYOUT_VERSION`; edit 9)
- ciel `2.6.1`, open_pdks
  `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7`, YoWASP Yosys
  `0.68.0.0.post1208` (wasm sha256 in the script) — unchanged from upstream.

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
   asking for a system package. Post-#140 this logic lives in a
   `create_venv` helper shared by both venvs (edit 9).
4. **No Docker OpenROAD route.** The upstream fallback symlinks
   `scripts/openroad-docker.sh`, which is not vendored. A missing `openroad`
   is reported, not installed.
5. **Dropped references** to upstream-only files (`verification/check_pins.py`,
   `verification/cross_check.py`, `npm run` targets). The pin table
   is `docs/environment.md`; no checker for it exists in this repo yet.
   Help text is re-sliced for the local header, and the usage line uses the
   `--pdk-root=` form.
6. **klt pinned to the PyPI release.** `KLT_REPO`/`KLT_REV` (a git commit) are
   replaced by `KLT_VERSION="0.9.1"` and
   `pip install --no-deps "klayout-tools==${KLT_VERSION}"`: a git build
   reports a dev version that fails an `==` check (klayout-tools#2823). It
   installs `--no-deps` for the reason edit 7 records.
7. **klayout module pinned for byte-reproducible GDS.**
   `KLAYOUT_VERSION="0.28.17.post1"` has no upstream counterpart: the
   `klayout` module, not `klt`, serialises the generated layout bytes, and a
   0.30.x module re-encodes two TEXT `MAG` records in the stock pad-frame
   cell, so the committed GDS would stop regenerating byte-identically
   (issue #104). klt declares `klayout>=0.30`, which this pin violates on
   purpose, so klt is installed `--no-deps` on top of the older module and
   its one other runtime dependency (`jsonschema>=4.0`) is installed
   explicitly; an installed-klayout version echo is added. klt's envelope
   output does not depend on the module version (verified under 0.28.17 and
   0.30.13, issue #104).
8. **Python interpreter ceiling lowered to 3.12.** The pinned klayout wheel
   ships CPython 3.10–3.12 wheels only (no cp313; on 3.13+ pip would build
   klayout's C++ sdist), so the candidate list drops `python3.13` and the
   ceiling check and FATAL guidance are rewritten; upstream accepts
   `<= 3.13` (cocotb alone). A consequence of edit 7.
9. **Split P&R venv.** A second venv `.venv-pnr` (`PNR_VENV_DIR`) is created
   beside the main one via the shared `create_venv` helper and provisioned
   as its own fifth step: `klayout-tools==${KLT_VERSION}` installed with
   dependencies satisfied on `klayout==${PNR_KLAYOUT_VERSION}` (0.30.13
   meets klt's `klayout>=0.30` floor, so no `--no-deps` there — the place
   a 0.30.x module is wanted). The `PNR_*` prefix is load-bearing:
   `check-driver-pad-gds.sh` parses the constants. Decided in
   `spec/decisions/0005-split-pnr-venv-pin.md`.

## Consequences

Re-vendoring from upstream means re-applying these nine edits. Edit 1 is
the only one this repo cannot do without. This list was re-derived from a
full `diff -u` of upstream at the pinned commit against the committed file;
a re-vendor must re-derive it the same way, not carry it forward by hand.
