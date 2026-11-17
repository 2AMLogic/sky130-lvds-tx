#!/bin/sh
# Freshness check behind T1 item 2 (digital partition): re-run place-and-route
# from flow/serializer/pnr.request.json and require (a) the committed
# pnr.response.json to still match (klt place-and-route --check --rerun) and
# (b) the freshly routed GDS to be byte-identical to the committed
# flow/serializer/serializer_routed.gds. The GDS is byte-reproducible at the
# fixed seed -- two consecutive runs and a third from the committed tree gave
# the same sha256 (issue #119).
#
# The byte-compare is premised on a FIXED netlist: the P&R backend is
# net-name-sensitive, so a regenerated netlist yields a different routed GDS
# even at identical connectivity (OpenROAD's resizer/CTS follow net and
# instance names; measured in issue #119). A byte-compare failure after a
# netlist regeneration therefore means the digital evidence must be
# re-closed -- re-run P&R, then the gates and envelopes that cite it, and
# commit the new artifacts -- not that this flow broke, and not something to
# suppress here.
#
# Needs `klt`, OpenROAD and the sky130 PDK (PDK_ROOT, PDK=sky130A); local_only,
# like the synthesis freshness check. Run from the repository root with the
# P&R venv active (.venv-pnr) so `klt` is the pinned pair.
set -eu

req=flow/serializer/pnr.request.json
report=flow/serializer/pnr.response.json
committed=flow/serializer/serializer_routed.gds
out=$(mktemp)
trap 'rm -f "$out"; rm -rf flow/serializer/.klt' EXIT

klt place-and-route --check "$report" "$req" --rerun
klt place-and-route "$req" --format json > "$out"
fresh=$(python3 -I -c '
import json, sys
print(json.load(open(sys.argv[1]))["gds_path"]["path"])' "$out")

if ! cmp -s "$fresh" "$committed"; then
  echo "$committed is stale: it differs from a fresh place-and-route of $req" >&2
  exit 1
fi
echo "$committed matches a fresh place-and-route"
