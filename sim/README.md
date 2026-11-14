# sim

ngspice testbenches and PVT corner results.

- `pdk-smoke/` — minimum-size inverter per MOS family at the PDK's tt/ff/ss
  corners. Proves the pinned models load; it is not the driver.
- `pad-dc/` — the pad cell's DC shunt current and junction capacitance at the
  pad, over G75's process and temperature axes (the supply axis is collapsed:
  the cell has no supply pin). Evidence for `P1` and the pad-side spot check of
  `P4`; it is not an ESD qualification and does not claim `P1` met.
