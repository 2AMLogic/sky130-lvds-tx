#!/bin/sh
# Freshness + footprint check for layout/sky130_lvds_tx_driver_pad.gds
# (issue #22): regenerate with layout/gen_driver_pad.py, require the result to
# be byte-identical to the committed GDS, and require each pad cell to fit the
# 75 x 200 um slot (P3) and the pair to be two slots wide, and require every
# driver.spice device (stage 2) to be present with the right m / SCALE.
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
import os, re, sys
import pya
ly = pya.Layout()
ly.read(os.environ["GDS"])
def cell(name):
    c = ly.cell(name)
    if c is None:
        sys.exit("missing cell " + name)
    return c
def box(name):
    return cell(name).dbbox()
pad = box("sky130_lvds_tx_pad_cell")
pair = box("sky130_lvds_tx_pad_pair")
ok = (abs(pad.width() - 75.0) < 1e-6 and pad.height() <= 200.0 + 1e-6
      and abs(pair.width() - 150.0) < 1e-6 and pair.height() <= 200.0 + 1e-6)
print("pad cell %.3f x %.3f um; pair %.3f x %.3f um" % (pad.width(), pad.height(), pair.width(), pair.height()))
if not ok:
    sys.exit("footprint outside the 75 x 200 um slot")
box("sky130_lvds_tx_driver_pad")

# Stage 2: every driver.spice device is in the GDS with the right multiplicity.
# A leaf device cell labels each unit's gate U<i>_G, so m = number of G labels.
def mult(c):
    n = 0
    for li in ly.layer_indexes():
        for sh in c.shapes(li).each():
            if sh.is_text() and re.search(r"\.U\d+_G$", sh.text_string):
                n += 1
    return n
def count(top, leaf_prefix):
    """total multiplicity of leaf cells whose name starts with leaf_prefix, under top"""
    tot = 0
    for inst in cell(top).each_inst():
        ch = inst.cell
        if ch.name.startswith(leaf_prefix):
            tot += mult(ch)
        else:
            tot += count_sub(ch, leaf_prefix)
    return tot
def count_sub(c, leaf_prefix):
    tot = 0
    for inst in c.each_inst():
        ch = inst.cell
        tot += mult(ch) if ch.name.startswith(leaf_prefix) else count_sub(ch, leaf_prefix)
    return tot
drv = "sky130_lvds_tx_driver"
bad = []
for d, m in [("XMPS", 14), ("XMSPA", 14), ("XMSPB", 14), ("XMSNA", 14), ("XMSNB", 14), ("XMNS", 14),
             ("XMWVA", 4), ("XMWVB", 4), ("XMWPA", 4), ("XMWPB", 4), ("XMGTA", 4), ("XMGTB", 4)]:
    got = sum(count(drv, "drv_slice_s%d_%s" % (sc, d)) for sc in (1, 11))
    if got != m:
        bad.append("%s: %d != %d" % (d, got, m))
for d in ["XMP_sb", "XMN_sb", "XMLN1", "XMLN2", "XMLP1", "XMLP2", "XMPU", "XMPP", "XMND", "XMNP"]:
    got = count(drv, "drv_sel_" + d)
    if got != 3:
        bad.append("%s: %d != 3" % (d, got))
for d in ["XMNB1", "XMNB2", "XMPB", "XMT", "XM1", "XM2", "XML1", "XML2", "XCC"]:
    got = count(drv, "drv_" + d)
    if got != 1:
        bad.append("%s: %d != 1" % (d, got))
for d in ["XRS1", "XRS2"]:
    if not any(c.name == "drv_" + d for c in ly.each_cell()):
        bad.append("missing resistor " + d)
if bad:
    sys.exit("driver device mismatch vs design/driver/driver.spice: " + "; ".join(bad))
b = box(drv)
print("driver %.1f x %.1f um (%.0f um^2) vs one 75 x 200 slot (15000 um^2)" % (b.width(), b.height(), b.width() * b.height()))
print("driver devices match design/driver/driver.spice (m / SCALE)")
PY
GDS="$committed" klayout -b -r "$probe"
echo "$committed matches a fresh run, fits the slot, and carries the driver devices"
