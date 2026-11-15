# Serializer place-and-route — record

`serializer_synth.v` (see `RECORD.md`) placed and routed with `klt place-and-route`
(OpenROAD) on `sky130_fd_sc_hd`, with a power grid on the 1.8 V core rail.
T1 item 2 (Layout, digital); the `power` block below is what item 11 reads.

## What changed for issue #98, and why

The previous revision of this record routed at `tt_025C_1v80` with the nominal
2.0 ns clock, and post-route STA failed setup at every `ss` corner (`STA.md`,
S3 NOT MET). Two things changed here; both are **implementation choices, not
spec changes**:

1. **Repair is aimed at the slow corner.** klt's `place-and-route` runs
   `repair_design`/`repair_timing` only against the single deck named by
   `pdk.corner` — the sweep corners are reported afterwards and never feed
   back into repair. `pdk.corner` moved `tt_025C_1v80` → `ss_n40C_1v60` (the
   binding in-spec corner), and `pdk.sweep_corners` widened to
   `ss_100C_1v60`, `ss_n40C_1v60`, `ss_n40C_1v76`, `tt_025C_1v80`,
   `ff_n40C_1v95` so the response reports the corners that matter without a
   separate STA round-trip.
2. **The implementation clock is tightened to 1.6 ns.** klt has no
   clock-uncertainty surface, so the 1.8 ns effective budget that `klt sta`
   judges (2.0 ns − 10 %) cannot be given to repair directly; period
   substitution is the only lever. 1.6 ns is *tighter* than that budget on
   purpose: at 1.8 ns, repair converged against the placement-stage parasitic
   estimate (which reads ~155 ns×10⁻³ optimistic relative to the routed SPEF)
   and the routed result still missed by 23 ps at `ss_n40C_1v60`. At 1.6 ns,
   repair upsizes past the estimate and the routed netlist clears the real
   1.8 ns budget with +0.093 ns at the binding corner (`STA.md`). **This
   substitution is for implementation only** — the STA record keeps the real
   2.0 ns period with `clock_uncertainty_ns.setup_ns: 0.2` and no period
   substitution, which is what makes it S3 evidence.

No RTL or synthesis-request change was needed *for P&R*: the RTL restructure
(registering the load/capture enables) is recorded in `RECORD.md` and was
already in place when this P&R request was edited.

## Run

| Field | Value |
|---|---|
| Request / response | `pnr.request.json` / `pnr.response.json` |
| Input netlist | `serializer_synth.v`, sha256 `a353a87bcfe3b3ec4586c1488685c609b1ac2dd6ec545e8944158671b10fdccd` (matches `provenance.input.content_hash`) |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (`PDK_ROOT` resolved to the pinned revision; see `provenance.pdk` and `layer_map` in the response) |
| `klt` | `0.9.2.dev1029+g76f47afa48f1` (host) |
| OpenROAD | `26Q3-1510-g6cb3f2b704` |
| P&R corner | `ss_n40C_1v60`, sweep `ss_100C_1v60` / `ss_n40C_1v60` / `ss_n40C_1v76` / `tt_025C_1v80` / `ff_n40C_1v95`; seed 1; clock 1.6 ns |
| Stage reached | `route`, status ok, `warnings: []` |

## Results

- Die 2297.76 µm², core 1764.19 µm², **42.91 % utilization achieved** (35 %
  requested); wirelength 1289 µm.
- **Router-internal** counts (not the item 3 signoff DRC, and metal density is
  explicitly not evaluated, see `coverage` in the response): 0 route DRC
  violations, 0 antenna violations; `min_area_repair`: clean, 0 patches.
- Timing at the P&R corner (`ss_n40C_1v60`, 1.6 ns implementation clock, no
  uncertainty): worst setup slack −0.080 ns, worst hold slack +0.850 ns — the
  negative setup slack is against the deliberately tighter implementation
  target, not the spec budget (see above). After post-route SPEF
  back-annotation (`post_route_spef`, 91/91 design nets annotated) at the same
  1.6 ns: −0.107 ns setup, 0 hold violations. Judged at the real 2.0 ns /
  0.2 ns-uncertainty budget in `STA.md`, the same netlist passes the three
  in-spec `ss` corners.
- Power block (`pnr.response.json` → `power`, quoted for item 11): `pdn: true`,
  `global_connect: true`, `power_net: VCCD`, `ground_net: VSS`,
  `tapcell_master: sky130_fd_sc_hd__tapvpwrvgnd_1` (25 tapcells, distance 14 µm),
  straps on met1/met4/met5, `placed.status: "complete"` (300 components,
  195 fillers). `VCCD` was accepted and global-connected as the rail name
  with no rename needed.

## What this does not show

- **Spec S3 is claimed by `STA.md`, not here.** The slack above is at the P&R
  implementation corner and clock, neither of which is the S3 budget. Post-route
  STA at every Liberty corner with 10 % uncertainty is in `STA.md`: setup now
  passes at every corner inside the spec's supply range, and the S3 verdict
  stays NOT MET only because the sub-1.62 V `ss` libraries still fail (ratification
  question, out of scope).
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
(`verification/signoff/evidence/item-2-layout-digital-r2.json`) is hand-written:
`klt signoff --attest` has no producer for item 2 (2AMLogic/klayout-tools#4188).

```console
export PDK_ROOT=<pinned root> PDK=sky130A
klt place-and-route flow/serializer/pnr.request.json --format json
sh verification/signoff/check-serializer-pnr.sh
```

`PDK=sky130A` is needed here because klt otherwise resolves the first variant
under `PDK_ROOT`, which on this host is not a sky130 one.

## Committed artifacts

The routed artifacts committed next to this record are the P&R outputs of the
run above; their sha256 digests are:

| File | sha256 |
|---|---|
| `serializer_routed.gds` | `1cecbc447bb64e157b9827df7adb60e13d678a4076f91cbcfe87c0240bbdd0ce` |
| `serializer_routed.v` (as-built, post-CTS) | `56c0fcec6e669344e1c8c628b7d0d5767036d83aa2b7b5a922746ee64279ac77` |
| `serializer_routed.def` | `3908451bf12beb8ca06aa32f64b234a41ff7e9ebeb96abe430f393fba0ce4539` |
| `serializer_routed.spef` | `82425c64b4fb315d4f8cfa19078aec625f89f3368fc61cc504a4a0c97f135219` |

The paths inside `pnr.response.json` (`gds_path`, `def_path`, `verilog_path`,
`spef_sta.spef_path`) name klt's scratch directory
`flow/serializer/.klt/place-and-route/`, which is not committed; the files
above are copies of those outputs, and the response is otherwise verbatim.
Recorded as a klt tool gap at 2AMLogic/klayout-tools#4231.

The binding is executed, not merely transcribed:
`verification/signoff/check-hygiene.sh` re-measures each of the four files
and compares it against this table; it runs in CI as part of the T1 item 10
attestation, so a perturbed or regenerated artifact fails the hygiene check
instead of drifting silently. The SPEF row is the load-bearing one:
`sta.response.json` points its top-level `spef_path` at the committed
`serializer_routed.spef` while its provenance hash covers only the DEF, so
this table is the only recorded binding of the parasitic numbers `STA.md`
rests on.
