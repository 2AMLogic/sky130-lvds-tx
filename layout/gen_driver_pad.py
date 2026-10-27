"""Generate layout/sky130_lvds_tx_driver_pad.gds (T1 item 2, analog; issue #22).

Run from the repository root with the pinned PDK on the environment:

    PDK_ROOT=~/.ciel PDK=sky130A klayout -b -r layout/gen_driver_pad.py

Environment: PDK_ROOT (default ~/.ciel), PDK (default sky130A), KLT (default
`klt`), GEN_OUT (default layout/sky130_lvds_tx_driver_pad.gds).

Stage 1 only (see layout/README.md): the pad-cell frame and the grounded-gate
ESD clamp. The stock sky130_ef_io__analog_noesd_pad is read from the PDK
(DR-001), never redrawn. Output is byte-reproducible: fixed cell names, no
timestamps, and every generated cell comes from `klt gen`, which is itself
deterministic.
"""
import json
import os
import subprocess
import sys
import tempfile

import pya

PDK_ROOT = os.path.expanduser(os.environ.get("PDK_ROOT", "~/.ciel"))
PDK = os.environ.get("PDK", "sky130A")
KLT = os.environ.get("KLT", "klt")
OUT = os.environ.get("GEN_OUT", "layout/sky130_lvds_tx_driver_pad.gds")

IO_GDS = os.path.join(PDK_ROOT, PDK, "libs.ref/sky130_fd_io/gds/sky130_ef_io__analog.gds")
FRAME = "sky130_ef_io__analog_noesd_pad"

# pad_cell.sch: XMESD, W=21.5 x m=4 = 86 um of L=0.55. klt gen caps a finger
# at 20 um, so the clamp is 5 fingers of 17.2 um: same total W, same L.
ESD_PARAMS = {"finger_width_um": 17.2, "l_um": 0.55, "fingers": 5, "add_guard_ring": True}
PAD_PITCH_UM = 75.0
SLOT_DEPTH_UM = 200.0
# Clamp origin inside the slot: below the met4/met5 bus rails, under the met3
# P_CORE stub (x 24.72-49.72), clear of the VCCHIB/VCCD rails at y < 12.
ESD_ORIGIN_UM = (34.0, 20.0)

def die(msg):
    sys.stderr.write("gen_driver_pad: %s\n" % msg)
    sys.exit(1)

def load_frame(dst):
    if not os.path.isfile(IO_GDS):
        die("stock I/O GDS not found: %s (run scripts/setup-env.sh; set PDK_ROOT)" % IO_GDS)
    src = pya.Layout()
    src.read(IO_GDS)
    cell = src.cell(FRAME)
    if cell is None:
        die("%s has no cell %s" % (IO_GDS, FRAME))
    top = dst.create_cell(FRAME)
    top.copy_tree(cell)
    return top

def gen_esd(dst):
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "esd.gds")
        run = subprocess.run(
            [KLT, "gen", "esd_device", "--params", json.dumps(ESD_PARAMS), "--pdk", PDK,
             "--pdk-root", PDK_ROOT, "--cell-name", "lvds_esd_nfet", "-o", out,
             "--format", "json"], capture_output=True, text=True)
        if run.returncode != 0:
            die("klt gen esd_device failed:\n%s%s" % (run.stdout, run.stderr))
        src = pya.Layout()
        src.read(out)
        top = dst.create_cell("lvds_esd_nfet")
        top.copy_tree(src.cell("lvds_esd_nfet"))
    return top

def main():
    ly = pya.Layout()
    ly.dbu = 0.001
    frame = load_frame(ly)
    esd = gen_esd(ly)

    pad = ly.create_cell("sky130_lvds_tx_pad_cell")
    pad.insert(pya.CellInstArray(frame.cell_index(), pya.Trans()))
    ox, oy = ESD_ORIGIN_UM
    pad.insert(pya.CellInstArray(esd.cell_index(), pya.Trans(int(ox / ly.dbu), int(oy / ly.dbu))))

    top = ly.create_cell("sky130_lvds_tx_driver_pad")
    pitch = int(PAD_PITCH_UM / ly.dbu)
    top.insert(pya.CellInstArray(pad.cell_index(), pya.Trans(0, 0)))          # PADP
    top.insert(pya.CellInstArray(pad.cell_index(), pya.Trans(pitch, 0)))      # PADN

    opts = pya.SaveLayoutOptions()
    opts.format = "GDS2"
    opts.gds2_write_timestamps = False
    opts.gds2_write_file_properties = False
    ly.write(OUT, opts)
    print("wrote %s" % OUT)

main()
