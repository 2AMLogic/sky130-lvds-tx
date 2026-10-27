# Serializer place-and-route — record

`serializer_synth.v` (see `RECORD.md`) placed and routed with `klt place-and-route`
(OpenROAD) on `sky130_fd_sc_hd`, with a power grid on the 1.8 V core rail.
T1 item 2 (Layout, digital); the `power` block below is what item 11 reads.

| Field | Value |
|---|---|
| Request / response | `pnr.request.json` / `pnr.response.json` |
| Input netlist | `serializer_synth.v`, sha256 `ef27a14ba381f0032c5add3d11b0cdbb7efd82a52f305cf9c7094b1dd841ac74` (matches `provenance.input.content_hash`) |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` |
| `klt` | `0.8.1.dev58+g78f36d8f316c` (host; the signoff record itself is rendered with the pinned `879d39ba`) |
| OpenROAD | `26Q3-1510-g6cb3f2b704` |
| P&R corner | `tt_025C_1v80` only (no corner sweep run); seed 1; clock 2.0 ns |
| Stage reached | `route`, status ok, `warnings: []` |

## Committed artifacts

| File | sha256 |
|---|---|
| `serializer_routed.gds` | `6a1239459c67b47fa001177b6be4d3f66abc7fb8e42f0e743fd5a0ee796cb8ff` |
| `serializer_routed.v` (as-built, post-CTS) | `92910f5010efb7a660a0fae5576f6650ebb8960941d6f278df57cc6c4c6dc711` |
| `serializer_routed.def` | `0025f8604158ef685716893fb12110352830e2d18eeeb9f5c17fa96f6a0b2d07` |
| `serializer_routed.spef` | `7ff0df6e4f6758effc542150ede0b317ed961e76b56af8df80f7fd08db55d2b7` |

The paths inside `pnr.response.json` (`gds_path`, `def_path`, `verilog_path`,
`spef_sta.spef_path`) name klt's scratch directory `flow/serializer/.klt/place-and-route/`,
which is not committed; the files above are copies of those outputs. The
response is otherwise verbatim. Tracked at 2AMLogic/klayout-tools#4231.

## Results

- Die 2141.38 µm², core 1707.89 µm², **39.12 % utilization achieved** (35 %
  requested); wirelength 1222 µm.
- **Router-internal** counts (not the item 3 signoff DRC, and metal density is
  explicitly not evaluated, see `coverage` in the response): 0 route DRC
  violations (detailed route converged 2 → 1 → 0), 0 antenna violations.
- Timing at `tt_025C_1v80`, 2.0 ns clock: worst setup slack +0.854 ns, worst
  hold slack +0.437 ns. After post-route SPEF back-annotation
  (`post_route_spef`, 71/71 design nets annotated): worst setup slack
  +0.818 ns, 0 setup and 0 hold violations.
- Power block (`pnr.response.json` → `power`, quoted for item 11): `pdn: true`,
  `global_connect: true`, `power_net: VCCD`, `ground_net: VSS`,
  `tapcell_master: sky130_fd_sc_hd__tapvpwrvgnd_1` (25 tapcells, distance 14 µm),
  straps on met1/met4/met5, `placed.status: "complete"` (273 components,
  188 fillers). `VCCD` was accepted and global-connected as the rail name
  with no rename needed.

## What this does not show

- **Spec S3 is not claimed.** The slack above is at the `tt_025C_1v80`
  P&R corner, not the `ss_100C_1v60` reference corner with 10 % clock
  uncertainty. Closing S3 needs STA at that corner (see `RECORD.md`).
- DRC (#24), LVS (#25) and the supply `klt erc` spec (#26) of this GDS are
  separate items; none is claimed here.
- Not integrated with the analog pad slot or any top-level floorplan.

## Reproducibility

Two consecutive runs of the request gave a byte-identical GDS, routed
verilog, DEF and SPEF (the response differs only in per-run `invocation_id`s
and log directories). `klt place-and-route --check flow/serializer/pnr.response.json
flow/serializer/pnr.request.json` (and with `--rerun`) reports `match`.
`verification/signoff/check-serializer-pnr.sh` runs the `--rerun` check and
byte-compares a fresh GDS to the committed one; it is `local_only` (needs
OpenROAD and the PDK), so CI re-verifies the committed file's hash but does not
re-route. The item 2 envelope
(`verification/signoff/evidence/item-2-layout-digital.json`) is hand-written:
`klt signoff --attest` has no producer for item 2 (2AMLogic/klayout-tools#4188).

```console
export PDK_ROOT=<pinned root> PDK=sky130A
klt place-and-route flow/serializer/pnr.request.json --format json
sh verification/signoff/check-serializer-pnr.sh
```

`PDK=sky130A` is needed here because klt otherwise resolves the first variant
under `PDK_ROOT`, which on this host is not a sky130 one.
