# Serializer post-route SDF — per-corner generation and the item-7 annotated run

Evidence record for T1 item 5's `sta` companion and the item 7 (digital)
attempt: two post-route SDFs written from the **committed** routed artifacts,
and the outcome of the SDF-annotated functional run against them. Request:
`sdf.request.json`; committed response: `sdf.response.json`.

## Method

- `klt sta`, `def` mode, `sdf: true`, on `serializer_routed.def` with
  `serializer_routed.spef` — one IEEE-1497 SDF per analyzed corner
  (`write_sdf -divider . -include_typ`, immediately after `read_spef`).
  This writes from the same DEF + SPEF as `sta.response.json`; **nothing was
  re-placed or re-routed** (`klt place-and-route`'s `post_route_sdf` was not
  used), so the routed bytes items 2, 3, 4 and 11 digital bind to are
  untouched. SPEF annotation at both corners: 93/93 design nets, 0 reader
  warnings (`annotation_complete: true`; `sdf.response.json` also records
  `unannotated_driver_count` 1 and `floating_driver_count` 1 (`clkload0/Y`),
  and `partially_unannotated_driver_count` 2 (`_116_/Q`, `_117_/Q`; `dout[0]`,
  `dout[1]`)).
- klt `0.9.1` (`.venv-pnr`, klayout `0.30.13` — the STA pin,
  `spec/decisions/0005-split-pnr-venv-pin.md`), OpenROAD `26Q3-1510-g6cb3f2b704`,
  PDK open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (provenance in
  `sdf.response.json`).
- Committed SDF copies: `serializer_routed.ss_n40C_1v76.sdf`,
  `serializer_routed.ff_n40C_1v95.sdf` — byte-identical to the run's
  `.klt/sta/` outputs (per-corner `sdf.content_hash` in `sdf.response.json`
  pins the committed files; re-running the request reproduces them).

## Corner selection

The spec's core supply is 1.8 V ± 10 % = 1.62–1.98 V (row C5,
`spec/target-spec.md`; the S3 STA table's 16 corners span well below that
floor). Filtering the committed 16-corner STA table (`STA.md`) to libraries
inside that literal window, the setup extremes are:

| Corner | Setup WNS (ns) | Role |
|---|---|---|
| `ss_n40C_1v76` | +0.488 | slowest (binding) in-window corner |
| `ff_n40C_1v95` | +1.292 | fastest in-window corner |

`ss_100C_1v60` (1.60 V) is below the window floor — `STA.md` calls the 1.60 V
library a slow boundary proxy; it is not exercised here. The Liberty corner
name identifies each SDF; the SDF triplet selection (`corner: "max"` on the
`ss` file, `"min"` on the `ff` file) is recorded in the probe below.

## The SDF-annotated run (T1 item 7): passes, but not committable at the pin

The same cocotb suite (`verification/serializer/test_serializer.py`) ran
SDF-annotated against `serializer_routed.v` with the pinned PDK's
`sky130_fd_sc_hd` verilog models (`primitives.v` + `sky130_fd_sc_hd.v`) at
both corners — `ss_n40C_1v76` at `corner: "max"`, `ff_n40C_1v95` at
`corner: "min"`, seed 21, under klt `0.9.1` + Icarus 13.0:

- **4/4 tests passed at both corners**, `environment.sdf.annotated: true`,
  `partial: true` — the dropped classes are disclosed Icarus limitations,
  not silent losses: `timingcheck` (20; Icarus implements SDF
  delay annotation but not TIMINGCHECK), `zero_delay_alias_port_interconnect`
  (2) and `zero_delay_bus_port_source_interconnect` (8; both zero-delay
  entries, timing-neutral by construction).
- **The 2AMLogic/klayout-tools#5002 `vvp` abort does not reproduce** on this
  design (93 design nets as measured here; the SDF fixes #5296, #5705 and #6075 are in 0.9.1). No
  simulator abort, no refused SDF construct.

The reports are **not committed**, and item 7 stays open, because the pinned
release cannot publish them portably:

1. `environment.sdf.file` in a 0.9.1 report is an **absolute host path**
   (2AMLogic/klayout-tools#5784, open) — the sole host-specific field in an
   otherwise repo-relative report.
2. A committed request cannot resolve the std-cell simulation models
   portably: `klt functional-verification`'s `pdk` block
   (2AMLogic/klayout-tools#6434) landed **after** 0.9.1, so the cell models
   would have to be named in `sources` by host-specific PDK paths.

Per #169 these are not papered over (no host paths in committed evidence, no
hand-written `$sdf_annotate` loader, no SDF stripping). The remedy is a pin
bump to a release carrying #6434 and the #5784 fix, proposed as its own
change; until then the committed artifacts above are the item-7 staging
point: the SDFs and their hash-pinned regeneration recipe.

## Negative control

The control is the RTL pair (`rtl.report.json` pass, 4/4;
`negative-control.report.json` fail, 3/4 — word-clock, walking-ones and
back-to-back fail, reset passes; both committed beside the requests). There
is no broken *gate-level* netlist to annotate: synthesizing and routing one
is out of scope for #169 (it would change the serializer), so an annotated
control is not available — the control is established at RTL only.

## Not covered

- Timing checks: every SDF TIMINGCHECK section is dropped by Icarus (see
  above); the annotated run proves functional behaviour under back-annotated
  *delays*, not $setup/$hold against the characterised limits.
- The three unconstrained output endpoints of `STA.md`'s completeness note
  (`dout[0]`, `dout[1]`, `word_clk`) are carried by the same DEF + Liberty —
  unchanged here.
- Out of scope: re-routing, spec S3 ratification, a toolchain pin change.
