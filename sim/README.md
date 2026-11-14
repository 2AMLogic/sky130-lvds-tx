# sim

ngspice testbenches and PVT corner results.

- `pdk-smoke/` — minimum-size inverter per MOS family at the PDK's tt/ff/ss
  corners. Proves the pinned models load; it is not the driver.
- `unpowered-pad/` — DC bench for the fail-safe well biasing with VCCD =
  VDDIO = 0 V (spec rows P4, P4a, P4b; `DR-008`). Both pads swept together
  0–2.4 V, the differential partner pattern, and the supply-ramp transient,
  over five process corners at −40 and 125 °C. **All three rows fail on the
  committed schematics**; the four findings and the follow-up each one owes
  are in `unpowered-pad/RECORD.md`.
