# 0003 — Retire the smoke placeholder bench

Status: accepted (verification housekeeping; decides nothing the spec decides).

## Context

`verification/smoke/{smoke.v,test_smoke.py,negative_control/smoke_broken.v}` were
a 4-bit counter DUT that proved the cocotb/Icarus harness and its negative
control "until the real serializer lands". The serializer landed in `e4167d4`
with its own bench and negative control (`verification/serializer/`), which CI
already runs. The placeholder had become the local `pnpm test` target and the
digital leg of the item-9 cold start, so local checks and the attested cold
start exercised the placeholder rather than the design.

## Decision

- Delete the three placeholder files and the CI "Smoke bench" step.
- Keep `verification/smoke/runner.py` (hosts `run_bench()`, imported by the
  serializer runner) and `verification/smoke/requirements.txt`; moving them to
  a shared location is a separate follow-up. `0001-verification-runner-kept-separate.md`
  names `smoke/runner.py` as the runner's home and stays accurate.
- `verification/signoff/cold-start.sh` runs the serializer bench for its digital
  leg (good leg plus negative control, so the leg still proves the harness
  can fail). The analog leg is unchanged.

## Evidence

Recorded evidence is append-only. `verification/signoff/evidence/item-9-testbenches.json`
is not edited. The inventory changed (placeholder files out, serializer bench
files in), so item 9 is re-attested with `klt signoff --attest 9`, which
produces a new record superseding the old one. The earlier record stays in git
history as the attestation of the placeholder-era cold start.
