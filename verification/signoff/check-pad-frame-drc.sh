#!/bin/sh
# Reproduce the classification of the stock pad frame's DRC findings (issue #44,
# layout/README.md "DRC of the stock pad frame"): the 486 met4/met5 violations
# in the analog report are in the PDK's own geometry, not in this repo's.
#
#   1. each stock cell, standalone, under the curated sky130 deck
#   2. the same stock cell under the foundry-native deck (sky130A_mr.drc)
#   3. a row of 5 stock cells abutted at the 75 um pitch
#
# Asserts the recorded counts; exits 1 on any difference. Needs klayout, `klt`
# and the pinned sky130A PDK (PDK_ROOT); local_only. Run from the repo root.
set -eu

: "${PDK_ROOT:=$HOME/.ciel}"
export PDK_ROOT
KLT="${KLT:-klt}"
GDS="$PDK_ROOT/sky130A/libs.ref/sky130_fd_io/gds/sky130_ef_io__analog.gds"
[ -f "$GDS" ] || { echo "stock I/O GDS not found: $GDS" >&2; exit 1; }
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

count() {  # <report.json> -> "<status> <violation_count> <rule_counts>"
  python3 -I -c 'import json,sys
d = json.load(open(sys.argv[1]))
print(d["status"], d["violation_count"], json.dumps(d["rule_counts"], sort_keys=True))' "$1"
}
expect() {  # <label> <got> <want>
  if [ "$2" != "$3" ]; then
    echo "MISMATCH $1" >&2; echo "  got:  $2" >&2; echo "  want: $3" >&2
    fail=1
  else
    echo "ok  $1: $2"
  fi
}
fail=0

for cell in sky130_ef_io__analog_noesd_pad sky130_ef_io__simple_pad_and_busses; do
  "$KLT" drc --deck sky130 --top "$cell" --format json "$GDS" > "$tmp/$cell.json" || [ $? -eq 3 ]
done
expect "curated deck, analog_noesd_pad" "$(count "$tmp/sky130_ef_io__analog_noesd_pad.json")" \
  'violations 257 {"met4.area.1": 1, "met4.enclosing.via3.1": 80, "met4.holes_area.1": 20, "met4.space.1": 108, "met4.width.1": 20, "met5.area.1": 2, "met5.width.1": 26}'
expect "curated deck, simple_pad_and_busses" "$(count "$tmp/sky130_ef_io__simple_pad_and_busses.json")" \
  'violations 229 {"met4.area.1": 1, "met4.enclosing.via3.1": 80, "met4.holes_area.1": 20, "met4.space.1": 108, "met4.width.1": 20}'

"$KLT" drc --engine klayout --pdk sky130A --pdk-root "$PDK_ROOT" --top sky130_ef_io__analog_noesd_pad \
  --format json "$GDS" > "$tmp/native.json" || [ $? -eq 3 ]
expect "foundry-native deck, analog_noesd_pad" "$(count "$tmp/native.json")" \
  'violations 241 {"m1.3ab": 6, "m4.1": 20, "m4.2": 108, "m4.3": 80, "m4.4": 1, "m5.1": 26}'

cat > "$tmp/row.py" <<'PY'
import os
import pya
ly = pya.Layout()
ly.read(os.environ["GDS"])
src = ly.cell("sky130_ef_io__analog_noesd_pad")
top = ly.create_cell("row5")
for i in range(5):
    top.insert(pya.CellInstArray(src.cell_index(), pya.Trans(i * 75000, 0)))
ly.write(os.environ["ROW_OUT"])
PY
GDS="$GDS" ROW_OUT="$tmp/row5.gds" klayout -b -r "$tmp/row.py" >/dev/null
"$KLT" drc --deck sky130 --top row5 --format json "$tmp/row5.gds" > "$tmp/row5.json" || [ $? -eq 3 ]
expect "curated deck, 5 abutted analog_noesd_pad" "$(count "$tmp/row5.json")" \
  'violations 1173 {"met4.area.1": 5, "met4.enclosing.via3.1": 400, "met4.holes_area.1": 100, "met4.space.1": 540, "met4.width.1": 100, "met5.area.1": 2, "met5.width.1": 26}'

exit "$fail"
