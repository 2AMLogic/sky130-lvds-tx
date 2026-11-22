# sim

ngspice testbenches and PVT corner results.

- `pdk-smoke/` — minimum-size inverter per MOS family at the PDK's tt/ff/ss
  corners. Proves the pinned models load; it is not the driver.
- `driver-dc/` — V_OD and V_OS of the current-steering driver in both static
  data states, pre-emphasis disabled, over the G75 PVT grid (spec rows E1-E4,
  DC only). Simulated, against a proposed spec; it closes no spec row on its
  own, because E1-E4 are statistical rows and the Monte Carlo is not run here.
- `pad-dc/` — the pad cell's DC shunt current and junction capacitance at the
  pad, over G75's process and temperature axes (the supply axis is collapsed:
  the cell has no supply pin). Evidence for `P1` and the pad-side spot check of
  `P4`; it is not an ESD qualification and does not claim `P1` met.
- `unpowered-pad/` — DC bench for the fail-safe well biasing with VCCD =
  VDDIO = 0 V (spec rows P4, P4a, P4b; `DR-008`). Both pads swept together
  0–2.4 V, the differential partner pattern, and the supply-ramp transient,
  over five process corners at −40 and 125 °C. **All three rows fail at the
  bench's pinned base commit** (`d7da34a8`, which predates the ESD-diode
  sizing fix `cd0c89a`); the four findings and what each still owes are in
  `unpowered-pad/RECORD.md`.
- `driver-tran/` — powered transient bench: PRBS-7 through one
  `lvds_tx_analog` into the 100 Ω ‖ 1 pF-per-side pad load, at 1 Gb/s and
  the 400 Mb/s fallback, over G75 (spec rows E5 edges, E9 eye, E4 dynamic
  V_OS(PP), W1 analog subtotal). The record gives per-pad slew times, folded
  differential eye openings, dynamic common-mode misses and the applicable
  power margins against the proposed spec. [Transient record](driver-tran/RECORD.md).

**Provenance convention:** a `RECORD.md` provenance block's `Client` row
klayout figure is the run's own `provenance.klayout_version` — the `klayout`
Python module the run's `klt` imported, readable live via `klt version
--format json` — **not** the host CLI's `klayout -v` and **not** the
`docs/environment.md` venv pin. Where a record disagrees with its run's
committed report, the report is canonical. How the record is corrected
depends on the block. A **pinned** block — everything above a record's
`## Addendum …` heading, which that heading declares append-only — is
corrected by an annotation immediately below its table and never by editing
the cell. The **current addendum** block, being the record's newest text,
may have a provenance row corrected in place, provided an annotation
immediately below the table preserves the figure originally printed.
