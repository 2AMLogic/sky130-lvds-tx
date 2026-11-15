#!/bin/sh
# Freshness check behind T1 item 1 (digital partition): re-synthesize
# rtl/serializer.v from flow/serializer/synth.request.json and require the
# result to be byte-identical to the committed gate-level netlist. The
# netlist sha256 is reproducible across runs; synth.response.json differs per
# run only in run_id, so the netlist (not the response) is the compared artifact.
#
# Needs `klt`, yosys and the sky130 PDK (PDK_ROOT, or klt's PDK search path);
# the inventory marks this check local_only so a toolchain-free CI runner
# re-verifies file hashes but skips the re-synthesis.
#
# TMPDIR caveat: klt synthesize's yosys -> yosys-abc invocation deadlocks when
# the TMPDIR path is longer than ~35 characters (measured 2026-11-15, klt
# 0.9.2.dev1029+g76f47afa48f1 / yosys 0.67+post: 35 passes, 36 hangs), with no
# diagnostic and no timeout on this host (#5780 reports the 300 s yosys
# watchdog firing in its own configuration). The trigger is the path length,
# not TMPDIR being non-default. Run with a short TMPDIR:
#   TMPDIR=/tmp sh verification/signoff/check-serializer-netlist.sh
# Upstream: 2AMLogic/klayout-tools#5798 and #5780; background in
# verification/README.md.
#
# Run from the repository root.
set -eu

req=flow/serializer/synth.request.json
committed=flow/serializer/serializer_synth.v
out=$(mktemp)
trap 'rm -f "$out"; rm -rf flow/serializer/.klt' EXIT

klt synthesize "$req" --format json > "$out"
netlist=$(python3 -I -c '
import json, sys
print(json.load(open(sys.argv[1]))["netlist_path"]["path"])' "$out")

if ! cmp -s "$netlist" "$committed"; then
  echo "$committed is stale: it differs from a fresh synthesis of rtl/serializer.v" >&2
  diff "$netlist" "$committed" | head -20 >&2 || true
  exit 1
fi
echo "$committed matches a fresh synthesis"
