# 0004 — Relocate the smoke runner into the serializer bench

Status: accepted (verification housekeeping; decides nothing the spec decides).

## Context

`0003-retire-smoke-placeholder-bench.md` kept `verification/smoke/runner.py`
(hosts `run_bench()`) and `verification/smoke/requirements.txt`, and deferred
moving them as "a separate follow-up". The serializer runner was their only
user, reaching `run_bench()` through an `importlib` loader shim, and the two
`requirements.txt` files were byte-identical (`cocotb==2.0.1`).

## Decision

- `run_bench()` and its helpers now live in `verification/serializer/runner.py`;
  the shim is gone.
- `verification/smoke/` is deleted. CI, `verification/README.md` and
  `verification/signoff/cold-start.sh` use `verification/serializer/requirements.txt`.
- `verification/signoff/item-9-inventory.json` drops `verification/smoke/runner.py`;
  item 9 is re-attested with `klt signoff --attest 9`.
- If a second cocotb bench lands, move `run_bench()` to a neutrally named shared
  module (e.g. `verification/common/`) rather than copying it.

## Supersedes

Only the path references: `verification/smoke/runner.py` named in
`0001-verification-runner-kept-separate.md` is now
`verification/serializer/runner.py`, and the "keep `smoke/runner.py`" bullet in
0003 is carried out. The reasoning of both records is unchanged and they are not
edited.

## Evidence

Recorded evidence is append-only: `item-9-testbenches.json` and its successors
are not edited; the re-attestation produces a new record.
