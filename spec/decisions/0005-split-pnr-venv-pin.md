# 0005 — Split venv pin: a dedicated `.venv-pnr` for digital P&R

**Status**: accepted (toolchain/environment decision; no change to the ratified spec)

## Decision

Provision a second, dedicated place-and-route venv at `.venv-pnr/` carrying
`klayout-tools==0.9.1` installed normally (dependency floor satisfied, no
`--no-deps`) on top of a `klayout==0.30.13` module pin (`PNR_KLAYOUT_VERSION`).
The attest/CI venv (`.venv`, `klayout==0.28.17.post1` + klt `0.9.1
--no-deps`) is left untouched. `scripts/setup-env.sh` provisions both;
`docs/environment.md` records which venv serves what.

This settles issue #120's decision block (settled 2026-11-15 in an attended
`/fleet:decide` session, round 20261111-r14, q101 — auto-selected under
`--yolo 70`, confidence 80%, not an operator ruling): **dedicated P&R venv:
plain klt 0.9.1 (klayout 0.30.x) for the digital PnR re-closure; keep the
attest/CI pair untouched.**

## Context

`klt 0.9.1`'s place-and-route std-cell GDS merge uses a klayout API that
exists only in 0.30.x (`Layout.read_bytes`), so under `.venv`'s
byte-reproducibility pair `klt place-and-route` cannot run at all — it
crashes with `'Layout' object has no attribute 'read_bytes'` (measured in
issue #115). Upstream `2AMLogic/klayout-tools#5768` tracks the gap: no
single klayout pin satisfies P&R and byte-reproducible GDS writes together
(still open as of 2026-11-15). Until upstream resolves it, the two needs
require two module pins, i.e. two venvs. The split is measured to work and
to byte-reproduce the committed digital GDS from the pre-#115 netlist; no
upstream dependency; each evidence envelope records the versions that
actually produced it.

`0.30.13` is pinned exactly — not `>=0.30` — because it is both the version
#119's measured control used and PyPI's current latest (verified
2026-11-15), so the exact pin changes nothing today and stops the P&R
toolchain drifting the next time a 0.30.x ships. The new constant is
prefixed (`PNR_KLAYOUT_VERSION`) because
`verification/signoff/check-driver-pad-gds.sh` parses the bare
`KLAYOUT_VERSION` from `scripts/setup-env.sh` with a `^`-anchored sed — a
second bare assignment would make that gate read two values and fail.

## Alternatives declined

- **One venv at klayout 0.30.x** — re-opens the #104 analog byte gate the
  0.28.17 pin exists to protect (the 0.30.x module re-encodes two TEXT
  `MAG` records in the stock pad-frame cell, so the committed GDS would
  stop regenerating byte-identically).
- **Wait for upstream `klayout-tools#5768`** — still open with no landed
  fix; it would block the digital P&R re-closure (#119) indefinitely.
- **`uvx --from "klayout-tools==0.9.1" klt`** — leaves no recorded pin for
  the module that actually ran, which the evidence convention requires per
  envelope.

## Consequences

- Two pinned venvs exist in `scripts/setup-env.sh` and
  `docs/environment.md` until the reversal condition lands; the split-pin
  wart `klayout-tools#5768` describes persists until then.
- `.venv-pnr` is for `klt place-and-route` only. `klt signoff --attest`,
  evidence regeneration and CI parity keep using `.venv`. yosys and the PDK
  stay provisioned in `.venv` / `PDK_ROOT` (venv-independent).
- `verification/signoff/check-serializer-pnr.sh` needs no change: it
  invokes bare `klt` from `$PATH`, so activating `.venv-pnr` selects the
  P&R toolchain.

## Reversal condition

The split collapses to one venv when `2AMLogic/klayout-tools#5768` lands
("klt 0.9.1 place-and-route GDS merge uses klayout>=0.30-only API
(`Layout.read_bytes`); no single klayout pin satisfies P&R and
byte-reproducible GDS writes together"). To reverse: remove `.venv-pnr`,
collapse the pins back to one venv, and retire this record.
