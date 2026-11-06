# Serializer STA — spec S3 (post-route, all `sky130_fd_sc_hd` Liberty corners)

Evidence record for spec row S3: setup slack >= 0 with 10 % clock uncertainty at
every Liberty corner, 500 MHz (2.0 ns) clock. Request: `sta.request.json`;
committed response: `sta.response.json`.

## Method

- `klt sta`, `def` mode, on `serializer_routed.def` with `serializer_routed.spef`
  (71/71 design nets annotated at every corner), clock `clk` at 2.0 ns, ideal clock.
- **Uncertainty applied with `constraints.clock_uncertainty_ns: {"setup_ns": 0.2}`**
  (10 % of 2.0 ns), reported in the response as `clock_uncertainty.applied: true`.
  No period substitution was used; hold is timed with no uncertainty.
- **klt version: `0.9.2.dev103+g9f4cec35997a`** (the host-installed klt). The repo
  pin in `signoff.yml` is `0.8.0`, which predates `clock_uncertainty_ns`
  (klayout-tools#4240); the pin was **not** changed. OpenROAD `26Q3-1510-g6cb3f2b704`,
  PDK open_pdks `f6eeac7dad085ffcc829ccfd721f7b4ce39edcf7`.
- Corners: the 16 `sky130_fd_sc_hd` Liberty files in the pinned PDK, excluding the two
  `*_ccsnoise` variants (same corner, different noise model). Check: `sta.request.json`.
- Sanity: `tt_025C_1v80` shows +0.618 ns here against +0.818 ns in `PNR.md`
  (no uncertainty); the 0.2 ns difference is exactly the applied uncertainty.

## Per-corner results

| Corner | Setup WNS (ns) | Setup TNS (ns) | Setup viol. | Hold WNS (ns) | `constraint_completeness` (unconstrained) | Worst setup path | Setup |
|---|---|---|---|---|---|---|---|
| `ff_100C_1v65` | +0.862 | 0.00 | 0 | +0.359 | incomplete (3) | `_100_/Q` → `_086_/D` | pass |
| `ff_100C_1v95` | +1.062 | 0.00 | 0 | +0.284 | incomplete (3) | `_100_/Q` → `_086_/D` | pass |
| `ff_n40C_1v56` | +0.624 | 0.00 | 0 | +0.411 | incomplete (3) | `_100_/Q` → `_093_/D` | pass |
| `ff_n40C_1v65` | +0.778 | 0.00 | 0 | +0.361 | incomplete (3) | `_100_/Q` → `_093_/D` | pass |
| `ff_n40C_1v76` | +0.916 | 0.00 | 0 | +0.319 | incomplete (3) | `_100_/Q` → `_093_/D` | pass |
| `ff_n40C_1v95` | +1.064 | 0.00 | 0 | +0.268 | incomplete (3) | `_100_/Q` → `_086_/D` | pass |
| `ss_100C_1v40` | -1.670 | -26.17 | 18 | +1.268 | incomplete (3) | `_100_/Q` → `_086_/D` | FAIL |
| `ss_100C_1v60` | -0.569 | -8.00 | 17 | +0.909 | incomplete (3) | `_100_/Q` → `_086_/D` | FAIL |
| `ss_n40C_1v28` | -6.722 | -114.22 | 18 | +2.368 | incomplete (3) | `_100_/Q` → `_093_/D` | FAIL |
| `ss_n40C_1v35` | -4.204 | -71.20 | 18 | +1.766 | incomplete (3) | `_100_/Q` → `_093_/D` | FAIL |
| `ss_n40C_1v40` | -3.093 | -52.09 | 18 | +1.485 | incomplete (3) | `_100_/Q` → `_093_/D` | FAIL |
| `ss_n40C_1v44` | -2.418 | -40.65 | 18 | +1.321 | incomplete (3) | `_100_/Q` → `_093_/D` | FAIL |
| `ss_n40C_1v60` | -0.876 | -14.25 | 18 | +0.896 | incomplete (3) | `_100_/Q` → `_086_/D` | FAIL |
| `ss_n40C_1v76` | -0.147 | -2.00 | 17 | +0.689 | incomplete (3) | `_100_/Q` → `_086_/D` | FAIL |
| `tt_025C_1v80` | +0.618 | 0.00 | 0 | +0.447 | incomplete (3) | `_100_/Q` → `_086_/D` | pass |
| `tt_100C_1v80` | +0.633 | 0.00 | 0 | +0.461 | incomplete (3) | `_100_/Q` → `_086_/D` | pass |

Hold is met (positive, no violations) at every corner.

## Constraint completeness

`constraint_completeness.status` is `incomplete` at every corner, for the same three
unconstrained endpoints: `dout[0]`, `dout[1]`, `word_clk`. These are output ports with
no output delay constraint; unclocked registers: 0. The clock-to-register paths are
fully timed, but output-port timing is not covered by this record.

## Verdict for S3: NOT MET

Setup fails with 10 % uncertainty at every slow-process (`ss_*`) corner and passes at
all `tt_*` and `ff_*` corners.

- **Spec-grid reference corner `ss_100C_1v60`** (RECORD.md's S3 reference): WNS
  **-0.569 ns**, 17 failing endpoints.
- **`ss_n40C_1v60`**: WNS -0.876 ns, the worst of the `ss` corners at 1.60 V.
- **Worst overall (binding): `ss_n40C_1v28`**, WNS -6.722 ns. The 1.28–1.44 V libraries
  sit well below the spec's 1.8 V ±10 % core supply (1.62 V), so they are listed
  because the row says "every Liberty corner"; the in-spec-supply picture is the
  1.60 V pair above, and the nearest one to spec (`ss_n40C_1v76`, -0.147 ns) also fails.
- Worst setup path: `_100_/Q` → `_086_/D` (or `_093_/D` at the low-voltage `ss_n40C`
  corners); detail in `sta.response.json` (`worst_setup_path`).

This is a finding, not a spec change. The spec row and clock are unchanged; closing
it needs a design or constraint change tracked separately.

## Not covered

- Liberty data above 100 °C is not published (spec PVT note). The spec's 125 °C
  `ss` / `ff` conditions are **not covered** by this record; `ss_100C_*` and
  `ff_100C_*` are the hottest corners checked, and they are not 125 °C evidence.
- Items out of scope: manifest item-5 citation, SDF re-run (item 7), P&R re-run.
