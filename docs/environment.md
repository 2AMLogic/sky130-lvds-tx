# Environment

One command provisions the pinned verification environment from a fresh
clone:

```
./scripts/setup-env.sh [--pdk-root=/path]    # PDK_ROOT defaults to ~/.ciel
source .venv/bin/activate                    # pinned klt and Yosys lead $PATH
```

It creates `.venv/`, installs the pinned `klt` and Yosys, installs the pinned
sky130A PDK with `sky130_fd_pr`, `sky130_fd_io` and `sky130_fd_sc_hd`, and
exits non-zero if the installed tree's `SOURCES` does not name the pinned
open_pdks revision or one of the three libraries is absent. Negative control:
`SETUP_ENV_EXPECTED_OPEN_PDKS_REV=000… ./scripts/setup-env.sh` exits 1.

The script is vendored from `2AMLogic/sky130-modexp@18f4d8f`; see
`reuse.lock.json` and `spec/decisions/0002-vendored-setup-env-edits.md`.
`iverilog` and `openroad` are host tools: the script reports them if missing
and does not install them.

## Pinned versions

| Constant | Value |
|---|---|
| `KLT_VERSION` | `0.8.0` |
| `CIEL_VERSION` | `2.6.1` |
| `CIEL_SKY130_VERSION` | `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` |
| `CIEL_LIBRARIES` | `sky130_fd_pr sky130_fd_io sky130_fd_sc_hd` |
| `YOWASP_YOSYS_VERSION` | `0.68.0.0.post1208` |
| `YOWASP_YOSYS_WASM_SHA256` | `e37a7e65e3fa4efbbd64a9c1b0e906be16cdc6c4d5273109d17537f78449f38c` |

## Notes

- The venv's `klt` is `0.8.0` (PyPI). `KLT_SIM_BACKEND` is read from 0.7.0 on, so
  this client honours the host's batch default; no sim was run against the
  venv's `klt` for this bump. The PDK smoke sim was run with the host `klt`
  (`sim/pdk-smoke/RECORD.md`).
- A batch worker's image carries its own sky130A (`open_pdks c6d73a35…`,
  not this pin). A `klt sim` request that must run on the pinned models sets
  `options.stage_model_inputs: true` so the pinned library ships with the job.
