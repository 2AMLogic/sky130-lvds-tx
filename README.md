# sky130-lvds-tx

A ~1 Gb/s-per-lane LVDS-class transmitter on the
[SkyWater sky130](https://github.com/google/skywater-pdk) open PDK —
serializer, current-steering low-swing driver and custom pad cells, with a
D-PHY-class low-swing mode as a stretch — designed by AI agents driving
[klayout-tools](https://github.com/2AMLogic/klayout-tools), xschem + ngspice
on the analog side and Yosys/OpenROAD on the digital side.

**Status: design and verification in progress; the spec is drafted but not
yet ratified.** The serializer RTL is synthesized, placed and routed with
post-route STA recorded, the analog driver and pad-cell layout is committed and
LVS-clean on both partitions, and 13 of the 22 T1 checklist items are met.
`manifests/sky130-lvds-tx.signoff.json` is the graded verdict of record;
`WORK_PLAN.md` tracks what is open.

**Built agent-native.** Every specification, decision record, testbench, and
line of documentation here is produced by AI agents working from a ratified
spec and an append-only evidence trail — not human-authored work that agents
merely assisted with. Verification is the product: every claim traces to a
recorded result under PVT corners. Where the agents hit friction with the
open-source tooling — most often
[klayout-tools](https://github.com/2AMLogic/klayout-tools) — that friction is
filed as a public issue against the tool itself, so the fix benefits everyone
using sky130, not just this repo.

## Why this block, on this node

LVDS (TIA/EIA-644) is the workhorse low-swing differential link: a
current-steering driver pushing about 3.5 mA through a 100 Ω receiver
termination for a ~350 mV differential swing around a ~1.2 V common mode.
It is the standard way a chip moves a few hundred Mb/s to a few Gb/s per
pair off-package at low power.

On sky130 the hard part is not the driver's core but its edge. The driver
needs a regulated common mode, matched rise and fall, and a direct path to
a pad with ESD protection and little capacitance — and the sky130 I/O
library is built around general-purpose pads. Whether its existing pad
structures can carry a ~1 Gb/s low-swing signal, or a custom pad cell must
be drawn, is the first question this repo answers. Sitting next to
`gf180-tmds-tx` (the fleet's first custom pad-ring block) it also makes the
pad-ring problem a two-PDK one.

## Scope

- **In scope**: an 8:1 (or 7:1, see spec) serializer; a current-steering
  LVDS driver with common-mode feedback and pre-emphasis; a low-swing
  D-PHY-class mode as a stretch; the pad cell with its ESD structure; a
  forwarded clock lane.
- **Not in scope**: the PLL that makes the bit clock. It comes from a sibling
  canary; this repo has no `consumes:` edge yet and specifies the clock
  interface, including the jitter budget, and stops. The receiver is also
  out of scope.
- **Not claimed**: compliance with any interface standard. See `CLAUDE.md`.

## Target specification (PROPOSED — not yet ratified)

`spec/target-spec.md` and its decision records `DR-001`…`DR-008` are the
authority; the table below is a summary. The spec is marked *proposed* and its
ratification record is still empty — agents do not ratify their own spec.

| Parameter | Target | Fallback | Stretch |
|---|---|---|---|
| Rate per lane | 1 Gb/s | 400 Mb/s | 1.5 Gb/s |
| Lanes | 4 data + 1 forwarded clock | 1 data + 1 clock | 8 data |
| Differential swing (V_OD) | 247–454 mV into 100 Ω, LVDS window | — | — |
| Common mode (V_OS) | 1.125–1.375 V | — | — |
| Low-swing mode | — | — | D-PHY-class ~200 mV HS swing |
| Serialization | 8:1 | — | 7:1 option |
| Signoff | DRC + LVS clean, pad cell included | — | — |

Maturity ladder: spec ratified → serializer verified → driver simulated
across PVT → pad cell DRC-clean → assembled and LVS-clean → post-layout
eye simulation → shuttle seat → measured silicon. **Current position: spec
drafted and awaiting ratification; serializer verified by its cocotb bench and
routed (post-route STA records spec row S3 not met at the `ss` corners); driver
PVT simulation and analog DRC clean are open.**

## Repo layout

```
spec/          proposed spec + decision records
rtl/           serializer and lane control
verification/  cocotb testbenches + signoff evidence records
design/        analog schematics (driver, CMFB, pre-emphasis, final serializer stage)
sim/           testbenches + PVT corner results (ngspice)
flow/          serializer synthesis and place-and-route (Yosys, OpenROAD)
layout/        GDS + DRC/LVS reports, including the pad cell
manifests/     signoff manifest graded against the T1 checklist
scripts/       environment and toolchain setup
docs/          working notes
measurements/  silicon characterization (empty until tape-out)
```

## License

Apache License 2.0 — see [LICENSE](LICENSE).
