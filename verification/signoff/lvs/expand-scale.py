"""Write driver-scale-expanded.spice: design/driver/driver.spice with the drv_slice
SCALE parameter substituted into a per-scale copy of the subcircuit.

klt lvs (subckt-call) does not evaluate `m={SCALE}` (2AMLogic/klayout-tools#4406), so the
SCALE=11 slice is compared as m=1. This derived netlist only works around that for a
diagnostic run; design/driver/driver.spice itself is not edited.

Run from the repository root:  python3 -I verification/signoff/lvs/expand-scale.py
"""
import re

SRC = "design/driver/driver.spice"
DST = "verification/signoff/lvs/driver-scale-expanded.spice"

text = open(SRC).read()
m = re.search(r"^\.subckt drv_slice .*?^\.ends\n", text, re.S | re.M)
if not m:
    raise SystemExit("no drv_slice subckt in " + SRC)
template = m.group(0)
scales = sorted({int(s) for s in re.findall(r"drv_slice SCALE=(\d+)", text)})
copies = []
for s in scales:
    body = template.replace(".subckt drv_slice ", ".subckt drv_slice_s%d " % s, 1)
    body = re.sub(r"\s+SCALE=\d+", "", body, count=1).replace("{SCALE}", str(s))
    copies.append(body)
out = text.replace(template, "\n".join(copies))
out = re.sub(r"drv_slice SCALE=(\d+)", r"drv_slice_s\1", out)
header = ("* DERIVED by verification/signoff/lvs/expand-scale.py from design/driver/driver.spice;\n"
          "* do not edit. drv_slice is copied per SCALE with {SCALE} substituted.\n")
open(DST, "w").write(header + out)
print("wrote %s (scales %s)" % (DST, scales))
