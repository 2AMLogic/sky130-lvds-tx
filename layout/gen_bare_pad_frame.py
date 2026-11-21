"""Generate layout/bare_pad_frame.gds (T1 item 3 analog; issue #165).

The bare-cell side of the disclosed foundry-cell DRC exception (operator
ruling on issue #44, applied per issue #165): two unmodified instances of
the PDK's `sky130_ef_io__simple_pad_and_busses` at the 75 um pad pitch --
the same cell, at the same relative placement, as the two instances inside
`sky130_lvds_tx_driver_pad`'s pad pair -- and nothing else. No geometry of
this repo is present; the cell subtree is copied from the stock I/O GDS
(DR-001), never redrawn, so its `cell_geometry_digest` equals the cell's
digest inside the block layout and the stock GDS itself.

Run from the repository root with the pinned PDK on the environment:

    PDK_ROOT=~/.ciel PDK=sky130A klayout -b -r layout/gen_bare_pad_frame.py

Environment: PDK_ROOT (default ~/.ciel), PDK (default sky130A),
GEN_OUT (default layout/bare_pad_frame.gds). Output is byte-reproducible:
no timestamps, fixed cell names.
"""
import os

import pya

PDK_ROOT = os.path.expanduser(os.environ.get("PDK_ROOT", "~/.ciel"))
PDK = os.environ.get("PDK", "sky130A")
OUT = os.environ.get("GEN_OUT", "layout/bare_pad_frame.gds")

IO_GDS = os.path.join(PDK_ROOT, PDK, "libs.ref/sky130_fd_io/gds/sky130_ef_io__analog.gds")
CELL = "sky130_ef_io__simple_pad_and_busses"
TOP = "bare_pad_frame"
PITCH_UM = 75.0

if not os.path.isfile(IO_GDS):
    raise SystemExit("gen_bare_pad_frame: stock I/O GDS not found: %s "
                     "(run scripts/setup-env.sh; set PDK_ROOT)" % IO_GDS)

src = pya.Layout()
src.read(IO_GDS)
cell = src.cell(CELL)
if cell is None:
    raise SystemExit("gen_bare_pad_frame: %s has no cell %s" % (IO_GDS, CELL))

ly = pya.Layout()
ly.dbu = 0.001
stock = ly.create_cell(CELL)
stock.copy_tree(cell)
top = ly.create_cell(TOP)
top.insert(pya.CellInstArray(stock.cell_index(), pya.Trans()))
top.insert(pya.CellInstArray(stock.cell_index(),
                             pya.Trans(int(PITCH_UM / ly.dbu), 0)))

opts = pya.SaveLayoutOptions()
opts.format = "GDS2"
opts.gds2_write_timestamps = False
opts.gds2_write_file_properties = False
ly.write(OUT, opts)
print("wrote %s" % OUT)
