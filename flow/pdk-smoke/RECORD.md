# PDK digital smoke — record

Proves the pinned Yosys → OpenROAD path runs on `sky130_fd_sc_hd` through `klt`.
The design (`smoke_counter.v`, a 4-bit counter) is a stand-in, not the
serializer.

| Field | Value |
|---|---|
| Repo base commit | `98d7150dbac92abfffb3e00588730fc3708bfc3e` (inputs are content-hashed in the responses) |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7`, `sky130_fd_sc_hd` `tt_025C_1v80` |
| `klt` | `0.6.0+gdac2b5daceb6` (the pinned `KLT_REV`, from `.venv`) |
| Yosys | 0.68 (YoWASP `0.68.0.0.post1208`, wasm sha256 verified by `setup-env.sh`) |
| OpenROAD | `26Q3-1510-g6cb3f2b704` (host, native) |

## Results

- Synthesis (`synth.request.json` → `synth.response.json`): status ok, 13
  instances, 136.38 µm² (80.08 µm² sequential), netlist `smoke_counter_synth.v`.
  `timing` is null (the response warns that the ABC log had no readable timing
  summary), so the 10 ns target is not verified by this stage.
- Place and route (`pnr.request.json` → `pnr.response.json`): status ok, reached
  `route`, seed 1; worst setup slack +9.15 ns at a 10 ns clock, worst hold slack +0.52 ns,
  0 antenna and 0 route DRC violations, die 1675 µm², 13.8 % utilization achieved (10 % requested).

## Caveats

- Utilization is 10 % because the `sky130hd` PDN preset needs a core at least
  28.74 µm wide; a 13-cell design is smaller than the grid. The numbers
  describe the flow running, not density.
- `pnr.response.json` had the checkout's absolute prefix stripped (the paths
  under `.klt/` are relative to the repo root); the DEF/GDS/Verilog it names
  are not committed. The leak is already tracked at
  2AMLogic/klayout-tools#3798 and #3820.
- Reproduce: `source .venv/bin/activate; export PDK_ROOT=<pinned root>`, then
  `klt synthesize flow/pdk-smoke/synth.request.json --format json` and
  `klt place-and-route flow/pdk-smoke/pnr.request.json --format json`.
  `klt synthesize` writes the netlist under `.klt/synthesize/<run-id>/`; it was copied to
  `smoke_counter_synth.v`.
