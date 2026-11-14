# Serializer STA — spec S3 (post-route, all `sky130_fd_sc_hd` Liberty corners)

Evidence record for spec row S3: setup slack >= 0 with 10 % clock uncertainty at
every Liberty corner, 500 MHz (2.0 ns) clock. Request: `sta.request.json`;
committed response: `sta.response.json`.

## Method

- `klt sta`, `def` mode, on `serializer_routed.def` with `serializer_routed.spef`
  (91/91 design nets annotated at every corner), clock `clk` at 2.0 ns, ideal clock.
- **Uncertainty applied with `constraints.clock_uncertainty_ns: {"setup_ns": 0.2}`**
  (10 % of 2.0 ns), reported in the response as `clock_uncertainty.applied: true`.
  No period substitution was used; hold is timed with no uncertainty.
- **klt version: `0.9.2.dev1029+g76f47afa48f1`** (the host-installed klt). The repo
  pin in `signoff.yml` is `0.8.0`, which predates `clock_uncertainty_ns`
  (klayout-tools#4240); the pin was **not** changed. OpenROAD `26Q3-1510-g6cb3f2b704`,
  PDK open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7` (resolved from
  `PDK_ROOT=/home/ubuntu/.ciel`; provenance in `sta.response.json`).
- Corners: the 16 `sky130_fd_sc_hd` Liberty files in the pinned PDK, excluding the two
  `*_ccsnoise` variants (same corner, different noise model). Check: `sta.request.json`.
- Sanity: `tt_025C_1v80` shows +1.035 ns here; `PNR.md`'s P&R-corner figure is
  +0.845 ns at the 1.6 ns implementation clock (no uncertainty). Converting that
  figure to the 2.0 ns period and subtracting the 0.2 ns uncertainty accounts for
  the difference to within 10 ps (the remainder is the P&R-internal estimate's
  parasitics versus this record's SPEF annotation).
- The design behind this record changed for this issue (issue #98): the load/capture
  enables are now registered (see `rtl/serializer.v` and `RECORD.md`), and P&R ran
  with repair aimed at the slow corner at a 1.6 ns implementation clock (see
  `PNR.md` for why the period substitution is implementation-only). The STA method
  itself is unchanged from the previous revision of this record.

## Per-corner results

| Corner | Setup WNS (ns) | Setup TNS (ns) | Setup viol. | Hold WNS (ns) | `constraint_completeness` (unconstrained) | Worst setup path | Setup |
|---|---|---|---|---|---|---|---|
| `ff_100C_1v65` | +1.190 | 0.00 | 0 | +0.363 | incomplete (3) | `_112_/Q` → `_129_/D` | pass |
| `ff_100C_1v95` | +1.319 | 0.00 | 0 | +0.295 | incomplete (3) | `_131_/Q` → `_131_/D` | pass |
| `ff_n40C_1v56` | +1.054 | 0.00 | 0 | +0.421 | incomplete (3) | `_130_/Q` → `_131_/D` | pass |
| `ff_n40C_1v65` | +1.152 | 0.00 | 0 | +0.377 | incomplete (3) | `_112_/Q` → `_129_/D` | pass |
| `ff_n40C_1v76` | +1.238 | 0.00 | 0 | +0.336 | incomplete (3) | `_112_/Q` → `_125_/D` | pass |
| `ff_n40C_1v95` | +1.330 | 0.00 | 0 | +0.287 | incomplete (3) | `_131_/Q` → `_131_/D` | pass |
| `ss_100C_1v40` | -0.564 | -7.33 | 20 | +1.184 | incomplete (3) | `_131_/Q` → `_131_/D` | FAIL |
| `ss_100C_1v60` | +0.192 | 0.00 | 0 | +0.847 | incomplete (3) | `_131_/Q` → `_131_/D` | pass |
| `ss_n40C_1v28` | -3.960 | -73.27 | 20 | +2.292 | incomplete (3) | `_112_/Q` → `_125_/D` | FAIL |
| `ss_n40C_1v35` | -2.163 | -39.39 | 20 | +1.704 | incomplete (3) | `_112_/Q` → `_125_/D` | FAIL |
| `ss_n40C_1v40` | -1.411 | -25.07 | 20 | +1.432 | incomplete (3) | `_112_/Q` → `_125_/D` | FAIL |
| `ss_n40C_1v44` | -0.942 | -16.30 | 20 | +1.272 | incomplete (3) | `_112_/Q` → `_125_/D` | FAIL |
| `ss_n40C_1v60` | +0.093 | 0.00 | 0 | +0.862 | incomplete (3) | `_112_/Q` → `_125_/D` | pass |
| `ss_n40C_1v76` | +0.562 | 0.00 | 0 | +0.661 | incomplete (3) | `_131_/Q` → `_131_/D` | pass |
| `tt_025C_1v80` | +1.035 | 0.00 | 0 | +0.438 | incomplete (3) | `_131_/Q` → `_131_/D` | pass |
| `tt_100C_1v80` | +1.029 | 0.00 | 0 | +0.441 | incomplete (3) | `_131_/Q` → `_131_/D` | pass |

Hold is met (positive, no violations) at every corner; the tightest margin is
+0.287 ns at `ff_n40C_1v95`, the corner the previous revision of this record
already flagged as the hold-critical one.

## Constraint completeness

`constraint_completeness.status` is `incomplete` at every corner, for the same three
unconstrained endpoints: `dout[0]`, `dout[1]`, `word_clk`. These are output ports with
no output delay constraint; unclocked registers: 0. The clock-to-register paths are
fully timed, but output-port timing is not covered by this record.

## Verdict for S3: NOT MET — but met at every corner inside the spec's supply range

Setup now passes with 10 % uncertainty at every `tt_*` and `ff_*` corner **and at the
three `ss` corners inside the spec's core-supply window**; it still fails at the four
slowest `ss` libraries. The row says "every Liberty corner", so the verdict stays
NOT MET until that wording is revisited — which is a ratification question (out of
scope here, see `spec/target-spec.md`); the spec row itself is unchanged.

- **Spec-grid reference corner `ss_100C_1v60`** (RECORD.md's S3 reference): WNS
  **+0.192 ns**, 0 violating endpoints (was −0.569 ns / 17 endpoints).
- **`ss_n40C_1v60`** (the binding in-spec corner, 1.62 V supply floor): WNS
  **+0.093 ns**, 0 violating endpoints (was −0.876 ns / 18 endpoints).
- **`ss_n40C_1v76`**: WNS **+0.562 ns**, 0 violating endpoints (was −0.147 ns).
- **Still failing: the 1.28–1.44 V `ss` libraries** (`ss_n40C_1v28/1v35/1v40/1v44`,
  `ss_100C_1v40`), worst **`ss_n40C_1v28` at −3.960 ns**. These sit well below the
  spec's 1.8 V ±10 % core supply (1.62 V floor, `spec/target-spec.md`); they are
  reported because the row says "every Liberty corner". Whether the row should
  cover libraries below the supply floor is left to ratification.
- What moved the paths: the `cnt` → decode → register-input critical path of the
  previous netlist (`_100_/Q` → `_086_/D`) is gone — the load/capture enables are
  held in flops (RTL change, `RECORD.md`) and P&R repair ran against the slow
  corner at a tightened implementation clock (`PNR.md`). The remaining worst
  paths are the counter's self-increment loop (`_131_/Q` → `_131_/D`) and the
  registered `capture` enable into the shift-register load muxes (`_112_/Q` →
  `_125_/D`), both with positive slack at the corners above.

This is a finding, not a spec change. The spec row and clock are unchanged; the
1.28–1.44 V libraries fail by construction of the ratified "every Liberty corner"
wording, and that wording is a ratification question, tracked separately.

## Not covered

- Liberty data above 100 °C is not published (spec PVT note). The spec's 125 °C
  `ss` / `ff` conditions are **not covered** by this record; `ss_100C_*` and
  `ff_100C_*` are the hottest corners checked, and they are not 125 °C evidence.
- Items out of scope: manifest item-5 citation, SDF re-run (item 7), P&R re-run.
