# Environment

One command provisions the pinned verification environment from a fresh
clone:

```
./scripts/setup-env.sh [--pdk-root=/path]    # PDK_ROOT defaults to ~/.ciel
source .venv/bin/activate                    # pinned klt and Yosys lead $PATH
```

It creates **two** repo-local venvs, `.venv/` and `.venv-pnr/` (see
"Two venvs" below), installs the pinned `klt` into both, installs the
pinned Yosys into `.venv`, installs the pinned sky130A PDK with
`sky130_fd_pr`, `sky130_fd_io` and `sky130_fd_sc_hd`, and exits non-zero if
the installed tree's `SOURCES` does not name the pinned open_pdks revision
or one of the three libraries is absent. Negative control:
`SETUP_ENV_EXPECTED_OPEN_PDKS_REV=000… ./scripts/setup-env.sh` exits 1.

The script is vendored from `2AMLogic/sky130-modexp@18f4d8f`; see
`reuse.lock.json` and `spec/decisions/0002-vendored-setup-env-edits.md`.
`iverilog` and `openroad` are host tools: the script reports them if missing
and does not install them.

## Cold-start check

Item 9's third-party cold start (digital serializer bench with negative control, then the
analog smoke through `klt sim`; needs `uv`, `iverilog` and the PDK above):

```
sh verification/signoff/cold-start.sh
```

Inventory: `verification/signoff/item-9-inventory.json`.

## Pinned versions

| Constant | Value |
|---|---|
| `KLT_VERSION` | `0.9.1` (both venvs) |
| `KLAYOUT_VERSION` | `0.28.17.post1` (`.venv`, attest/CI) |
| `PNR_KLAYOUT_VERSION` | `0.30.13` (`.venv-pnr`, P&R) |
| `CIEL_VERSION` | `2.6.1` |
| `CIEL_SKY130_VERSION` | `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` |
| `CIEL_LIBRARIES` | `sky130_fd_pr sky130_fd_io sky130_fd_sc_hd` |
| `YOWASP_YOSYS_VERSION` | `0.68.0.0.post1208` |
| `YOWASP_YOSYS_WASM_SHA256` | `e37a7e65e3fa4efbbd64a9c1b0e906be16cdc6c4d5273109d17537f78449f38c` |

## Two venvs

`scripts/setup-env.sh` provisions two venvs
(`spec/decisions/0005-split-pnr-venv-pin.md`):

- **`.venv`** — the attest/CI pair: `klayout==0.28.17.post1` first, then
  `klayout-tools==0.9.1` with `--no-deps` (deliberately violating klt's own
  `klayout>=0.30` floor, issue #104), plus the pinned Yosys. Use it for
  `klt signoff --attest`, evidence regeneration and CI parity.
- **`.venv-pnr`** — the place-and-route pair: `klayout==0.30.13` (pinned
  exactly, `PNR_KLAYOUT_VERSION`) with `klayout-tools==0.9.1` installed
  normally (no `--no-deps`), so klt's `klayout>=0.30` floor is satisfied.
  Use it **for `klt place-and-route` only** — it is the only provisioned
  environment in which P&R runs at all (`Layout.read_bytes` is
  0.30.x-only; upstream `2AMLogic/klayout-tools#5768`).

```
source .venv-pnr/bin/activate
klt place-and-route flow/serializer/pnr.request.json --format json
```

`verification/signoff/check-serializer-pnr.sh` invokes bare `klt` from
`$PATH` — no venv path is hardcoded into the gate — so activating
`.venv-pnr` is what selects the P&R toolchain for it. The PDK is consumed
through `PDK_ROOT`, which is venv-independent.

**Reversal condition**: the split collapses to one venv when
`2AMLogic/klayout-tools#5768` lands.

## Notes

- The venv's `klt` is `0.9.1` (PyPI), installed `--no-deps` so the venv can
  carry `klayout==0.28.17.post1` next to it: klt declares `klayout>=0.30`, but
  the older module is what serialises the committed driver-pad GDS to its
  attested bytes (a 0.30.x module re-encodes two TEXT `MAG` records in the
  stock pad-frame cell; issue #104). klt's envelope output does not depend on
  the module version. `KLT_SIM_BACKEND` is read from 0.7.0 on, so this client
  honours the host's batch default; no sim was run against the venv's `klt`
  for this bump. The PDK smoke sim was run with the host `klt`
  (`sim/pdk-smoke/RECORD.md`).
- A batch worker's image carries its own sky130A (`open_pdks c6d73a35…`,
  not this pin). A `klt sim` request that must run on the pinned models sets
  `options.stage_model_inputs: true` so the pinned library ships with the job.
