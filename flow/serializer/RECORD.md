# Serializer synthesis — record

`rtl/serializer.v` (8:1 → 2:1 reduction, ÷4 word clock) synthesized on
`sky130_fd_sc_hd` at the `ss_100C_1v60` Liberty corner (S3's reference corner)
with a 2.0 ns clock target.

| Field | Value |
|---|---|
| Request / response | `synth.request.json` / `synth.response.json` (run `run-806c4ca2481d40f2a7d4c5ab30f92139`) |
| Netlist | `serializer_synth.v`, sha256 `ef27a14ba381f0032c5add3d11b0cdbb7efd82a52f305cf9c7094b1dd841ac74` |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` |
| `klt` | `0.8.1.dev55+g879d39bad82b` (host) |
| Yosys | `0.67+post` |
| Result | 60 instances, 625.6 µm² (360.3 µm² sequential), 18 flops, 0 latches, 0 combinational loops |

## What this does and does not show

- The netlist is **reproducible**: two consecutive runs gave the same netlist
  sha256. `synth.response.json` is not byte-reproducible (`run_id` differs per
  run), so the freshness check (`verification/signoff/check-serializer-netlist.sh`)
  compares the netlist, not the response.
- `timing` is ABC's `abc_stime` estimate (critical path 1446.69 ps against the
  2000 ps target). `sta` is `null`: the `klt_statime_native` extension is not
  installed on this host, so **no gate-level STA was run and spec S3 is not
  claimed here**. S3 stays open until an STA step reports setup slack with 10 %
  clock uncertainty.
- Synthesized here with the host `klt`, which is newer than the `KLT_REV` that
  `scripts/setup-env.sh` pins (0.6.0); the item 1 envelope was attested with the
  `signoff.yml` pin. The netlist is expected to be the same under the pinned
  `klt`; that has not been checked.
- The re-synthesis freshness check is `local_only`: CI re-verifies the
  inventoried files' hashes but does not re-run Yosys.

## Reproduce

```console
export PDK_ROOT=<pinned root>
klt synthesize flow/serializer/synth.request.json --format json
sh verification/signoff/check-serializer-netlist.sh
python3 verification/serializer/runner.py   # cocotb bench + negative control
```
