# sim

ngspice testbenches and PVT corner results.

- `pdk-smoke/` — minimum-size inverter per MOS family at the PDK's tt/ff/ss
  corners. Proves the pinned models load; it is not the driver.
- `driver-dc/` — V_OD and V_OS of the current-steering driver in both static
  data states, pre-emphasis disabled, over the G75 PVT grid (spec rows E1-E4,
  DC only). Simulated, against a proposed spec; it closes no spec row on its
  own, because E1-E4 are statistical rows and the Monte Carlo is not run here.
