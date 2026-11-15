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
