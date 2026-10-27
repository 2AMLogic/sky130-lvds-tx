#!/bin/sh
# Cold-start entry point for T1 item 9 (testbenches shipped); run by
# `klt signoff --attest 9` from the repository root, and by a third party
# after ./scripts/setup-env.sh (docs/environment.md):
#
#   source .venv/bin/activate && sh verification/signoff/cold-start.sh
#
# Needs uv, iverilog and the pinned sky130A PDK (docs/environment.md); the
# bench's cocotb comes from verification/smoke/requirements.txt via uv.
# Digital leg: cocotb/Icarus smoke bench, good leg plus negative control.
# Analog leg: the PDK smoke request through `klt sim` (3 process corners;
# with KLT_SIM_BACKEND=batch this goes to the batch fleet, never a local
# ngspice loop). Scratch output lives in a temp dir; committed results are
# not rewritten.
set -eu

scratch=$(mktemp -d)
trap 'rm -rf "$scratch"' EXIT

uv run --no-project --with-requirements verification/smoke/requirements.txt \
    python verification/smoke/runner.py --out "$scratch/smoke.json"
klt sim sim/pdk-smoke/request.json -o "$scratch/sim" --report-out "$scratch/sim-report.json"
