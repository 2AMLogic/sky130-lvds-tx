# Dynamic-gmin reproducer (issue #176)

Minimal, self-contained evidence for the "Dynamic gmin stepping failed"
diagnosis in the 2026-11-21 RECORD.md addendum. Three decks, one circuit
(Sweep B, `tt`/-40 °C, the isolation netlist at `45ebd2d3`), one variable:
the `.meas` set.

| Deck | `.meas` set | Result |
|---|---|---|
| `deck-sweepb-tt-m40-full.cir` | all 96 (as `klt sim` generates) | `Warning: Dynamic gmin stepping failed`, recovered by true gmin stepping, all measurements produced |
| `deck-sweepb-tt-m40-pari.cir` | exactly one: `.meas dc idiff_max MAX par('(i(vamp) - i(vamn)) / 2')` | same warning — the minimal trigger |
| `deck-sweepb-tt-m40-nomeas.cir` | none | no stepping attempted, clean solve |

Logs from the committed decks (same ngspice build as the addendum's
provenance table) are the accompanying `*.log` files.

## Run

From a scratch directory (the deck must be run with `wnflag=1` in force,
which the graded runs set through `klt`'s `.spiceinit` mechanism):

```sh
mkdir -p /tmp/gmin-repro && cd /tmp/gmin-repro
echo "set wnflag=1" > .spiceinit
ngspice -b <repo>/sim/unpowered-pad/repro-gmin/deck-sweepb-tt-m40-full.cir
grep -c "Dynamic gmin stepping failed" ngspice.log   # or redirect stdout
```

The `.lib` line pins the PDK install this repo uses (`/home/ubuntu/.ciel`,
see RECORD.md "Pinning the PDK root"); adjust it if your sky130A lives
elsewhere. Everything else resolves relative to the deck (`../tb_sweep_b.spice`
and, through it, `../../../design/lvds_tx_analog.spice`), so the decks run
from a clean checkout at `45ebd2d3` or later.

## Circuit-level probe (not committed as a deck)

The node-side half of the diagnosis: with the full `.meas` set restored,
insert a 1 GOhm anchor on the two floating predriver wells — inside the
`predriver` subckt of a throwaway copy of
`design/lvds_tx_analog.spice`, directly before its `.ends`:

```spice
RPWM PWM VSSIO 1e9
RPWE PWE VSSIO 1e9
```

and point the deck's `.include` at a `tb_sweep_b.spice` copy whose
`../../design` resolves to that copy. The warning disappears (Sweep B
`tt`/-40 °C and ramp `tt`/125 °C go clean; Sweep A `tt`/-40 °C drops from
four cold-start failures to one). This is a diagnostic probe only — no
bleeder was landed; the design disposition belongs to #167.
