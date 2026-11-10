# DR-009: Pad-cell body substrate tie to VSSIO is deferred to the clamp seam

- **Status**: proposed; no `spec/target-spec.md` value changes
- **Date**: 2026-11-02
- **Author**: builder agent, issue #77
- **Ratifies against / input to**: T1 item 11 (`klt erc` supply spec), `verification/README.md`, `DR-001`, `DR-008`
- **Supersedes**: none

## Context

The stock `sky130_ef_io__analog_noesd_pad` cells enclose their upper body (y 50 to
180 um) in a deep n-well (`64/18`). The body is a p-tub inside it, with a drawn
p-tap ring (`65/44`); an n-well ring (`64/20`, 2.6 to 72.2 um) surrounds the tub. A
DNW/p-tub junction isolates the tub from the global p-substrate, so its bias is a
separate design choice (`VSSIO`, a quiet ground, or deliberately floated to cut pad
capacitance), not substrate continuity.

A first draft classified the tub under the `VSSIO` substrate tie
(`well_complement_of: ["64/20"]`). That tie reported `erc.missing_tie` on the two
tub boxes (the DNW extent), and it also left the n-well ring with no declared tie.

The ring's tap has a metal path only to two met4 stubs at y 37 to 40 um (x 19.5 to
25.7 and 48.7 to 54.9 um). Measured on the committed GDS they are li1-to-met4 stacks
of the stock `sky130_ef_io__simple_pad_and_busses` cell; no shape of this repo's
cells touches them, and this repo's clamp (`lvds_esd_nfet__core`, x 33 to 40 um)
sits between them with its own guard tap. DR-001 puts no ESD device in the stock
cell. Their intended net is not established. `layout/README.md` lists the
clamp-to-`VSSIO` connection as not drawn (issue #24).

## Decision

Do not add a tap or a strap from the tub or the ring to any net in this change.
Declare the tub and the ring as their own tie classes in
`analog.supply-spec.json` so the findings stay in the committed ERC record
(`item-11-erc-analog-r4.json`) and do not disappear:

- `substrate_vssio` becomes the complement of `64/20` and `64/18`: the global
  p-substrate only.
- `pad_ptub_vssio`: the p-tub in `64/18`, net `VSSIO` (the DR-001 end-state
  intent, a bias choice).
- `pad_dnw_ring_vddio`: the n-well ring, net `VDDIO`, **provisional**. The ring was
  previously unchecked.

Item 11 analog stays unmet. The four `erc.missing_tie` findings (two per ring or
tub) are not waived, and no ratified spec value is relaxed.

## Rationale

The tub and ring bias nets are decisions the pad and clamp LVS, still deferred,
must inform. Folding the tub into the substrate tie asserted a requirement the
physics does not impose and hid the unchecked ring. A strap drawn now to an
unestablished net could short a terminal, and the only metal reaching the ring is
stock-frame geometry whose purpose is unestablished.

## Consequences

- Item 11 analog cannot grade `met` until the tub and ring are tied. The exit
  condition is a strap from the stock tub pickups (the met4 stubs) to the chosen
  net, then a re-run of `klt erc` expecting no `erc.missing_tie`. Wiring the clamp
  to `VSSIO` (#24) alone does not clear the findings. That strap needs its own
  tracking issue or an explicit scope under #24.
- The ring's net (`VDDIO`) and the tub's net (`VSSIO`) are to be confirmed when the
  strap is drawn.
- This record is not an acceptance of the stock frame as a finished design.
