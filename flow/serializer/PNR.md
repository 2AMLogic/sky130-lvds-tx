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

## What changed for issue #119, and why

#115 regenerated `serializer_synth.v` under the pinned `yowasp-yosys`
(net-alias renames, e.g. `load ↔ _031_`), which moved the input out from
under the previously committed response: `klt place-and-route --check`
reported `drifted`, and a control run proved the routed GDS does **not**
reproduce from the regenerated netlist — the cause is the netlist, not the
toolchain. This record's run re-closes the flow against the current (r2)
netlist, per the pin decision in `spec/decisions/0005-split-pnr-venv-pin.md`:

1. **The P&R toolchain moved to `.venv-pnr`** (`klt 0.9.1` +
   `klayout 0.30.13`, `PNR_KLAYOUT_VERSION`); the previous run used a host
   dev build of klt. OpenROAD and the PDK pin are unchanged.
2. **The fresh implementation is a different physical layout of the same
   logic.** OpenROAD's resizer/CTS sized differently from the renamed nets
   (`nand2_1 ×14 → nand2_1 ×12 + nand2_4 ×2`, `clkbuf_1 → clkbuf_16`, a
   `buf_12` added; fill redistributed; vias moved). The backend is
   **net-name-sensitive**: byte-reproducibility holds for a *fixed* netlist
   (two seeded runs and `check-serializer-pnr.sh` reproduce
   `serializer_routed.gds` byte-identically), but a netlist regeneration is
   expected to change the routed bytes even at identical connectivity.
3. **Equivalence is established the flow's own way**: `klt lvs` of the fresh
   GDS against the fresh `serializer_routed.v` (the same run's output) is
   `match` (`item-4-lvs-digital-r4.json`), the input binding carries
   P&R ↔ `serializer_synth.v`, and the gates re-ran clean: DRC `clean`
   (`item-3-drc-digital-r3.json`), ERC `clean` with `VCCD`/`VSS` one island
   each (`item-11-erc-digital-r3.json`). STA (`STA.md`) keeps the same
   verdict shape as the previous record: setup passes at every corner inside
   the spec's supply range (`ss_n40C_1v60` now +0.035 ns) and still fails at
   the five sub-1.62 V `ss` libraries.

## Run

| Field | Value |
|---|---|
| Request / response | `pnr.request.json` / `pnr.response.json` |
| Input netlist | `serializer_synth.v`, sha256 `c9760e742c2d3979b42795345cce86394152de8d4a1bb0dd17c5328a79025353` (matches `provenance.input.content_hash`) |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (`PDK_ROOT` resolved to the pinned revision; see `provenance.pdk` and `layer_map` in the response) |
| `klt` | `0.9.1` (`.venv-pnr` pin, with `klayout==0.30.13`; `spec/decisions/0005-split-pnr-venv-pin.md`) |
| OpenROAD | `26Q3-1510-g6cb3f2b704` |
| P&R corner | `ss_n40C_1v60`, sweep `ss_100C_1v60` / `ss_n40C_1v60` / `ss_n40C_1v76` / `tt_025C_1v80` / `ff_n40C_1v95`; seed 1; clock 1.6 ns |
| Stage reached | `route`, status ok, `warnings: []` |

## Results

- Die 2297.76 µm², core 1764.19 µm², **46.31 % utilization achieved** (35 %
  requested); wirelength 1317 µm.
- **Router-internal** counts (not the item 3 signoff DRC, and metal density is
  explicitly not evaluated, see `coverage` in the response): 0 route DRC
  violations, 0 antenna violations; `min_area_repair`: clean, 0 patches.
- Timing at the P&R corner (`ss_n40C_1v60`, 1.6 ns implementation clock, no
  uncertainty): worst setup slack −0.144 ns, worst hold slack +0.849 ns — the
  negative setup slack is against the deliberately tighter implementation
  target, not the spec budget (see above). After post-route SPEF
  back-annotation (`post_route_spef`, 93/93 design nets annotated) at the same
  1.6 ns: −0.165 ns setup, 0 hold violations. Judged at the real 2.0 ns /
  0.2 ns-uncertainty budget in `STA.md`, the same netlist passes the three
  in-spec `ss` corners.
- Power block (`pnr.response.json` → `power`, quoted for item 11): `pdn: true`,
  `global_connect: true`, `power_net: VCCD`, `ground_net: VSS`,
  `tapcell_master: sky130_fd_sc_hd__tapvpwrvgnd_1` (25 tapcells, distance 14 µm),
  straps on met1/met4/met5, `placed.status: "complete"` (299 components,
  192 fillers). `VCCD` was accepted and global-connected as the rail name
  with no rename needed.

## What this does not show

- **Spec S3 is claimed by `STA.md`, not here.** The slack above is at the P&R
  implementation corner and clock, neither of which is the S3 budget. Post-route
  STA at every Liberty corner with 10 % uncertainty is in `STA.md`: setup now
  passes at every corner inside the spec's supply range, and the S3 verdict
  stays NOT MET only because the sub-1.62 V `ss` libraries still fail (ratification
  question, out of scope).
- DRC (#24), LVS (#25) and the supply `klt erc` spec (#26) of this GDS are
  separate items; they were re-run for this re-closure and are claimed by
  their own envelopes (`item-3-drc-digital-r3.json`,
  `item-4-lvs-digital-r4.json`, `item-11-erc-digital-r3.json`), not here.
- Not integrated with the analog pad slot or any top-level floorplan.

## Reproducibility

Two consecutive runs of the request gave a byte-identical GDS, routed
verilog, DEF and SPEF (the response differs only in per-run `invocation_id`s
and log directories), and `verification/signoff/check-serializer-pnr.sh`
reproduced the same bytes again from the committed tree. The premise is
**for a fixed netlist**: the backend is net-name-sensitive, so a regenerated
netlist yields a different routed GDS even at identical connectivity — that
is the drift #115's regeneration exposed and #119 re-closed, not a gate
failure to suppress. `klt place-and-route --check flow/serializer/pnr.response.json
flow/serializer/pnr.request.json` (and with `--rerun`) reports `match`.
`check-serializer-pnr.sh` runs the `--rerun` check and
byte-compares a fresh GDS to the committed one; it is `local_only` (needs
OpenROAD and the PDK), so CI re-verifies the committed file's hash but does not
re-route. The item 2 envelope
(`verification/signoff/evidence/item-2-layout-digital-r3.json`) is produced
by `klt signoff --attest 2` (klayout-tools#4188's producer) under the attest
venv, with the regeneration claim backed by that script; the r2 envelope is
hand-written history.

```console
source .venv-pnr/bin/activate
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
| `serializer_routed.gds` | `f5de09887d17301b9e8fe89fbdf97f84ec97d78ce362900790783e058d158f25` |
| `serializer_routed.v` (as-built, post-CTS) | `0ee679daaa4fad342e6b9983a57ef15dff3653e8fac9cda5919fc02542ce5e15` |
| `serializer_routed.def` | `909673a1341851f1b1b8f3194c8d1664e326dccd120d9cc8dec82ed301eadd44` |
| `serializer_routed.spef` | `6ae32c78bfb4d822d882b0969d8719d43e038863f38ecfd060254bcad21dc7cd` |

The previous implementation's artifacts (`1cecbc44…` GDS / `56c0fcec…`
verilog / `3908451b…` DEF / `82425c64…` SPEF) correspond to the
pre-#115 netlist and are superseded; the r2-era envelopes that bind them
stay as append-only history.

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
