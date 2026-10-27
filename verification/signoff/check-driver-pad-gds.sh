#!/bin/sh
# Freshness + footprint check for layout/sky130_lvds_tx_driver_pad.gds
# (issue #22): regenerate with layout/gen_driver_pad.py, require the result to
# be byte-identical to the committed GDS, and require each pad cell to fit the
# 75 x 200 um slot (P3) and the pair to be two slots wide.
#
# Needs klayout, `klt` and the pinned sky130A PDK (PDK_ROOT); local_only.
# Run from the repository root.
set -eu

committed=layout/sky130_lvds_tx_driver_pad.gds
fresh=$(mktemp)
probe=$(mktemp).py
trap 'rm -f "$fresh" "$probe" "${probe%.py}"' EXIT

: "${PDK_ROOT:=$HOME/.ciel}"
export PDK_ROOT PDK="${PDK:-sky130A}"

GEN_OUT="$fresh" klayout -b -r layout/gen_driver_pad.py >/dev/null
if ! cmp -s "$fresh" "$committed"; then
  echo "$committed is stale: it differs from a fresh run of layout/gen_driver_pad.py" >&2
  exit 1
fi

cat > "$probe" <<'PY'
import os, sys
import pya
ly = pya.Layout()
ly.read(os.environ["GDS"])
def box(name):
    c = ly.cell(name)
    if c is None:
        sys.exit("missing cell " + name)
    return c.dbbox()
pad = box("sky130_lvds_tx_pad_cell")
top = box("sky130_lvds_tx_driver_pad")
ok = (abs(pad.width() - 75.0) < 1e-6 and pad.height() <= 200.0 + 1e-6
      and abs(top.width() - 150.0) < 1e-6 and top.height() <= 200.0 + 1e-6)
print("pad cell %.3f x %.3f um; pair %.3f x %.3f um" % (pad.width(), pad.height(), top.width(), top.height()))
sys.exit(0 if ok else "footprint outside the 75 x 200 um slot")
PY
GDS="$committed" klayout -b -r "$probe"
echo "$committed matches a fresh run and fits the slot"
