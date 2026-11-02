# DR-009: Pad-cell body substrate tie to VSSIO is deferred to the clamp seam

- **Status**: proposed; no `spec/target-spec.md` value changes
- **Date**: 2026-11-02
- **Author**: builder agent, issue #77
- **Ratifies against / input to**: T1 item 11 (`klt erc` supply spec), `verification/README.md`, `DR-001`, `DR-008`
- **Supersedes**: none

## Context

`klt erc` with a `VSSIO` substrate tie (`well_complement_of: ["64/20"]`) reports
`erc.missing_tie` on the upper body (y 50 to 180 um) of both pad cells. That body
is a p-well inside the stock `sky130_ef_io__analog_noesd_pad` deep n-well. It already
has a drawn p-tap ring. The ring's only metal path goes to an unlabelled met4 rail
(y 37 to 40 um, x 19.5 to 55 um) that lies inside the ESD clamp's footprint
(probably its guard ring; not traced to the clamp's devices), and nothing carries it to a supply strap. `layout/README.md`
lists the clamp-to-`VSSIO` connection as not drawn (issue #24).

## Decision

Do not add a tap or a strap from this ring to `VSSIO` in this change. Keep the
`substrate_vssio` tie declared in `analog.supply-spec.json` so the two findings stay in
the committed ERC record (`item-11-erc-analog-r2.json`) instead of disappearing.
Item 11 analog stays unmet. The finding is not waived, and no ratified spec value
is relaxed.

## Rationale

The island's role (clamp source, body, or both) is not established without the pad and clamp LVS that is also deferred.
A metal bridge to `VSSIO` could short a clamp terminal. DR-001 puts the ESD
path on `VSSIO` only, so the intended end state is a `VSSIO` tie, but it should be drawn
with the clamp connection, where DRC feedback and an LVS of the pad exist.

## Consequences

- Item 11 analog cannot grade `met` until the clamp is wired to `VSSIO` (#24); the
  expected change is then to re-run `klt erc` and expect no `erc.missing_tie`.
- This record is not an acceptance of the stock frame as a finished design.
