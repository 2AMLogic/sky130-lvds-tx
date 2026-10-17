# PDK analog smoke — record

Simulated, not measured. Proves the pinned sky130A models and the `tt`/`ff`/`ss`
corner sections load and give sane inverter transients for both MOS families.
It says nothing about the driver.

| Field | Value |
|---|---|
| Repo base commit | `98d7150dbac92abfffb3e00588730fc3708bfc3e` (inputs below are content-hashed) |
| PDK | sky130A, open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (ciel 2.6.1; `docs/environment.md`) |
| Model library sha256 | `17c208a699228f5acb87bf59c09c22a4c4d3937b6766b4957737d34e8e075f64` (`sky130.lib.spice`) |
| Netlist sha256 | `f60f32b82db5eff3e4e391dc4024d9b3dc2a20fee58f004f3c82bb4b72d9408a` (`inverters.spice`) |
| Client | `klt 0.7.1.dev1757+ge7cca478ef21`, klayout 0.30.12 |
| Engine | ngspice-46 on the batch worker (`klt` runner 0.7.0); client-side ngspice is 42 and did not run the corners |
| Backend | `batch` (host default), job `klt-sim-c812af437506`, 3 units, `options.stage_model_inputs: true` |

## What ran

One `klt sim` request (`request.json`): `inverters.spice` holds a 1.8 V
inverter (`sky130_fd_pr__nfet_01v8`/`pfet_01v8`, W 0.42 µm, L 0.15 µm, 1.8 V
supply) and a 5 V-rated-family inverter (`nfet_g5v0d10v5`/`pfet_g5v0d10v5`,
W 0.42 µm, L 0.50 µm, 3.3 V supply), 2 fF load each, 10 ps step, 12 ns
transient. Corners `tt`, `ff`, `ss` at 27 °C. Results: `results/summary.json`
(per-corner values) and `results/report.json.gz` (the full `klt sim` report).

Propagation delays, ps (50 % to 50 %):

| Family | Corner | tpHL | tpLH |
|---|---|---|---|
| 1.8 V core | tt | 33.5 | 56.9 |
| 1.8 V core | ff | 25.1 | 45.9 |
| 1.8 V core | ss | 44.1 | 77.0 |
| 5 V-rated @ 3.3 V | tt | 49.0 | 89.6 |
| 5 V-rated @ 3.3 V | ff | 39.2 | 73.3 |
| 5 V-rated @ 3.3 V | ss | 61.9 | 118.0 |

All 3 corners pass; the outputs reach the rails (`vhigh` = supply, `vlow` below
5 % of supply). Ordering ff < tt < ss holds in every case.

## Caveats

- **The worker image's own PDK is a different revision**
  (`open_pdks c6d73a35f524…`; the report's `pdk_stamp_comparison` says
  `mismatch`). A first run without staging used it. The committed run stages
  the pinned `sky130.lib.spice` and its include closure (319 files,
  `environment.staged_model_inputs`), so the executed models are the pinned
  ones. The per-corner numbers were identical in the two runs.
- The first submit hit the fleet's concurrency cap
  (`batch_concurrency_cap`); the run was re-submitted with
  `--wait-for-capacity` and went to the fleet, not to this host.
- Temperature and supply were not swept; only the PDK process corners were.
- Reproduce: `PDK_ROOT=<pinned root> klt sim sim/pdk-smoke/request.json --report-out …`.
