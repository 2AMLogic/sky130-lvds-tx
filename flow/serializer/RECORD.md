# Serializer synthesis — record

`rtl/serializer.v` (8:1 → 2:1 reduction, ÷4 word clock) synthesized on
`sky130_fd_sc_hd` at the `ss_100C_1v60` Liberty corner (S3's reference corner)
with a 2.0 ns clock target.

## What changed for issue #98, and why

Setup failed at every `ss` corner in post-route STA (`STA.md`, previous
revision). The critical path was the counter decode: `cnt[0]/Q` → one decode
gate → the `sr` load/shift mux select → `sr[0]/D`, with every signal cell at
minimum drive and `cnt[0]`/`cnt[1]` fanning out to 13/12 loads. Two changes,
both cycle-exact (the cocotb bench and the negative control still pass —
`verification/serializer/`):

1. **RTL: the `sr`-load and `cap`-capture enables are held in flops.** They
   were decoded combinationally from `cnt` (`last = (cnt == LAST)`) at the
   point of use; they are now registered one cycle of *decision* earlier from
   `cnt_next`, so each carries exactly the value the equivalent decode of
   `cnt` would have in the same cycle. The `cnt` → decode → register-input
   path disappears from the design: the enables reach the mux selects straight
   off a flop. Reset values are the constant-folded decodes of `cnt == 0`.
   This is a retiming of the enables, not of the datapath — bit order, the
   word boundary and the `word_clk` phase contract of `DR-003`/`DR-004` are
   unchanged.
2. **Synthesis request: `dont_use` for the weak-drive complex gates** that
   ABC kept mapping the high-fanout decode through (`mux2i`, `or2`, `and2`,
   `a21o`, `a22o`, `o21a`, `and3b`, `or3`, `and3` — all `_1`-only in the
   previous netlist). The mapper now builds the decode from `nand2`/`nand2b`/
   `nor2`/`nor3b`/`a21oi`/`o21bai` + an output buffer, which P&R's
   `repair_timing` can size up; drive-strength diversity is introduced
   post-route instead (two enables land as `dfxtp_2`/`dfxtp_4`, the decode
   `nor3b` as `_2` — see `serializer_routed.v`).

The negative control
(`verification/serializer/negative_control/serializer_broken.v`) is a
near-verbatim copy of the restructured RTL with the same two-line mutation as
before (`CW = $clog2(CYC + 1)`, `LAST_W = CYC` — counter wraps one cycle
late), so the bench still bites on the new design.

## Run

| Field | Value |
|---|---|
| Request / response | `synth.request.json` / `synth.response.json` (run `run-b9e5c0c8159b4668b26f9ae3389bb221`) |
| Netlist | `serializer_synth.v`, sha256 `c9760e742c2d3979b42795345cce86394152de8d4a1bb0dd17c5328a79025353` |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` |
| `klt` | `0.9.1` (pinned venv per `scripts/setup-env.sh`) |
| Yosys | `0.68.0.0.post1208` (yowasp wheel; wasm sha256 `e37a7e65…` verified against the pin) |
| Result | 76 instances, 675.6 µm² (400.4 µm² sequential), 20 flops, 0 latches, 0 combinational loops |

## What this does and does not show

- The netlist is **reproducible**: `verification/signoff/check-serializer-netlist.sh`
  re-synthesizes from `rtl/serializer.v` + `synth.request.json` and requires the
  result byte-identical to the committed netlist. `synth.response.json` is not
  byte-reproducible (`run_id` differs per run), so the netlist (not the response)
  is the compared artifact. The check is `local_only`: CI re-verifies the
  inventoried files' hashes but does not re-run Yosys.
- `timing` is `null` in the pinned run's response (klt 0.9.1 records the
  `timing_unavailable` warning where the older build printed ABC's `abc_stime`
  estimate); the 2000 ps delay target is still enforced by the request's
  `clock_period_ns`. `sta` is `null`: the `klt_statime_native` extension is not
  installed on this host, so **no gate-level STA was run and spec S3 is not
  claimed here**. Post-route STA with 10 % clock uncertainty is recorded in
  `STA.md`: setup passes at every corner inside the spec's supply range,
  including S3's reference corner `ss_100C_1v60`; the S3 verdict stays NOT MET
  only because the sub-1.62 V `ss` libraries still fail (ratification question,
  out of scope).
- Regenerated under the repo's pinned venv (`scripts/setup-env.sh`: `klt 0.9.1`,
  `yowasp-yosys 0.68.0.0.post1208` wasm-sha-verified) per issue #115: the
  previous netlist carried a host-yosys (`0.67+post`) header and was
  pin-irreproducible. The logic is unchanged — same 76 instances across the
  same 10 cell types; the regenerated netlist differs from the old one only in
  the version header and net-alias/port-connection renames. **The routed GDS
  does not reproduce from this netlist** (a fresh P&R yields a different
  physical implementation — OpenROAD's resizer/CTS are net-name-sensitive);
  that re-closure is tracked separately, and the committed
  `serializer_routed.gds` and downstream digital envelopes correspond to the
  previous netlist until it lands.

## Retired stand-in smoke flow

`flow/pdk-smoke/` (a 4-bit stand-in counter run through `klt synthesize` and
`klt place-and-route` to prove the pinned Yosys → OpenROAD path) was retired
once the serializer exercised the same path. Its recorded result is not
deleted from history: it was added in commit `62424be` and remains readable
there (`git show 62424be:flow/pdk-smoke/RECORD.md`). Retirement ruled on in
issue #39.

## Reproduce

```console
export PDK_ROOT=<pinned root>
klt synthesize flow/serializer/synth.request.json --format json
sh verification/signoff/check-serializer-netlist.sh
python3 verification/serializer/runner.py   # cocotb bench + negative control
```
